"""
corpus_io.py v1.1 — I/O shell for PYQ corpus acquisition, image integrity,
                    document size governance and the Analysis doc.

v1.1 — 2026-07-25 — CLUSTER K: THE Analysis-doc reader, writer and verifier
    (GAP-2026-07-25-002). The Step-2c Analysis doc previously had FOUR readers
    across four specs, implementing four different structural conventions, and no
    writer at all (PYQAnalyse S4-2 was `pass`). Three of the four were measurably
    wrong on the first real exam's doc. One reader, one writer, one verifier; all
    heading recognition delegated to blueprint_core.parse_taxonomy_level so every
    label form works in every step; correctness asserted by round-trip over a
    GENERATED matrix of exam shapes rather than by review. See Cluster K header.


v1.0.3 — 2026-07-25 — optimize_docx gains `always`, which runs the tier ladder even when
    the input is already under budget. Requested so PYQCompress can be driven purely by
    what the operator attaches rather than by a size threshold. force_tier was NOT reused
    for this: it pins one tier and makes the closing `return True` unconditional, so an
    oversized paper would have stopped at that tier, still over budget, and reported
    success with the floor-exceeded WARN suppressed. Adds _no_gain_guard, a
    document-level counterpart to the existing per-part no-growth rule: the ZIP container
    can grow even when no part does, and CHECK 5 treats growth as a HARD STOP, so a small
    already-optimal document would have aborted the run instead of being left alone.

v1.0.2 — 2026-07-25 — MEDIA STEM COLLISION (silent figure loss). optimize_docx renamed
    every re-encoded part to .jpeg/.png and stored it in a dict keyed by that name, so
    two parts sharing a stem and taking the same encoder route (word/media/image1.png +
    word/media/image1.jpg, both photographic) both resolved to word/media/image1.jpeg
    and one OVERWROTE the other. The writer then emitted a duplicate zip member and Word
    rendered whichever it met first, silently replacing one figure with the other.
    Invisible to every existing gate: parts, media and refs all still matched, no
    relationship dangled, and the per-stem pixel check that would have caught it is
    skipped by design at T2-T4 (allow_resample=True) — so the corrupted file passed
    parity and was DELIVERED. Reproduced end to end; T1 caught it, T2-T4 did not.
    Four changes: (a) _target_media_name keeps a part's name when its extension already
    maps to the encoder's content type, so .jpg is no longer renamed to .jpeg and the
    common collision never forms; (b) a genuine remaining collision is disambiguated
    (__c2) rather than overwritten; (c) an explicit input->output name map replaces the
    reverse-lookup in the writer, which could not express a disambiguated name; (d) the
    relationship rewrite is a single regex pass — chained str.replace() with
    {image1.png -> image1.jpeg, image1.jpeg -> image1__c2.jpeg} rewrote the part it had
    just manufactured and pointed both references at one file. A part-count guard
    (len(parts) == len(names)) backstops all of it. assert_docx_parity now compares
    pixel dimensions as an unordered multiset: keying on the stem carried the v1.0.1
    false positive one level up, because a disambiguated name changes the stem.

v1.0.1 — 2026-07-25 — assert_docx_parity raised a FALSE-POSITIVE HARD STOP whenever the
    governor renamed a media part. Re-encoding a photographic PNG produces image1.jpeg
    from image1.png, and the pixel-dimension comparison was keyed on the full basename,
    so the renamed part had no counterpart in `after` and was reported as a dimension
    change on a document whose dimensions were identical (verified: 2400x1800 before and
    after). Dormant on the measured corpus, whose papers store .jpeg parts that the jpeg
    route leaves named as they were; it fires on any PNG-sourced photograph, i.e. exactly
    the papers the governor exists for. Comparison is now by extension-less part name.
    Found by the Framework_PYQSort v1.12 governor test, not by this module's self-test —
    a regression case has been added (io_parity_rename_*).

WHY THIS MODULE EXISTS (and why none of it lives in blueprint_core.py)
    blueprint_core.py declares a THIN-CORE INVARIANT: pure, no I/O, standard library
    only. paper_pipeline.py makes the same promise. Every concern below is inherently
    impure — Drive retrieval, ZIP surgery, image transcoding, disk writes — so hosting
    it in either module would break a stated design invariant. Worse, importing PIL or
    python-docx into blueprint_core.py would make the ALLOCATION core unimportable
    wherever those packages are absent, which is exactly the P0 recorded in
    Framework_MockTestAnalyse v2.26: a failed `import blueprint_core` aborted Step 5
    for EVERY exam.

    corpus_io.py is therefore the one home for impure corpus plumbing, exactly as
    explain_engine.py is the one home for impure explanation plumbing.

        blueprint_core Cluster H   DECIDES   (pure data in -> pure data out)
        corpus_io                  PERFORMS  (bytes, files, images)

    Every decision this module needs is delegated to Cluster H. This module contains
    no thresholds, no ladders and no classification rules of its own.

ANTI-DRIFT CONTRACT
    Steps 1, 2b, 3, 4, 5 and PYQCompress all consume this module. No spec may define a
    local copy of any function named here — enforced by validate_framework_md.py
    Check Z. A spec may only call it or define a thin forwarding adapter. Re-localising
    a shared function produces ZERO drift signal until the two copies disagree; that is
    the failure that required Framework_MockTestAnalyse v2.27 and
    Framework_PYQAnalyse v2.20.

DEPENDENCY POLICY
    Standard library at module scope. Pillow and python-docx are imported LAZILY inside
    the functions that need them, so Cluster H shell functions (path / JSON / ZIP logic)
    keep working without them, and a missing optional dependency surfaces as a named
    error at the point of use rather than an import failure at load time.

DEFECTS THIS MODULE EXISTS TO FIX (see Framework_PYQCompress §3 for the full register)
    B  Drive download was unguarded — zero try/except existed anywhere in the corpus
    G  legacy .doc accepted at enumeration though python-docx cannot open it
    H  native Google Docs silently skipped, removing a paper with no error
    I  images inside TABLES invisible: doc.paragraphs does not descend into tables
    J  legacy VML <v:imagedata> images invisible in every image-handling spec
    K  header / footer / footnote images never extracted
    L  pre-Q.1 images silently discarded rather than bucketed
    N  the real download envelope (context spill + double JSON parse) undocumented
    O  duplicate paper identity double-counted a year
"""

import base64
import io
import json
import os
import re
import shutil
import zipfile

import blueprint_core as bc


# ── exceptions — named and actionable; the CALLER decides what is fatal ──────────

class CorpusError(Exception):
    """Base for every failure raised by this module."""


class TransportFallback(CorpusError):
    """Bytes could not be fetched from Drive. NOT fatal — route to the upload lane.

    Raised for the size cap, a truncated payload, a permission failure, a malformed
    envelope, and any unrecognised connector error. The caller MUST catch this and
    request the paper by chat upload instead of stopping the run.

    This is the guarantee that a future change to the connector's cap cannot break the
    pipeline: correctness does not depend on the predicted partition being right, only
    on the fallback being taken.
    """


class EnumerationError(CorpusError):
    """A Drive folder listing cannot be turned into a usable corpus."""


class DuplicatePaperError(EnumerationError):
    """Two files resolve to the same paper identity — HARD STOP.

    Left unchecked this double-counts the paper's year in the §1-6 coverage gate, or
    drops one of the two depending on listing order.
    """


class IntegrityError(CorpusError):
    """A document failed a structural or image-integrity gate — HARD STOP."""


class VisionUnavailable(CorpusError):
    """The vision liveness probe failed.

    NOT the same as an unreadable image and must never be recorded as one. An unreadable
    image is a property of the IMAGE; this is a property of the SESSION. The remedy is a
    fresh session, not a downgraded classification.
    """


class DependencyMissing(CorpusError):
    """An optional package (Pillow / python-docx) is needed here but not installed."""


# ── constants that are pure I/O concerns (all POLICY lives in Cluster H) ─────────

A_NS = 'http://schemas.openxmlformats.org/drawingml/2006/main'
R_NS = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'
V_NS = 'urn:schemas-microsoft-com:vml'

MEDIA_RE = re.compile(r'^word/(media|embeddings)/', re.I)
RASTER_EXT = ('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tif', '.tiff', '.webp')
VECTOR_EXT = ('.emf', '.wmf', '.svg')

# Every part that can carry a drawing. Footnotes and endnotes are included because a
# figure there is still a figure; omitting them makes the reference count silently low
# and would fire IMG-4 for a benign reason.
STORY_PARTS_RE = re.compile(
    r'^word/(document|header\d*|footer\d*|footnotes|endnotes)\.xml$')

DEFAULT_Q_PATTERN = r'^\s*Q\.?\s*(\d+)'
PREAMBLE = 'preamble'
DEFAULT_UPLOAD_DIR = '/mnt/user-data/uploads'


def _need(mod):
    """Import an optional dependency, or fail with a named, actionable error."""
    try:
        if mod == 'PIL':
            from PIL import Image  # noqa: F401
            return __import__('PIL.Image', fromlist=['Image'])
        if mod == 'docx':
            import docx  # noqa: F401
            return docx
    except ImportError as exc:
        raise DependencyMissing(
            f'{mod} is required for this operation but is not installed ({exc}). '
            f'Install with: pip install {"Pillow" if mod == "PIL" else "python-docx"} '
            f'--break-system-packages')


# ═══════════════════════════════════════════════════════════════════════════════
# CLUSTER H SHELL — ACQUISITION
# ═══════════════════════════════════════════════════════════════════════════════

def parse_drive_folder_id(url):
    """Extract the folder id from a Drive folder URL, or return the input if it already
    looks like a bare id. None when neither."""
    s = str(url or '').strip()
    m = re.search(r'drive\.google\.com/drive/(?:u/\d+/)?folders/([A-Za-z0-9_-]+)', s)
    if m:
        return m.group(1)
    if re.fullmatch(r'[A-Za-z0-9_-]{12,}', s):
        return s
    return None


def normalise_drive_listing(response):
    """Turn any shape of Drive listing response into uniform file records.

    Accepts the bare list, {'files': [...]} or {'items': [...]}, and tolerates both the
    'title' and 'name' spellings the connector has used.

    fileSize arrives as a STRING and is absent for folders and native Google types.
    Both are normalised here so no caller has to think about it. Capturing size at
    enumeration costs nothing — the listing already carries it — and is what allows the
    AUTO/UPLOAD partition to be computed BEFORE any download is attempted, instead of
    discovering the blocker three-quarters of the way through a run.
    """
    items = response
    if isinstance(response, dict):
        items = response.get('files', response.get('items', []))
    out = []
    for it in items or []:
        if not isinstance(it, dict):
            continue
        raw = it.get('fileSize', it.get('size'))
        try:
            size = int(raw) if raw is not None else None
        except (TypeError, ValueError):
            size = None
        out.append({
            'id': it.get('id'),
            'name': it.get('title') or it.get('name') or '',
            'mimeType': it.get('mimeType', ''),
            'fileSize': size,
            'parentId': it.get('parentId'),
            'source': 'gdrive',
        })
    return out


def collect_corpus_files(list_fn, folder_id, recurse=True, require_size=True,
                         _seen=None, _papers=None, _rejects=None, _depth=0):
    """Walk a Drive folder and return (papers, rejects).

    `list_fn(folder_id, page_token=None)` is injected so this is testable without Drive
    and so the caller owns the connector call. It must return whatever the connector
    returns; normalise_drive_listing handles the shape.

    Pagination is followed to exhaustion — without it a folder of more than one page
    silently loses papers.

    Sub-folders are visited in DESCENDING name order so year-named folders are walked
    newest-first, preserving the recency-first intent of the existing enumeration.

    Raises DuplicatePaperError when two usable files share a canonical identity.
    """
    if _seen is None:
        _seen, _papers, _rejects = {}, [], []
    if _depth > 24:
        raise EnumerationError('folder nesting exceeded 24 levels — possible cycle')

    subfolders, page_token = [], None
    while True:
        resp = list_fn(folder_id, page_token=page_token) if page_token else list_fn(folder_id)
        entries = normalise_drive_listing(resp)
        page_token = resp.get('nextPageToken') if isinstance(resp, dict) else None

        for e in entries:
            verdict, reason = bc.screen_drive_entry(
                e['name'], e['mimeType'], e['fileSize'], require_size=require_size)
            if verdict == 'folder':
                subfolders.append((e['name'], e['id']))
                continue
            if verdict == 'reject':
                _rejects.append(dict(e, reason=reason))
                continue
            key = bc.canonical_paper_key(e['name'])
            if key in _seen:
                prev = _seen[key]
                raise DuplicatePaperError(
                    'Two files resolve to the same paper identity — HARD STOP.\n'
                    f'  identity : {key}\n'
                    f'  file A   : {prev["name"]}  (id {prev.get("id")}, '
                    f'{prev.get("fileSize")} bytes)\n'
                    f'  file B   : {e["name"]}  (id {e.get("id")}, '
                    f'{e.get("fileSize")} bytes)\n'
                    'Remove or rename one in Drive. Leaving both makes this paper\'s '
                    'year count twice, or drops one at random depending on listing order.')
            rec = dict(e, paper_key=key)
            _seen[key] = rec
            _papers.append(rec)

        if not page_token:
            break

    if recurse:
        subfolders.sort(key=lambda x: x[0], reverse=True)
        for _, sub_id in subfolders:
            collect_corpus_files(list_fn, sub_id, recurse, require_size,
                                 _seen, _papers, _rejects, _depth + 1)
    return _papers, _rejects


def decode_drive_payload(payload):
    """Turn whatever download_file_content returned into raw file bytes.

    The real contract is not what a one-line pseudocode wrapper suggests, and every
    execution of Steps 2b/4/5 has rediscovered it by trial and error:

      * for any file of consequence the tool result EXCEEDS the context limit and is
        spilled to a JSON file on disk, so `payload` may be a PATH;
      * that spilled JSON is a LIST whose [0]['text'] is itself a JSON STRING;
      * parsing that string yields {'id','title','mimeType','content'} where 'content'
        holds the base64 payload.

    Accepts, in order: raw bytes, a spill-file path, the parsed list/dict, or the inner
    JSON string. Anything else raises TransportFallback so the caller routes to upload
    rather than dying.
    """
    if isinstance(payload, (bytes, bytearray)):
        return bytes(payload)

    obj = payload
    if isinstance(obj, str):
        if os.path.exists(obj):
            try:
                with open(obj, 'r', encoding='utf-8') as fh:
                    obj = json.load(fh)
            except (OSError, ValueError) as exc:
                raise TransportFallback(f'could not read spill file {obj}: {exc}')
        else:
            try:
                obj = json.loads(obj)
            except ValueError:
                raise TransportFallback(
                    'download payload is neither bytes, a spill-file path, nor JSON')

    for _ in range(6):                                   # bounded unwrap; never loops
        if isinstance(obj, list):
            if not obj:
                raise TransportFallback('download payload was an empty list')
            obj = obj[0]
            continue
        if isinstance(obj, dict):
            content = obj.get('content')
            if isinstance(content, str):
                try:
                    return base64.b64decode(content)
                except Exception as exc:
                    raise TransportFallback(f'base64 content would not decode: {exc}')
            text = obj.get('text')
            if isinstance(text, str):
                try:
                    obj = json.loads(text)
                except ValueError:
                    raise TransportFallback(
                        'payload text was not the expected JSON envelope')
                continue
        break
    raise TransportFallback('could not locate base64 content in the download payload')


def verify_downloaded_bytes(raw, expected_size=None, name=''):
    """Prove the payload is a complete .docx before anything downstream trusts it.

    The byte-count check is not redundant with the magic check. A payload truncated at a
    ZIP member boundary can still open as a valid archive while presenting FEWER media
    parts — a silent image loss with no error anywhere. Comparing against the size Drive
    reported is the only thing that catches that case.
    """
    label = f' for {name}' if name else ''
    if not raw:
        raise TransportFallback(f'download returned no bytes{label}')
    if raw[:4] != b'PK\x03\x04':
        raise TransportFallback(
            f'payload{label} is not a .docx (magic {raw[:4]!r}) — it may be an error '
            'page, an HTML login redirect, or a native Google type')
    if expected_size is not None and len(raw) != expected_size:
        raise TransportFallback(
            f'size mismatch{label}: received {len(raw):,} bytes, Drive reported '
            f'{expected_size:,}. Treating as truncated.')
    return True


def fetch_drive_docx(download_fn, paper, dest_dir):
    """Fetch one paper to disk. ANY failure raises TransportFallback — never SystemExit.

    `download_fn(file_id)` is injected so the caller owns the connector call.

    Papers already known to exceed the connector cap are not attempted at all: the
    request is guaranteed to fail and would only add latency. Everything else is
    attempted, because the partition is predictive and a marginal file fetches fine.
    """
    size = paper.get('fileSize')
    name = paper.get('name', '<unnamed>')
    if size is not None and size > bc.DRIVE_CAP:
        raise TransportFallback(
            f'{name} is {size:,} bytes, above the {bc.DRIVE_CAP:,}-byte connector cap — '
            'routing to the upload lane without attempting a download')
    try:
        payload = download_fn(paper['id'])
    except TransportFallback:
        raise
    except Exception as exc:                              # connector / auth / network
        raise TransportFallback(f'download of {name} failed: {exc}')

    raw = decode_drive_payload(payload)
    verify_downloaded_bytes(raw, size, name)
    os.makedirs(dest_dir, exist_ok=True)
    dest = os.path.join(dest_dir, os.path.basename(name))
    with open(dest, 'wb') as fh:
        fh.write(raw)
    return dest


def resolve_uploaded_papers(expected_keys, upload_dir=DEFAULT_UPLOAD_DIR):
    """Match chat-uploaded .docx files against the papers this batch asked for.

    Matching is by CANONICAL identity, never by exact filename and NEVER by recency.

      * exact filename fails because the browser appends " (1)" when the original is
        already in the operator's Downloads folder — which happens on every remediation
        round trip;
      * recency ("the newest three files") fails because uploads ACCUMULATE across
        turns, so by batch 3 the directory still holds batches 1 and 2 and the step
        would silently reprocess them.

    Returns {'matched': {key: path}, 'missing': [...], 'unexpected': [...]}.
    An unrecognised upload is reported, never guessed at and never processed.
    """
    want = set(expected_keys)
    matched, unexpected = {}, []
    if os.path.isdir(upload_dir):
        for fn in sorted(os.listdir(upload_dir)):
            if fn.startswith('~$') or not fn.lower().endswith('.docx'):
                continue
            path = os.path.join(upload_dir, fn)
            key = bc.canonical_paper_key(fn)
            if key in want:
                matched.setdefault(key, path)
            else:
                unexpected.append(path)
    return {'matched': matched,
            'missing': sorted(want - set(matched)),
            'unexpected': unexpected}


# ═══════════════════════════════════════════════════════════════════════════════
# CLUSTER I SHELL — IMAGE INTEGRITY
# ═══════════════════════════════════════════════════════════════════════════════

def _safe_document(path):
    """Open a .docx via python-docx, converting any package-level failure into a NAMED
    error.

    python-docx surfaces a missing or corrupt part as a bare KeyError/BadZipFile from
    deep inside its package reader. Allowing that to escape means a structurally broken
    document produces an unhandled traceback instead of a gate verdict, which is exactly
    the class of failure this module exists to eliminate.
    """
    docx = _need('docx')
    try:
        return docx.Document(path)
    except DependencyMissing:
        raise
    except Exception as exc:
        raise IntegrityError(
            f'{os.path.basename(path)} could not be opened as a Word package '
            f'({type(exc).__name__}: {exc}). The file is corrupt, truncated, or is '
            f'missing a part that its relationships still reference.')


def _open_zip(path_or_zip):
    """Open a .docx as a ZIP, converting archive-level corruption into a NAMED error.

    A .docx IS a ZIP, so a truncated or malformed download surfaces here first as a bare
    BadZipFile. Letting that escape produces an unhandled traceback instead of a gate
    verdict — the exact class of failure this module exists to eliminate.
    """
    if isinstance(path_or_zip, zipfile.ZipFile):
        return path_or_zip
    try:
        return zipfile.ZipFile(path_or_zip)
    except zipfile.BadZipFile as exc:
        raise IntegrityError(
            f'{os.path.basename(str(path_or_zip))} is not a readable Word package '
            f'({exc}). The file is corrupt or truncated.')


def _rels_for(z, part):
    """rId -> media basename, for the .rels belonging to `part`."""
    rel = f'{os.path.dirname(part)}/_rels/{os.path.basename(part)}.rels'
    out = {}
    if rel in z.namelist():
        txt = z.read(rel).decode('utf-8', 'ignore')
        for rid, tgt in re.findall(r'Id="([^"]+)"[^>]*Target="([^"]+)"', txt):
            out[rid] = os.path.basename(tgt)
    return out


def count_image_refs(path_or_zip, body_only=False):
    """Count EVERY image reference in the document. Returns (total, per_part, unresolved).

    Matches BOTH image mechanisms:
      * <a:blip r:embed>      DrawingML — covers inline AND floating (<wp:anchor>)
      * <v:imagedata r:id>    legacy VML — emitted by older Word, some PDF converters,
                              and pasted OLE / equation objects

    and scans every story part (document, headers, footers, footnotes, endnotes), not
    just document.xml.

    Deliberately does NOT use python-docx `inline_shapes`. That property sees only
    inline body drawings, so anchored figures, VML objects and header images are
    invisible to it. A count that can silently run low is worse than no count at all,
    because it makes a broken document look verified.
    """
    z = _open_zip(path_or_zip)
    total, per_part, unresolved = 0, {}, []
    for part in z.namelist():
        if not STORY_PARTS_RE.match(part):
            continue
        if body_only and part != 'word/document.xml':
            continue
        xml = z.read(part).decode('utf-8', 'ignore')
        rels = _rels_for(z, part)
        rids = re.findall(r'<a:blip[^>]*r:embed="([^"]+)"', xml)
        rids += re.findall(r'<v:imagedata[^>]*r:id="([^"]+)"', xml)
        for rid in rids:
            tgt = rels.get(rid)
            if not tgt:
                unresolved.append((part, rid))
                continue
            per_part[tgt] = per_part.get(tgt, 0) + 1
            total += 1
    return total, per_part, unresolved


def dangling_media_targets(path_or_zip):
    """Relationship targets that point at a media part which does not exist."""
    z = _open_zip(path_or_zip)
    names = set(z.namelist())
    out = []
    for n in z.namelist():
        if not n.endswith('.rels'):
            continue
        owner = os.path.dirname(os.path.dirname(n))
        for t in re.findall(r'Target="((?:\.\./)?media/[^"]+)"',
                            z.read(n).decode('utf-8', 'ignore')):
            cand = os.path.normpath(os.path.join(owner, t)).replace('\\', '/')
            if cand not in names:
                out.append(cand)
    return out


def extract_images(path, outdir):
    """Write every media part to disk as ORIGINAL BYTES and describe each one.

    Nothing is re-encoded, re-rendered or resized here — a .docx is a ZIP, so the stored
    bytes ARE the original image. Re-encoding happens only inside the governor, and only
    under assert_docx_parity().

    Vector parts (EMF/WMF/SVG) cannot be opened as rasters. They are labelled 'vector'
    and REPORTED rather than skipped, so a document that will not shrink has a stated
    reason instead of an unexplained result.
    """
    Image = _need('PIL')
    os.makedirs(outdir, exist_ok=True)
    z = _open_zip(path)
    out = {}
    for n in z.namelist():
        if not MEDIA_RE.match(n):
            continue
        raw = z.read(n)
        base = os.path.basename(n)
        fp = os.path.join(outdir, base)
        with open(fp, 'wb') as fh:
            fh.write(raw)
        rec = {'part': n, 'path': fp, 'bytes': len(raw), 'kind': None,
               'format': None, 'size': None, 'mode': None, 'note': ''}
        if os.path.splitext(base)[1].lower() in VECTOR_EXT:
            rec['kind'] = 'vector'
            rec['note'] = 'vector part — rasterise before view(); governor leaves it as-is'
        else:
            try:
                im = Image.open(io.BytesIO(raw))
                im.load()
                rec.update(kind='raster', format=im.format, size=im.size, mode=im.mode)
            except Exception as exc:
                rec['kind'] = 'unreadable'
                rec['note'] = str(exc)[:80]
        out[base] = rec
    return out


def map_images_to_questions(path, q_pattern=DEFAULT_Q_PATTERN):
    """Attach every body image to the question it appears under, in DOCUMENT ORDER.

    Iterates `doc.element.body.iter()`, NOT `doc.paragraphs`.

    This is not a stylistic preference. In python-docx `doc.paragraphs` returns only
    paragraphs that are direct children of the body; paragraphs inside table cells are
    excluded entirely. Any figure laid out in a table — the normal arrangement for
    match-the-following items, multi-panel figures and option grids — is therefore never
    visited and never mapped. The question is then classified TEXT rather than FIGURAL,
    which corrupts the format distribution that drives Step 7 generation, and no error
    is raised anywhere. body.iter() descends into tables and fixes this.

    Images appearing before the first question go to a 'preamble' bucket rather than
    being silently dropped, so IMG-4 does not fire for a benign reason.

    q_pattern is supplied by the caller — this module knows nothing about how any
    particular exam numbers its questions.
    """
    d = _safe_document(path)
    z = _open_zip(path)
    rels = _rels_for(z, 'word/document.xml')
    mapping, cur = {}, PREAMBLE
    for el in d.element.body.iter():
        if el.tag.split('}')[-1] != 'p':
            continue
        txt = ''.join(t.text or '' for t in el.iter() if t.tag.split('}')[-1] == 't')
        m = re.match(q_pattern, txt)
        if m:
            cur = int(m.group(1))
        for b in el.iter(f'{{{A_NS}}}blip'):
            rid = b.get(f'{{{R_NS}}}embed')
            if rid:
                mapping.setdefault(cur, []).append(rels.get(rid, f'UNRESOLVED:{rid}'))
        for v in el.iter(f'{{{V_NS}}}imagedata'):
            rid = v.get(f'{{{R_NS}}}id')
            if rid:
                mapping.setdefault(cur, []).append(rels.get(rid, f'UNRESOLVED:{rid}'))
    return mapping


def verify_images(path, extracted=None, mapping=None, expected_size=None,
                  q_pattern=DEFAULT_Q_PATTERN, workdir=None):
    """Run gates IMG-1 .. IMG-5. Returns (verdicts, stats). Never raises.

    The caller decides what to do with a FAIL; this function only reports. Verdict
    evaluation is delegated to blueprint_core.image_gate_verdict so the pass/fail rules
    are unit-testable without any file present.
    """
    if extracted is None:
        extracted = extract_images(path, workdir or f'/tmp/pyq_img/{os.getpid()}')
        # extract_images raises IntegrityError on a corrupt archive; that is a HARD STOP
        # and is allowed to propagate — there is nothing left to verify.

    # The mapping needs python-docx, which fails hard on a structurally broken package.
    # A broken document must still produce GATE VERDICTS rather than a traceback, so the
    # failure is captured and reported through IMG-4 like any other integrity fault.
    map_error = None
    if mapping is None:
        try:
            mapping = map_images_to_questions(path, q_pattern)
        except (IntegrityError, DependencyMissing) as exc:
            mapping, map_error = {}, str(exc)

    z = _open_zip(path)
    all_refs, per_part, unresolved = count_image_refs(z)
    body_refs, _, _ = count_image_refs(z, body_only=True)
    preamble = len(mapping.get(PREAMBLE, []))
    mapped = sum(len(v) for k, v in mapping.items() if k != PREAMBLE)

    verdicts = bc.image_gate_verdict(
        actual_size=os.path.getsize(path),
        expected_size=expected_size,
        unresolved=len(unresolved),
        missing_on_disk=sorted(set(per_part) - set(extracted)),
        mapped=mapped,
        preamble=preamble,
        body_refs=body_refs,
        unreadable=[k for k, v in extracted.items() if v['kind'] == 'unreadable'])

    if map_error:
        verdicts['IMG-4'] = f'FAIL document could not be read for mapping — {map_error}'

    stats = {
        'refs_all': all_refs,
        'refs_body': body_refs,
        'media_on_disk': len(extracted),
        'mapped': mapped,
        'preamble': preamble,
        'header_footer': all_refs - body_refs,
        'vector': sum(1 for v in extracted.values() if v['kind'] == 'vector'),
        'unreadable': sum(1 for v in extracted.values() if v['kind'] == 'unreadable'),
        'questions_with_images': len([k for k in mapping if k != PREAMBLE]),
        'dangling': dangling_media_targets(z),
    }
    return verdicts, stats


def figural_consistency(mapping, q_formats, figural_value='FIGURAL', overrides=()):
    """Gate IMG-5b — cross-check image presence against format classification.

    Catches two different faults with one assertion:
      * a question that HAS an image but was not classified FIGURAL  -> image was lost
        or the classifier missed it;
      * a question classified FIGURAL with NO image                  -> misclassification,
        unless it is an explicit logged override (the INHERENTLY-VISUAL path, where a
        question is visual in nature without carrying an embedded figure).

    Returns {'image_not_figural': [...], 'figural_no_image': [...]}.
    """
    ov = set(overrides)
    with_img = {k for k in mapping if k != PREAMBLE and mapping[k]}
    image_not_figural = sorted(
        q for q in with_img
        if q in q_formats and q_formats[q] != figural_value and q not in ov)
    figural_no_image = sorted(
        q for q, f in q_formats.items()
        if f == figural_value and q not in with_img and q not in ov)
    return {'image_not_figural': image_not_figural,
            'figural_no_image': figural_no_image}


def normalise_for_view(src, dest, max_edge=1600):
    """Prepare an extracted figure for view(): raster, RGB, bounded, PNG.

    Every figure measured in this corpus is a CMYK JPEG, which is not a safe input to a
    vision call. Normalising here means no caller has to remember to do it.
    """
    Image = _need('PIL')
    im = Image.open(src)
    im.load()
    if im.mode not in ('RGB', 'L'):
        im = im.convert('RGB')
    if max(im.size) > max_edge:
        r = max_edge / float(max(im.size))
        im = im.resize((max(1, int(im.size[0] * r)), max(1, int(im.size[1] * r))),
                       Image.LANCZOS)
    os.makedirs(os.path.dirname(os.path.abspath(dest)) or '.', exist_ok=True)
    im.save(dest, 'PNG', optimize=True)
    return dest


def make_vision_probe(outdir, token=None):
    """Write a liveness-probe image and return (path, token).

    The caller views the image and must read the token back. A match proves the vision
    path is live for this session; a miss means vision is UNAVAILABLE — a property of
    the session, not of any figure.

    The token is random and appears nowhere in text, so it cannot be inferred from
    context; it can only be obtained by actually seeing the image.
    """
    Image = _need('PIL')
    from PIL import ImageDraw
    import random
    import string
    token = token or ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
    os.makedirs(outdir, exist_ok=True)
    path = os.path.join(outdir, 'vision_probe.png')
    im = Image.new('RGB', (560, 180), (255, 255, 255))
    d = ImageDraw.Draw(im)
    d.rectangle([10, 10, 550, 170], outline=(0, 0, 0), width=5)
    d.text((150, 85), f'PROBE {token}', fill=(0, 0, 0))
    im.save(path, 'PNG')
    return path, token


def score_vision_probe(reported, token):
    """Compare what the caller read back against the true token. Case/space tolerant."""
    if not reported:
        return False
    return re.sub(r'\s+', '', str(reported)).upper().endswith(str(token).upper())


# ═══════════════════════════════════════════════════════════════════════════════
# CLUSTER J SHELL — SIZE GOVERNOR
# ═══════════════════════════════════════════════════════════════════════════════

def media_display_inches(path):
    """media basename -> widest display width in inches, across every story part.

    Read from each drawing's own <wp:extent cx=".."> (EMU), falling back to the VML
    style width in points.

    This is what makes downscaling CONTENT-AWARE. A figure is only over-resolved
    relative to the size it is actually displayed at: one measured figure in this corpus
    is 2546 px wide but appears 2.09 inches wide, i.e. 1216 DPI. A blanket pixel cap
    would degrade a small, correctly-sized figure while barely touching that one.
    """
    EMU_PER_INCH = 914400
    z = _open_zip(path)
    widths = {}
    for part in z.namelist():
        if not STORY_PARTS_RE.match(part):
            continue
        rels = _rels_for(z, part)
        if not rels:
            continue
        xml = z.read(part).decode('utf-8', 'ignore')
        for blk in re.findall(r'<w:drawing>.*?</w:drawing>', xml, re.S):
            cx = re.search(r'<wp:extent[^>]*\bcx="(\d+)"', blk)
            rid = re.search(r'<a:blip[^>]*r:embed="([^"]+)"', blk)
            if not (cx and rid):
                continue
            base = rels.get(rid.group(1))
            if base:
                widths[base] = max(widths.get(base, 0.0),
                                   int(cx.group(1)) / float(EMU_PER_INCH))
        for blk in re.findall(r'<w:pict>.*?</w:pict>', xml, re.S):
            rid = re.search(r'r:id="([^"]+)"', blk)
            st = re.search(r'style="[^"]*width:\s*([\d.]+)pt', blk)
            if not rid:
                continue
            base = rels.get(rid.group(1))
            if base:
                widths[base] = max(widths.get(base, 0.0),
                                   float(st.group(1)) / 72.0 if st else 0.0)
    return widths


def _is_line_art(im, sample_cap=250_000):
    """<=256 distinct colours => line art. Deterministic; work is bounded."""
    s = im.convert('RGB')
    if s.size[0] * s.size[1] > sample_cap:
        r = (sample_cap / float(s.size[0] * s.size[1])) ** 0.5
        s = s.resize((max(1, int(s.size[0] * r)), max(1, int(s.size[1] * r))))
    return len(set(s.getdata())) <= 256


def _normalise_mode(im):
    """Return (image, has_alpha) in a colour space that can actually be encoded.

    CMYK is the single largest cause of bloat in this corpus — 100% of measured figures
    were CMYK. It carries a fourth channel and is written by design tools at print
    quality with no chroma subsampling; a 544x568 diagram occupied 595 KB, about 1.9
    bytes per pixel where a correct RGB JPEG uses 0.15-0.3. Converting to RGB is
    visually lossless for screen use and is where nearly all of the reduction comes from.

    Palette ('P') and 16-bit modes are also normalised, because PIL cannot quantise or
    JPEG-encode them directly — attempting it raises "image has wrong mode".
    """
    if im.mode in ('RGBA', 'LA'):
        return im, True
    if im.mode == 'P':
        conv = im.convert('RGBA' if 'transparency' in im.info else 'RGB')
        return conv, conv.mode == 'RGBA'
    if im.mode in ('L', '1'):
        return im.convert('L'), False
    if im.mode in ('I;16', 'I', 'F'):
        return im.convert('L'), False
    return im.convert('RGB'), False


def _recode(raw, quality, dpi_ceiling, display_in):
    """Re-encode one media part. Returns (bytes, ext, how) or (None, None, why)."""
    Image = _need('PIL')
    try:
        im = Image.open(io.BytesIO(raw))
        im.load()
    except Exception:
        return None, None, 'unreadable or vector — left untouched'

    src_fmt = (im.format or '').upper()
    im, has_alpha = _normalise_mode(im)

    if dpi_ceiling and display_in and display_in > 0:
        effective_dpi = im.size[0] / float(display_in)
        if effective_dpi > dpi_ceiling:
            r = dpi_ceiling / effective_dpi
            im = im.resize((max(1, int(im.size[0] * r)), max(1, int(im.size[1] * r))),
                           Image.LANCZOS)

    route = bc.classify_media_route(
        src_fmt, has_alpha, False if has_alpha else _is_line_art(im))

    out = io.BytesIO()
    if route == 'png':
        im.save(out, 'PNG', optimize=True)
        return out.getvalue(), 'png', 'png/alpha'
    if route == 'png-lineart':
        im.convert('P', palette=Image.ADAPTIVE, colors=256).save(out, 'PNG', optimize=True)
        return out.getvalue(), 'png', 'png/lineart'
    im.save(out, 'JPEG', quality=quality, optimize=True, progressive=True, subsampling=2)
    return out.getvalue(), 'jpeg', ('jpeg/reencode' if src_fmt in ('JPEG', 'JPG')
                                    else 'jpeg/photo')


#: Extensions already carrying the right content type for each encoder route, so a
#: part using one needs no rename. Renaming gratuitously (image1.jpg -> image1.jpeg)
#: churns every relationship that references it and manufactures stem collisions that
#: would not otherwise exist.
_EXT_OK = {'jpeg': ('.jpeg', '.jpg'), 'png': ('.png',)}


def _target_media_name(name, ext):
    """Output name for one re-encoded media part. Keeps the name when the existing
    extension already maps to the encoder's content type."""
    stem, cur = os.path.splitext(name)
    if cur.lower() in _EXT_OK[ext]:
        return name
    return stem + ('.jpeg' if ext == 'jpeg' else '.png')


def _no_gain_guard(src, dst, orig, report):
    """v1.0.3 — never hand back a file LARGER than the one we were given.

    Per-PART growth is already prevented (_recode keeps the original bytes whenever a
    re-encode comes out bigger), but the ZIP CONTAINER can still grow: a package whose
    media is already optimally encoded gains nothing from re-deflation and can lose to
    the original writer's settings by a few bytes.

    Before `always` this was unreachable — a file under budget was never re-encoded at
    all — so no document-level rule was needed. It is now the normal case for small
    documents, and Framework_PYQCompress CHECK 5 treats growth as a HARD STOP, so a file
    with nothing to gain would have ABORTED THE RUN rather than simply being left alone.
    Restoring the original bytes makes "nothing to gain" a reportable outcome instead.
    """
    if os.path.getsize(dst) >= orig:
        shutil.copyfile(src, dst)
        return dict(report, bytes=orig, ratio=1.0, no_gain=True)
    return dict(report, no_gain=False)


def optimize_docx(src, dst, budget=None, force_tier=None, always=False):
    """Bring `src` under `budget` using blueprint_core's deterministic tier ladder.

    Stops at the FIRST tier that meets the budget, so the least invasive change that
    works is the one applied. On the measured corpus every paper cleared at T1, meaning
    no image was downscaled at all and every pixel dimension was preserved.

    Guarantees: never grows a part, never drops a part, never changes the part count.
    Returns (ok, report, log). ok=False means the ladder floor was reached and the file
    is STILL over budget — the caller should WARN and route to the upload lane, not halt,
    because a legitimately huge paper must not block delivery.

    The caller MUST still run assert_docx_parity(); this function does not self-certify.
    """
    budget = bc.SIZE_BUDGET if budget is None else budget
    orig = os.path.getsize(src)
    # v1.0.3 — `always` runs the ladder regardless of input size. The ladder itself needs
    # no change: a small file's T1 output is under budget, so it returns at T1, which is
    # the least invasive tier. NOTE for callers: force_tier is NOT a substitute — it pins
    # a single tier AND makes the final `return True` unconditional, so an oversized file
    # would stop at that tier, still over budget, and be reported as a success.
    if orig <= budget and not force_tier and not always:
        return True, {'tier': 'T0', 'bytes': orig, 'orig': orig, 'ratio': 1.0,
                      'quality': None, 'dpi_ceiling': None,
                      'note': 'already under budget — untouched'}, []

    display = media_display_inches(src)
    report, log = {}, []

    for tier, quality, dpi in bc.TIER_LADDER:
        if force_tier and tier != force_tier:
            continue
        zin = zipfile.ZipFile(src)
        names = zin.namelist()
        name_set = set(names)
        parts, renames, outname, log = {}, {}, {}, []

        for n in names:
            raw = zin.read(n)
            if MEDIA_RE.match(n):
                base = os.path.basename(n)
                data, ext, how = _recode(raw, quality, dpi, display.get(base, 0.0))
                if data is None or len(data) >= len(raw):
                    new, payload = n, raw                  # never grow a part
                    log.append((base, len(raw), len(raw), how + ' [kept]'))
                else:
                    new = _target_media_name(n, ext)
                    payload = data
                    log.append((base, len(raw), len(data), how))

                # v1.0.2 — a media part may NEVER overwrite another. Two parts that
                # share a stem and take the same encoder route (image1.png +
                # image1.bmp, both photographic) both want image1.jpeg; the old code
                # collapsed them into ONE zip member, so Word rendered whichever it
                # met first and the other figure was silently replaced. Every count
                # the parity assert checks — parts, media, refs — still matched, and
                # the per-stem pixel check is skipped at T2-T4, so the corrupted file
                # was delivered clean. Disambiguate instead of overwriting.
                if new in parts or (new != n and new in name_set):
                    stem, dot_ext = os.path.splitext(new)
                    k = 2
                    while (f'{stem}__c{k}{dot_ext}' in parts
                           or f'{stem}__c{k}{dot_ext}' in name_set):
                        k += 1
                    new = f'{stem}__c{k}{dot_ext}'

                parts[new] = payload
                outname[n] = new
                if os.path.basename(new) != base:
                    renames[base] = os.path.basename(new)
            else:
                parts[n] = raw
                outname[n] = n
        zin.close()

        # v1.0.2 — belt-and-braces: one member out for every member in. Catches any
        # future path that collapses two parts into one key, including a duplicate
        # member name in a damaged input package.
        if len(parts) != len(names) or len(outname) != len(names):
            raise IntegrityError(
                f'part collision in {os.path.basename(src)} at tier {tier}: '
                f'{len(names)} package member(s) in, {len(parts)} out. Two parts '
                'resolved to a single name — refusing to write a package in which '
                'one figure silently replaces another.')

        # Renaming a media part invalidates every reference to it. Rewrite the
        # relationship targets and guarantee the content-type defaults exist, or Word
        # reports the file as corrupt.
        #
        # v1.0.2 — SINGLE PASS. Sequential str.replace() chained: with renames
        # {'image1.png': 'image1.jpeg', 'image1.jpeg': 'image1__c2.jpeg'} the first
        # substitution manufactured a second 'image1.jpeg', which the second
        # substitution then rewrote as well, pointing both references at one part.
        rename_re = (re.compile('|'.join(re.escape(k) for k in
                                sorted(renames, key=len, reverse=True)))
                     if renames else None)
        for pn in list(parts):
            if pn.endswith('.rels') or pn == '[Content_Types].xml':
                txt = parts[pn].decode('utf-8')
                if rename_re is not None:
                    txt = rename_re.sub(lambda m: renames[m.group(0)], txt)
                if pn == '[Content_Types].xml':
                    for ext_, ctype in (('jpeg', 'image/jpeg'), ('png', 'image/png'),
                                        ('jpg', 'image/jpeg')):
                        if f'Extension="{ext_}"' not in txt:
                            txt = re.sub(
                                r'(<Types[^>]*>)',
                                rf'\1<Default Extension="{ext_}" ContentType="{ctype}"/>',
                                txt, count=1)
                parts[pn] = txt.encode('utf-8')

        os.makedirs(os.path.dirname(os.path.abspath(dst)) or '.', exist_ok=True)
        with zipfile.ZipFile(dst, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as zo:
            for n in names:
                # v1.0.2 — write through the explicit map built above. The previous
                # reverse-lookup guessed the output name by trying '.jpeg' then
                # '.png', which cannot express a disambiguated name and silently
                # resolved two inputs to one key.
                zo.writestr(outname[n], parts[outname[n]])

        size = os.path.getsize(dst)
        report = {'tier': tier, 'bytes': size, 'orig': orig,
                  'ratio': size / float(orig), 'quality': quality, 'dpi_ceiling': dpi}
        if size <= budget or force_tier:
            return True, _no_gain_guard(src, dst, orig, report), log

    return False, _no_gain_guard(src, dst, orig, report), log


def docx_invariants(path):
    """Every observable property that optimisation must leave untouched."""
    import hashlib
    import xml.dom.minidom as minidom
    Image = _need('PIL')

    z = _open_zip(path)
    d = _safe_document(path)
    xml = z.read('word/document.xml').decode('utf-8', 'ignore')
    media = sorted(n for n in z.namelist() if n.startswith('word/media/'))

    xmlerr = 0
    for n in z.namelist():
        if n.endswith(('.xml', '.rels')):
            try:
                minidom.parseString(z.read(n))
            except Exception:
                xmlerr += 1

    txt = '\n'.join(p.text for p in d.paragraphs)
    tbl = ''.join(c.text for t in d.tables for r in t.rows for c in r.cells)
    return {
        'parts': len(z.namelist()),
        'media': len(media),
        'paras': len(d.paragraphs),
        'tables': len(d.tables),
        'shapes': len(d.inline_shapes),
        'chars': len(txt),
        'tablechars': len(tbl),
        'omml': xml.count('<m:oMath'),
        'drawings': xml.count('<w:drawing'),
        'pict': xml.count('<w:pict'),
        'hyperlinks': xml.count('<w:hyperlink'),
        'texthash': hashlib.sha256(txt.encode()).hexdigest(),
        'refs': count_image_refs(z)[0],
        'xmlerr': xmlerr,
        'zipbad': z.testzip() or 'OK',
        'dangling': dangling_media_targets(z),
        'px': {os.path.basename(n): Image.open(io.BytesIO(z.read(n))).size
               for n in media if os.path.splitext(n)[1].lower() in RASTER_EXT},
    }


def assert_docx_parity(src, dst, allow_resample=False):
    """Raise IntegrityError unless every observable property survived optimisation.

    Deliberately includes the SHA256 of the extracted text, the OMML equation count and
    the per-image pixel dimensions.

    A governor that quietly dropped a figure would still produce a smaller, perfectly
    openable document — and because the pipeline reads question stems as TEXT, the loss
    would not announce itself anywhere downstream. Byte size and "it opens in Word" are
    not evidence of correctness.

    allow_resample=True permits pixel dimensions to change (tiers T2-T4 downscale by
    design) while still enforcing every other invariant.
    """
    before, after = docx_invariants(src), docx_invariants(dst)
    keys = ['parts', 'media', 'paras', 'tables', 'shapes', 'chars', 'tablechars',
            'omml', 'drawings', 'pict', 'hyperlinks', 'texthash', 'refs']
    failures = [f'{k}: {before[k]} -> {after[k]}' for k in keys if before[k] != after[k]]
    if after['xmlerr']:
        failures.append(f"{after['xmlerr']} malformed XML part(s)")
    if after['zipbad'] != 'OK':
        failures.append(f"corrupt zip member: {after['zipbad']}")
    if after['dangling']:
        failures.append(f"dangling relationship(s): {after['dangling'][:3]}")
    if not allow_resample:
        # v1.0.1 — the original comparison keyed on the full basename, so a legitimately
        # renamed part (image1.png -> image1.jpeg on the photo route) had no counterpart
        # in `after` and was reported as a dimension change on a document whose
        # dimensions were untouched — a FALSE-POSITIVE HARD STOP. Dormant on the
        # measured corpus, whose papers store .jpeg parts the jpeg route leaves named as
        # they were; it fired on any PNG-sourced photograph. Fixed by keying on the
        # extension-less name.
        #
        # v1.0.2 — keying on the STEM has the same defect one level up: the governor may
        # now emit a disambiguated name (image1__c2.jpeg) when two parts share a stem and
        # take the same route, which changes the stem and reproduced the identical false
        # positive. Pixel dimensions are therefore compared as an unordered MULTISET over
        # all raster parts, which is what the invariant actually asserts — "no figure's
        # pixel dimensions changed" — and is immune to any renaming the governor performs.
        b_px = sorted(before['px'].values())
        a_px = sorted(after['px'].values())
        if b_px != a_px:
            def _by_stem(px):
                out = {}
                for k, v in px.items():
                    out.setdefault(os.path.splitext(k)[0], []).append(v)
                return out

            b_stem, a_stem = _by_stem(before['px']), _by_stem(after['px'])
            named = [k for k, v in b_stem.items() if sorted(v) != sorted(a_stem.get(k, []))]
            failures.append(
                'pixel dimensions changed: '
                + (str(named[:3]) if named else f'{b_px[:3]} -> {a_px[:3]}'))
    if failures:
        raise IntegrityError(
            'Optimised document failed the parity assertion — HARD STOP.\n  '
            + '\n  '.join(failures))
    return {'before': before, 'after': after}


# ═══════════════════════════════════════════════════════════════════════════════
# CLUSTER K SHELL — ANALYSIS DOC  (the Step-2c taxonomy artefact)
# ═══════════════════════════════════════════════════════════════════════════════
# GAP-2026-07-25-002. Before this cluster the Analysis doc had FOUR independent
# readers implementing FOUR different structural conventions, and no writer at all
# (Framework_PYQAnalyse S4-2 was `pass`). Measured on the live IIT_JAM_BIOTECHNOLOGY
# doc, three of the four readers were wrong:
#
#   Framework_PYQSort S1-2          1 subject  / 26 topics / 131 subtopics  (truth 6/26/131)
#   MockTestAnalyse extract_...     1 section  /  0 subtopics
#   MockTestAnalyse _extract_..._   0 sections /  0 subtopics
#   Blueprint S2-2                  prose ("Claude extracts") — non-deterministic
#
# The first flattened every subject into the first one (a `not section_name` latch);
# the other two read doc.paragraphs while every subtopic lives in a TABLE, and keyed
# hierarchy off Word Heading styles that the generator does not emit (para.style is
# None for every paragraph of a real doc).
#
# This cluster is now THE reader, THE writer and THE verifier. Every consumer
# delegates. Heading recognition is delegated one level further, to
# blueprint_core.parse_taxonomy_level() — so all six level-1 label forms
# (Subject/Domain/Section/Part/Area) and all six level-2 forms
# (Topic/Chapter/Unit/Module/Block, numbered or colon-style, case-insensitive)
# work in EVERY step automatically, including any form the engine learns later.
#
# WHY A WRITER LIVES HERE TOO: correctness is asserted by round-trip,
# read(write(taxonomy)) == taxonomy, over a GENERATED matrix of exam shapes. The
# framework serves ~200 exams; it cannot be validated against 200 real corpora, so
# the self-test generates the shapes instead. That matrix is the correctness claim.

ANALYSIS_DOC_SUFFIX = '_PYQ_Analysis.docx'
ANALYSIS_SEARCH_DIRS = ('/mnt/project/', '/mnt/user-data/uploads/')

_NS_W = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'

# Cells that are never a subtopic name. Compared case-insensitively after strip.
# A legitimate subtopic literally named "TOTAL" would be dropped here — that is
# SAFE rather than silent, because the per-topic "Subtopics: k" declaration then
# disagrees with the parse and verify_analysis_doc() HARD STOPS naming the topic.
_SKIP_CELLS = frozenset(('subtopic', 'topic', 'grand total', 'total', ''))

# Declaration patterns. The doc states its own shape THREE times per subject; the
# reader asserts its parse against all three. This is what makes a mis-parse loud
# without needing any second artefact.
_D1_RE = re.compile(r'(\d+)\s*Topics?\b.*?\b(\d+)\s*Subtopics?', re.IGNORECASE)
_D3_RE = re.compile(r'\bSubtopics?\s*:\s*(\d+)', re.IGNORECASE)
_GRAND_RE = re.compile(r'^GRAND\s+TOTAL$', re.IGNORECASE)


class AnalysisDocError(Exception):
    """Raised for every Analysis-doc fault. Callers surface .args[0] verbatim as a
    HARD STOP: the message always names the file, the fault and the operator action."""


def _para_text(child):
    """Text of a w:p element, runs joined. docx-js splits runs on '&' and on style
    changes, so joining is mandatory — reading only the first run truncates names."""
    return ''.join(t.text for t in child.iter('{%s}t' % _NS_W) if t.text).strip()


def _table_rows(child, doc):
    from docx.table import Table as _DocxTable
    return [[c.text.strip() for c in row.cells] for row in _DocxTable(child, doc).rows]


def discover_analysis_doc(search_dirs=ANALYSIS_SEARCH_DIRS):
    """Locate the ONE Analysis doc. Returns a path; raises AnalysisDocError otherwise.

    There is exactly one conforming name, [ExamCode]_PYQ_Analysis.docx. The
    per-subject form [ExamCode]_PYQ_Analysis_[Subject].docx was retired by
    PYQAnalyse v2.6 and no project has ever held one, so it is NOT a supported
    generation — it is a nonconforming file, and it is named as such rather than
    silently ignored (a silently-ignored file is how an operator ends up sorting
    against a taxonomy they did not intend).
    """
    seen, found, nonconforming, word97 = set(), [], [], []
    for d in search_dirs:
        if not os.path.isdir(d):
            continue
        for name in sorted(os.listdir(d)):
            if name.startswith('~$') or name.startswith('.'):
                continue                      # Word lock file / hidden artefact
            low = name.lower()
            if name in seen:
                continue                      # same name in both dirs: project wins
            if low.endswith(ANALYSIS_DOC_SUFFIX.lower()):
                seen.add(name)
                found.append(os.path.join(d, name))
            elif low.endswith('.docx') and '_pyq_analysis_' in low:
                seen.add(name)
                nonconforming.append(name)
            elif low.endswith('.doc') and '_pyq_analysis' in low:
                seen.add(name)
                word97.append(name)

    if len(found) > 1:
        raise AnalysisDocError(
            "HARD STOP: %d Analysis docs found — exactly one is expected.\n"
            "  %s\n"
            "One project holds one exam. Remove the ones that do not belong to this "
            "exam and re-run." % (len(found), '\n  '.join(os.path.basename(p) for p in found)))
    if found:
        return found[0]
    if word97:
        raise AnalysisDocError(
            "HARD STOP: %s is a Word 97 .doc, which cannot be read.\n"
            "Open it in Word and Save As .docx, then upload it as %s."
            % (word97[0], '[ExamCode]' + ANALYSIS_DOC_SUFFIX))
    if nonconforming:
        raise AnalysisDocError(
            "HARD STOP: found %s, which is not the expected deliverable name.\n"
            "PYQApprove (Step 2c) produces ONE merged doc named "
            "[ExamCode]%s containing every subject. The per-subject form was retired "
            "in PYQAnalyse v2.6.\n"
            "Re-run PYQApprove and upload the doc it delivers."
            % (nonconforming[0], ANALYSIS_DOC_SUFFIX))
    raise AnalysisDocError(
        "HARD STOP: no Analysis doc found in %s.\n"
        "Expected [ExamCode]%s from PYQApprove (Step 2c).\n"
        "If the file IS in project Files, project knowledge may have stored it as "
        "extracted text rather than as the .docx package — attach the downloaded "
        ".docx to this chat as well." % (' or '.join(search_dirs), ANALYSIS_DOC_SUFFIX))


def _scan(doc_path):
    """Single pass over the body. Returns (subjects, order, declared, anomalies).

    ONE pass over doc.element.body, never doc.paragraphs, so paragraphs and tables
    are seen in true document order. The two-pass form the pre-fix readers used
    cannot attribute a table to a subject at all: by the time pass 2 runs, the
    subject boundaries from pass 1 are gone.
    """
    from docx import Document
    doc = Document(doc_path)

    subjects, order, declared, anomalies = {}, [], [], []
    cur_s = cur_t = None
    blk = None

    for child in doc.element.body:
        tag = child.tag.split('}')[-1] if '}' in child.tag else child.tag

        if tag == 'p':
            text = _para_text(child)
            if not text:
                continue
            level, name = bc.parse_taxonomy_level(text)

            if level == 1:
                cur_s, cur_t = name, None
                if cur_s not in subjects:
                    subjects[cur_s] = {}
                    order.append(cur_s)
                blk = {'subject': cur_s, 'd1': None, 'd2': [], 'd2_grand': None,
                       'd3': [], 'master_seen': False}
                declared.append(blk)
                continue

            if level == 2:
                if cur_s is None:
                    anomalies.append("topic heading %r appears before any subject "
                                     "heading" % text[:60])
                    continue
                cur_t = name
                subjects[cur_s].setdefault(cur_t, {})
                continue

            # level 3 => a decorative paragraph of the header/footer block.
            # Subtopics live in TABLES, never in paragraphs, so a level-3 paragraph
            # is never data. It may still carry a DECLARATION.
            if blk is None:
                continue
            m = _D1_RE.search(text)
            if m and blk['d1'] is None and not blk['master_seen']:
                blk['d1'] = (int(m.group(1)), int(m.group(2)))
                continue
            m = _D3_RE.search(text)
            if m and cur_t is not None:
                blk['d3'].append((cur_t, int(m.group(1))))
            continue

        if tag != 'tbl':
            continue

        rows = _table_rows(child, doc)
        data = [r for r in rows if r and r[0].strip()]
        is_master = bool(data) and any(
            bc.parse_taxonomy_level(r[0])[0] == 2 for r in data)

        if is_master:
            # MASTER SUMMARY TABLE — a declaration, never data.
            if blk is None:
                anomalies.append("a master summary table appears before any subject heading")
                continue
            blk['master_seen'] = True
            for r in data:
                lvl, tname = bc.parse_taxonomy_level(r[0])
                if lvl == 2 and len(r) >= 2 and r[1].strip().isdigit():
                    blk['d2'].append((tname, int(r[1].strip())))
                elif _GRAND_RE.match(r[0].strip()) and len(r) >= 2 and r[1].strip().isdigit():
                    blk['d2_grand'] = int(r[1].strip())
            continue

        if cur_s is None or cur_t is None:
            anomalies.append("a subtopic table at document position %d belongs to no "
                             "topic — the heading above it was not recognised"
                             % list(doc.element.body).index(child))
            continue

        bucket = subjects[cur_s][cur_t]
        for r in rows:
            if len(r) < 2:
                continue
            name = r[0].strip()
            if name.lower() in _SKIP_CELLS:
                continue
            if bc.parse_taxonomy_level(name)[0] == 2:
                continue                      # a stray topic row inside a data table
            if name not in bucket:
                bucket[name] = len(bucket)

    return subjects, order, declared, anomalies


def verify_analysis_doc(subjects, order, declared, anomalies, doc_name='Analysis doc'):
    """Assert the PARSE against the document's OWN declarations. Returns a list of
    plain-English failures; empty means the doc and the parse agree.

    The doc states its shape three times per subject:
      D1  header  "Total: — Questions | <T> Topics | <S> Subtopics"
      D2  master summary table: one row per topic (+ GRAND TOTAL)
      D3  per topic "Total PYQs: — | Subtopics: <k>"
    Nothing but a correct parse satisfies all three. This is what makes a
    mis-parse LOUD without any second artefact, on any exam, from day one.
    """
    fails = list(anomalies)
    decl_names = [b['subject'] for b in declared]

    dupes = sorted({s for s in decl_names if decl_names.count(s) > 1})
    if dupes:
        fails.append("the document declares the same subject more than once: %s — "
                     "each subject must appear exactly once" % dupes)
    if len(order) != len(declared):
        fails.append("SUBJECT COUNT: parsed %d, the document declares %d subject "
                     "heading(s) -> %s" % (len(order), len(declared), decl_names))

    for b in declared:
        s = b['subject']
        if s not in subjects:
            fails.append("[%s] declared in the document but absent from the parse" % s)
            continue
        topics = subjects[s]
        n_t = len(topics)
        n_s = sum(len(v) for v in topics.values())

        if b['d1'] and b['d1'] != (n_t, n_s):
            fails.append("[%s] header declares %d topics / %d subtopics; parsed %d / %d"
                         % (s, b['d1'][0], b['d1'][1], n_t, n_s))
        if b['d2']:
            if len(b['d2']) != n_t:
                fails.append("[%s] master summary table lists %d topics; parsed %d"
                             % (s, len(b['d2']), n_t))
            for tname, tcount in b['d2']:
                if tname not in topics:
                    fails.append("[%s] master summary lists topic %r, which is absent "
                                 "from the parse" % (s, tname))
                elif len(topics[tname]) != tcount:
                    fails.append("[%s] master summary declares %d subtopics under %r; "
                                 "parsed %d" % (s, tcount, tname, len(topics[tname])))
        if b['d2_grand'] is not None and b['d2_grand'] != n_s:
            fails.append("[%s] master summary GRAND TOTAL is %d; parsed %d"
                         % (s, b['d2_grand'], n_s))
        for tname, k in b['d3']:
            if tname in topics and len(topics[tname]) != k:
                fails.append("[%s] topic %r declares Subtopics: %d; parsed %d"
                             % (s, tname, k, len(topics[tname])))
        if not topics:
            fails.append("[%s] has no topics — an empty subject cannot be sorted "
                         "against" % s)
        for tname, subs in topics.items():
            if not subs:
                fails.append("[%s] topic %r has no subtopics" % (s, tname))

    for s in order:
        if s not in decl_names:
            fails.append("[%s] parsed but the document contains no matching subject "
                         "heading for it" % s)

    # Every name must survive the round trip through the sorted-PYQ heading parser.
    # bc.is_taxonomy_heading() rejects text at or above MAX_HEADING_LEN, so a longer
    # name stops being a heading at Step 4/5 and its questions are silently absorbed
    # by the PREVIOUS subtopic. Caught HERE, at the artefact, not four steps later.
    for s, topics in subjects.items():
        for label, value in [('subject', s)] + \
                [('topic', t) for t in topics] + \
                [('subtopic', x) for t in topics for x in topics[t]]:
            if len(value) >= bc.MAX_HEADING_LEN:
                fails.append("%s name is %d characters, at or above the %d-character "
                             "heading limit: %r. A name this long stops being "
                             "recognised as a heading in the sorted files and its "
                             "questions are silently attributed to the preceding "
                             "subtopic. Shorten it in the taxonomy and re-run "
                             "PYQApprove." % (label, len(value), bc.MAX_HEADING_LEN, value))
    return fails


def read_analysis_doc(path=None, search_dirs=ANALYSIS_SEARCH_DIRS, verify=True):
    """THE Analysis-doc reader. Returns a dict:

        {'path','exam_code','subjects','taxonomy','triples','counts','fingerprint'}

    taxonomy/triples carry exactly the shape PYQSort S1-2 has always returned, so
    downstream consumers are unchanged:
        {subject: {'subject_order': int,
                   'topics': {topic: {'topic_idx': int,
                                      'subtopics': {name: {'subtopic_idx': int}}}}}}

    topic_idx is POSITIONAL WITHIN THE SUBJECT, which is what Framework_PYQSort
    §L1111 has always specified ("position of topic within its section's Analysis
    doc"). The pre-fix code derived it from the printed "Topic N:" label, which
    restarts at 1 for every subject in a merged doc — six topics claiming index 0.
    """
    if path is None:
        path = discover_analysis_doc(search_dirs)
    base = os.path.basename(path)

    try:
        subjects, order, declared, anomalies = _scan(path)
    except AnalysisDocError:
        raise
    except Exception as ex:
        raise AnalysisDocError(
            "HARD STOP: %s could not be opened as a .docx package (%s: %s).\n"
            "Most common cause: project knowledge stored the Word document as "
            "extracted TEXT rather than as the original binary. Attach the "
            "downloaded .docx to this chat and re-run." % (base, type(ex).__name__, ex))

    if not order:
        raise AnalysisDocError(
            "HARD STOP: %s contains no subject heading.\n"
            "Expected a paragraph of the form 'Subject: <name>' (or Domain:/Section:/"
            "Part:/Area:) for each subject. Either this is not a PYQApprove Analysis "
            "doc, or the PYQAnalyse §6 HEADING FORMAT CONTRACT was violated." % base)

    if verify:
        fails = verify_analysis_doc(subjects, order, declared, anomalies, base)
        if fails:
            raise AnalysisDocError(
                "HARD STOP: %s does not agree with itself — the taxonomy parsed out of "
                "it does not match the totals the document declares. Sorting against a "
                "taxonomy that fails this check silently mis-files questions.\n  %s\n"
                "Re-run PYQApprove to regenerate the Analysis doc."
                % (base, '\n  '.join(fails[:12]) +
                   ('\n  ... and %d more' % (len(fails) - 12) if len(fails) > 12 else '')))

    taxonomy, triples = {}, []
    for subject in order:
        topics_out = {}
        for t_i, (topic, subs) in enumerate(subjects[subject].items()):
            topics_out[topic] = {
                'topic_idx': t_i,
                'subtopics': {n: {'subtopic_idx': i} for n, i in subs.items()}}
            for n in subs:
                triples.append((subject, topic, n))
        taxonomy[subject] = {'subject_order': len(taxonomy), 'topics': topics_out}

    exam_code = base[:-len(ANALYSIS_DOC_SUFFIX)] if base.endswith(ANALYSIS_DOC_SUFFIX) else None
    return {
        'path': path,
        'exam_code': exam_code,
        'subjects': list(order),
        'taxonomy': taxonomy,
        'triples': triples,
        'counts': {'subjects': len(order),
                   'topics': sum(len(v['topics']) for v in taxonomy.values()),
                   'subtopics': len(triples)},
        'fingerprint': bc.taxonomy_fingerprint(triples),
    }


def write_analysis_doc(taxonomy, exam_code, subject_order=None, out_dir='/mnt/user-data/outputs',
                       counts=None):
    """THE Analysis-doc writer (PYQAnalyse S4-2, which was `pass` until v2.24).

    taxonomy : {subject: {topic: [subtopic, ...]}}   — insertion order is preserved
    counts   : optional {(subject, topic, subtopic): int} for Phase B (--counts).
               Absent => every PYQ Count cell is an em-dash, per S4-1.

    Emits exactly the structure read_analysis_doc() contracts on, including all
    three redundant declarations. One writer + one reader + a round-trip assertion
    is the whole correctness argument; a doc this function produces is a doc that
    function reads, by construction rather than by review.
    """
    from docx import Document
    from docx.shared import Pt, RGBColor
    from docx.enum.text import WD_BREAK

    order = list(subject_order or taxonomy.keys())
    missing = [s for s in taxonomy if s not in order]
    order += missing

    over = [(lbl, v) for s in taxonomy
            for lbl, v in ([('subject', s)] +
                           [('topic', t) for t in taxonomy[s]] +
                           [('subtopic', x) for t in taxonomy[s] for x in taxonomy[s][t]])
            if len(v) >= bc.MAX_HEADING_LEN]
    if over:
        raise AnalysisDocError(
            "HARD STOP: %d taxonomy name(s) are at or above the %d-character heading "
            "limit and cannot be written — they would stop being recognised as "
            "headings in the sorted files.\n  %s"
            % (len(over), bc.MAX_HEADING_LEN,
               '\n  '.join('%s (%d chars): %r' % (l, len(v), v) for l, v in over[:5])))

    doc = Document()

    def bold(text, size):
        p = doc.add_paragraph()
        r = p.add_run(text)
        r.bold = True
        r.font.size = Pt(size)
        r.font.color.rgb = RGBColor(0x00, 0x33, 0x66)
        return p

    def cell(v):
        return '—' if v is None else str(v)

    for i, subject in enumerate(order):
        topics = taxonomy[subject]
        if i:
            doc.add_paragraph().add_run().add_break(WD_BREAK.PAGE)

        n_sub = sum(len(v) for v in topics.values())
        bold('%s — %s' % (exam_code, subject), 14)
        bold('Subject: %s' % subject, 12)                      # LEVEL 1 — §6 contract
        bold('PYQ Topic & Subtopic-wise Count', 11)
        bold('Total: %s Questions  |  %d Topics  |  %d Subtopics'      # D1
             % (cell(sum(counts.get((subject, t, x), 0)
                         for t in topics for x in topics[t]) if counts else None),
                len(topics), n_sub), 11)

        tbl = doc.add_table(rows=1, cols=3)                     # D2
        h = tbl.rows[0].cells
        h[0].text, h[1].text, h[2].text = 'Topic', 'Total Subtopics', 'Total PYQs'
        for t_i, (topic, subs) in enumerate(topics.items(), 1):
            c = tbl.add_row().cells
            c[0].text = 'Topic %d: %s' % (t_i, topic)
            c[1].text = str(len(subs))
            c[2].text = cell(sum(counts.get((subject, topic, x), 0) for x in subs)
                             if counts else None)
        c = tbl.add_row().cells
        c[0].text = 'GRAND TOTAL'
        c[1].text = str(n_sub)
        c[2].text = cell(sum(counts.get((subject, t, x), 0)
                             for t in topics for x in topics[t]) if counts else None)

        for t_i, (topic, subs) in enumerate(topics.items(), 1):
            bold('Topic %d: %s' % (t_i, topic), 12)             # LEVEL 2 — §6 contract
            bold('Total PYQs: %s  |  Subtopics: %d'             # D3
                 % (cell(sum(counts.get((subject, topic, x), 0) for x in subs)
                         if counts else None), len(subs)), 11)
            st = doc.add_table(rows=1, cols=2)
            hh = st.rows[0].cells
            hh[0].text, hh[1].text = 'Subtopic', 'PYQ Count'
            for x in subs:
                r = st.add_row().cells
                r[0].text = x
                r[1].text = cell(counts.get((subject, topic, x), 0) if counts else None)
            r = st.add_row().cells
            r[0].text = 'TOTAL'
            r[1].text = cell(sum(counts.get((subject, topic, x), 0) for x in subs)
                             if counts else None)

        bold('IFAS Edutech  —  %s %s PYQ Analysis' % (exam_code, subject), 10)

    os.makedirs(out_dir, exist_ok=True)
    out = os.path.join(out_dir, '%s%s' % (exam_code, ANALYSIS_DOC_SUFFIX))
    doc.save(out)
    return out


CK_LIVE_FIXTURE = 'IIT_JAM_BIOTECHNOLOGY_PYQ_Analysis.docx'


def _ck_shapes():
    """The exam-shape matrix. The framework serves ~200 exams and cannot be validated
    against 200 real corpora, so the shapes are GENERATED. This matrix IS the
    exam-agnostic correctness claim; it covers shapes no real exam has produced yet.
    """
    # ABSOLUTE length, never derived from bc.MAX_HEADING_LEN. Deriving it would make
    # this shape vacuous with respect to the constant: lowering the cap would shrink
    # the fixture with it and the test would stay green (INV-8, a check that measures
    # nothing). 150 characters is comfortably legal at 300 and illegal at the old 100.
    long_ok = 'Regulation of Gene Expression in Prokaryotes and Eukaryotes ' + 'x' * 90
    assert len(long_ok) == 150
    return [
        ('single subject', {'Physics': {'Mechanics': ['Kinematics', 'Newton Laws']}}),
        ('six subjects', {'S%d' % i: {'T%d' % j: ['x%d_%d' % (i, j)]
                                      for j in range(1, i + 2)} for i in range(1, 7)}),
        ('thirty subjects', {'Sub %02d' % i: {'Topic A': ['one', 'two']}
                             for i in range(1, 31)}),
        ('duplicate TOPIC name across subjects',
         {'Physics': {'Thermodynamics': ['Entropy', 'Carnot']},
          'Chemistry': {'Thermodynamics': ['Enthalpy', 'Free Energy']}}),
        ('duplicate SUBTOPIC name across topics',
         {'Biology': {'Cell': ['Introduction', 'Organelles'],
                      'Genetics': ['Introduction', 'Linkage']}}),
        ('punctuation in names',
         {'General Intelligence & Reasoning':
          {'Analogy — Verbal / Non-Verbal': ["Bloom's Taxonomy, Applied",
                                             'Ratio & Proportion']}}),
        ('unicode in names', {'\u0938\u093e\u092e\u093e\u0928\u094d\u092f \u0939\u093f\u0902\u0926\u0940':
                              {'\u0935\u094d\u092f\u093e\u0915\u0930\u0923': ['\u0938\u0902\u0927\u093f', '\u0938\u092e\u093e\u0938']}}),
        ('name at the length boundary', {'Physics': {'Mechanics': [long_ok]}}),
        ('single subtopic per topic', {'Maths': {'Algebra': ['Matrices']}}),
        ('many topics one subject',
         {'GS': {'Topic %02d' % i: ['a', 'b', 'c'] for i in range(1, 21)}}),
    ]


def _ck_selftest(check, tmp):
    """Cluster K assertions. `check(name, cond)` is the caller's harness hook."""
    import glob as _glob

    # ── the heading limit is real, and a 150-char name must survive it ─────────
    class _R:
        def __init__(self, t):
            self.text, self.bold = t, True
    class _P:
        def __init__(self, t):
            self.text, self.runs = t, [_R(t)]
    check('K MAX_HEADING_LEN admits a 150-character subtopic heading',
          bc.is_taxonomy_heading(_P('n' * 150), lambda t: False))
    check('K MAX_HEADING_LEN still rejects a pasted stem',
          not bc.is_taxonomy_heading(_P('n' * bc.MAX_HEADING_LEN), lambda t: False))

    # ── ROUND TRIP over the generated matrix ────────────────────────────────────
    for label, tax in _ck_shapes():
        d = os.path.join(tmp, 'rt_' + re.sub(r'[^a-z0-9]+', '_', label.lower()))
        os.makedirs(d, exist_ok=True)
        try:
            p = write_analysis_doc(tax, 'EXAM', out_dir=d)
            got = read_analysis_doc(p)
        except Exception as ex:
            # Report per shape instead of aborting the suite: when this cluster
            # regresses, the operator needs to see WHICH shapes broke, not just the
            # first one.
            for suffix in ('round-trip', 'subject order', 'counts', 'topic_idx positional'):
                check('K %s: %s [%s]' % (suffix, label, type(ex).__name__), False)
            continue
        rebuilt = {s: {t: list(v['subtopics']) for t, v in d2['topics'].items()}
                   for s, d2 in got['taxonomy'].items()}
        check('K round-trip: ' + label, rebuilt == tax)
        check('K subject order: ' + label, got['subjects'] == list(tax))
        n = sum(len(x) for t in tax.values() for x in t.values())
        check('K counts: ' + label,
              got['counts'] == {'subjects': len(tax),
                                'topics': sum(len(t) for t in tax.values()),
                                'subtopics': n})
        # topic_idx must be contiguous 0..n-1 WITHIN each subject and never collide
        ok = all(sorted(v['topic_idx'] for v in d2['topics'].values())
                 == list(range(len(d2['topics']))) for d2 in got['taxonomy'].values())
        check('K topic_idx positional: ' + label, ok)

    # ── every level-1 and level-2 label form the engine blesses ─────────────────
    tax = {'Alpha': {'Beta': ['gamma', 'delta']}}
    d = os.path.join(tmp, 'labels'); os.makedirs(d, exist_ok=True)
    src = write_analysis_doc(tax, 'EXAM', out_dir=d)
    from docx import Document as _D
    for l1 in ('Subject', 'Domain', 'Section', 'Part', 'Area'):
        for l2 in ('Topic 1', 'Chapter 1', 'Unit 1', 'Module 1', 'Block 1'):
            doc = _D(src)
            for para in doc.paragraphs:
                t = para.text.strip()
                if t.startswith('Subject:'):
                    para.runs[0].text = '%s: Alpha' % l1
                elif t.startswith('Topic 1:'):
                    para.runs[0].text = '%s: Beta' % l2
            alt = os.path.join(d, 'ALT%s' % ANALYSIS_DOC_SUFFIX)
            doc.save(alt)
            # the master-summary rows still say "Topic 1:", which is level 2 either way
            got = read_analysis_doc(alt, verify=False)
            check('K label form %s / %s' % (l1, l2),
                  got['subjects'] == ['Alpha']
                  and list(got['taxonomy']['Alpha']['topics']) == ['Beta'])

    # ── the self-check must FIRE on each corruption, not just pass on good input ─
    def _mutate(fn, name):
        d2 = os.path.join(tmp, 'mut_' + name); os.makedirs(d2, exist_ok=True)
        p = write_analysis_doc({'Physics': {'Mechanics': ['Kinematics', 'Newton Laws']},
                                'Chemistry': {'Bonding': ['Ionic']}}, 'EXAM', out_dir=d2)
        doc = _D(p)
        fn(doc)
        doc.save(p)
        try:
            read_analysis_doc(p)
            return False
        except AnalysisDocError:
            return True

    def drop_subject_line(doc):
        for para in doc.paragraphs:
            if para.text.strip() == 'Subject: Chemistry':
                para.runs[0].text = 'Chemistry notes'
                return

    def dup_subject(doc):
        for para in doc.paragraphs:
            if para.text.strip() == 'Subject: Chemistry':
                para.runs[0].text = 'Subject: Physics'
                return

    def wrong_declared_count(doc):
        for para in doc.paragraphs:
            if para.text.strip().startswith('Total PYQs:'):
                para.runs[0].text = 'Total PYQs: —  |  Subtopics: 7'
                return

    def wrong_grand_total(doc):
        for tbl in doc.tables:
            for row in tbl.rows:
                if row.cells[0].text.strip() == 'GRAND TOTAL':
                    row.cells[1].text = '99'
                    return

    def drop_a_subtopic_row(doc):
        for tbl in doc.tables:
            for row in tbl.rows:
                if row.cells[0].text.strip() == 'Newton Laws':
                    row.cells[0].text = ''
                    return

    check('K catches a missing subject heading', _mutate(drop_subject_line, 'dropsubj'))
    check('K catches a duplicated subject', _mutate(dup_subject, 'dupsubj'))
    check('K catches a wrong declared subtopic count', _mutate(wrong_declared_count, 'badcount'))
    check('K catches a wrong GRAND TOTAL', _mutate(wrong_grand_total, 'badgrand'))
    check('K catches a dropped subtopic row', _mutate(drop_a_subtopic_row, 'droprow'))

    # ── name length is refused at the PRODUCER, not discovered downstream ───────
    too_long = 'y' * bc.MAX_HEADING_LEN
    d3 = os.path.join(tmp, 'toolong'); os.makedirs(d3, exist_ok=True)
    try:
        write_analysis_doc({'Physics': {'Mechanics': [too_long]}}, 'EXAM', out_dir=d3)
        check('K refuses to write an over-length name', False)
    except AnalysisDocError:
        check('K refuses to write an over-length name', True)

    # ── discovery ──────────────────────────────────────────────────────────────
    dd = os.path.join(tmp, 'disc'); os.makedirs(dd, exist_ok=True)
    up = os.path.join(tmp, 'disc_up'); os.makedirs(up, exist_ok=True)
    dirs = (dd + os.sep, up + os.sep)

    def _clear():
        for d4 in (dd, up):
            for f in _glob.glob(os.path.join(d4, '*')):
                os.remove(f)

    def _raises(sub):
        try:
            discover_analysis_doc(dirs)
            return False
        except AnalysisDocError as ex:
            return sub in str(ex)

    _clear()
    check('K no doc -> named stop', _raises('no Analysis doc found'))

    _clear()
    open(os.path.join(dd, '~$EXAM' + ANALYSIS_DOC_SUFFIX), 'w').close()
    check('K ignores a Word lock file', _raises('no Analysis doc found'))

    _clear()
    open(os.path.join(dd, 'EXAM_PYQ_Analysis.doc'), 'w').close()
    check('K names the Word 97 .doc case', _raises('Word 97'))

    _clear()
    open(os.path.join(dd, 'EXAM_PYQ_Analysis_Physics.docx'), 'w').close()
    check('K names the retired per-subject form', _raises('not the expected deliverable name'))

    _clear()
    open(os.path.join(dd, 'A' + ANALYSIS_DOC_SUFFIX), 'w').close()
    open(os.path.join(dd, 'B' + ANALYSIS_DOC_SUFFIX), 'w').close()
    check('K stops on two Analysis docs', _raises('exactly one is expected'))

    _clear()
    write_analysis_doc({'Physics': {'Mechanics': ['Kinematics']}}, 'EXAM', out_dir=dd)
    write_analysis_doc({'Physics': {'Mechanics': ['DIFFERENT']}}, 'EXAM', out_dir=up)
    got = read_analysis_doc(search_dirs=dirs)
    check('K same name in both dirs -> project wins, loaded once',
          got['triples'] == [('Physics', 'Mechanics', 'Kinematics')])

    # ── fingerprint ────────────────────────────────────────────────────────────
    a = read_analysis_doc(os.path.join(dd, 'EXAM' + ANALYSIS_DOC_SUFFIX))
    b = read_analysis_doc(os.path.join(up, 'EXAM' + ANALYSIS_DOC_SUFFIX))
    check('K fingerprint distinguishes different taxonomies',
          a['fingerprint'] != b['fingerprint'])
    check('K fingerprint is stable across reads',
          a['fingerprint'] == read_analysis_doc(a['path'])['fingerprint'])

    # ── the live fixture: the one shape that is field evidence, not generated ───
    fx = None
    for cand in (os.path.join(os.path.dirname(os.path.abspath(__file__)), CK_LIVE_FIXTURE),
                 os.path.join('fixtures', CK_LIVE_FIXTURE), CK_LIVE_FIXTURE):
        if os.path.exists(cand):
            fx = cand
            break
    if fx:
        live = read_analysis_doc(fx)
        check('K live fixture: 6 subjects / 26 topics / 131 subtopics',
              live['counts'] == {'subjects': 6, 'topics': 26, 'subtopics': 131})
        check('K live fixture: 6 distinct subjects across the triples',
              len({t[0] for t in live['triples']}) == 6)


# ═══════════════════════════════════════════════════════════════════════════════
# SELF-TEST
# ═══════════════════════════════════════════════════════════════════════════════

def self_test():
    passed = total = 0
    fails = []

    def check(name, cond):
        nonlocal passed, total
        total += 1
        if cond:
            passed += 1
        else:
            fails.append(name)

    # ── folder id parsing ────────────────────────────────────────────────────
    check('io_folder_url', parse_drive_folder_id(
        'https://drive.google.com/drive/folders/13sdlvaEJjwLKmsvP-zdCpv4l4GhZbF9s')
        == '13sdlvaEJjwLKmsvP-zdCpv4l4GhZbF9s')
    check('io_folder_url_u0', parse_drive_folder_id(
        'https://drive.google.com/drive/u/0/folders/ABC123defGHI') == 'ABC123defGHI')
    check('io_folder_bare_id', parse_drive_folder_id('13sdlvaEJjwLKmsvP') == '13sdlvaEJjwLKmsvP')
    check('io_folder_none', parse_drive_folder_id('not a link') is None)

    # ── listing normalisation ────────────────────────────────────────────────
    raw = [{'id': '1', 'title': 'a.docx', 'mimeType': bc.DOCX_MIME, 'fileSize': '12694409'},
           {'id': '2', 'name': 'b.docx', 'mimeType': bc.DOCX_MIME, 'size': 100},
           {'id': '3', 'title': 'yr', 'mimeType': bc.FOLDER_MIME}]
    norm = normalise_drive_listing(raw)
    check('io_norm_size_str_to_int', norm[0]['fileSize'] == 12694409)
    check('io_norm_name_alias', norm[1]['name'] == 'b.docx')
    check('io_norm_missing_size_none', norm[2]['fileSize'] is None)
    check('io_norm_envelope', len(normalise_drive_listing({'files': raw})) == 3)
    check('io_norm_empty', normalise_drive_listing([]) == [])
    check('io_norm_junk_skipped', len(normalise_drive_listing(['junk', None])) == 0)

    # ── enumeration: rejects, duplicates, pagination, recursion ──────────────
    tree = {
        'root': {'items': [
            {'id': 'f1', 'title': '2010.docx', 'mimeType': bc.DOCX_MIME, 'fileSize': '900'},
            {'id': 'f2', 'title': 'old.doc', 'mimeType': 'application/msword', 'fileSize': '9'},
            {'id': 'f3', 'title': 'native', 'mimeType': bc.GDOC_MIME},
            {'id': 'sub', 'title': '2011', 'mimeType': bc.FOLDER_MIME}]},
        'sub': {'items': [
            {'id': 'f4', 'title': '2011.docx', 'mimeType': bc.DOCX_MIME, 'fileSize': '800'}]},
    }

    def fake_list(fid, page_token=None):
        return tree[fid]

    papers, rejects = collect_corpus_files(fake_list, 'root')
    check('io_enum_finds_nested', len(papers) == 2)
    check('io_enum_rejects_both', len(rejects) == 2)
    check('io_enum_reject_has_reason', all(r['reason'] for r in rejects))
    check('io_enum_size_captured', papers[0]['fileSize'] == 900)
    check('io_enum_key_present', 'paper_key' in papers[0])

    def fake_dup(fid, page_token=None):
        return {'items': [
            {'id': 'a', 'title': 'X_2010.docx', 'mimeType': bc.DOCX_MIME, 'fileSize': '1'},
            {'id': 'b', 'title': 'X_2010 (1).docx', 'mimeType': bc.DOCX_MIME, 'fileSize': '2'}]}
    try:
        collect_corpus_files(fake_dup, 'root')
        check('io_enum_duplicate_hard_stop', False)
    except DuplicatePaperError as exc:
        check('io_enum_duplicate_hard_stop', 'X_2010' in str(exc))

    pages = [{'items': [{'id': 'p1', 'title': 'a.docx', 'mimeType': bc.DOCX_MIME,
                         'fileSize': '1'}], 'nextPageToken': 'T'},
             {'items': [{'id': 'p2', 'title': 'b.docx', 'mimeType': bc.DOCX_MIME,
                         'fileSize': '1'}]}]

    def fake_paged(fid, page_token=None):
        return pages[1] if page_token else pages[0]

    check('io_enum_paginates', len(collect_corpus_files(fake_paged, 'r')[0]) == 2)

    # ── payload decoding: every documented shape ─────────────────────────────
    payload = base64.b64encode(b'PK\x03\x04hello').decode()
    inner = json.dumps({'id': 'x', 'title': 't', 'mimeType': 'm', 'content': payload})
    check('io_decode_raw_bytes', decode_drive_payload(b'PK\x03\x04') == b'PK\x03\x04')
    check('io_decode_inner_json', decode_drive_payload(inner) == b'PK\x03\x04hello')
    check('io_decode_spill_shape',
          decode_drive_payload([{'text': inner, 'type': 'text'}]) == b'PK\x03\x04hello')
    check('io_decode_dict', decode_drive_payload({'content': payload}) == b'PK\x03\x04hello')
    spill = '/tmp/_ci_spill.json'
    with open(spill, 'w') as fh:
        json.dump([{'text': inner, 'type': 'text'}], fh)
    check('io_decode_spill_path', decode_drive_payload(spill) == b'PK\x03\x04hello')
    for bad, label in [([], 'empty_list'), ('nonsense', 'garbage'), ({'k': 1}, 'no_content')]:
        try:
            decode_drive_payload(bad)
            check(f'io_decode_reject_{label}', False)
        except TransportFallback:
            check(f'io_decode_reject_{label}', True)

    # ── download verification ────────────────────────────────────────────────
    check('io_verify_ok', verify_downloaded_bytes(b'PK\x03\x04abc', 7))
    for args, label in [((b'', None), 'empty'), ((b'<html>', None), 'not_docx'),
                        ((b'PK\x03\x04abc', 99), 'truncated')]:
        try:
            verify_downloaded_bytes(*args)
            check(f'io_verify_reject_{label}', False)
        except TransportFallback:
            check(f'io_verify_reject_{label}', True)

    # ── fetch: EVERY failure degrades, never SystemExit ──────────────────────
    def boom(_):
        raise RuntimeError('connector exploded')
    try:
        fetch_drive_docx(boom, {'id': 'x', 'name': 'n.docx', 'fileSize': 10}, '/tmp/ci')
        check('io_fetch_error_is_fallback', False)
    except TransportFallback:
        check('io_fetch_error_is_fallback', True)
    except Exception:
        check('io_fetch_error_is_fallback', False)
    try:
        fetch_drive_docx(boom, {'id': 'x', 'name': 'big.docx',
                                'fileSize': bc.DRIVE_CAP + 1}, '/tmp/ci')
        check('io_fetch_oversize_not_attempted', False)
    except TransportFallback as exc:
        check('io_fetch_oversize_not_attempted', 'without attempting' in str(exc))

    def good(_):
        return base64.b64encode(b'PK\x03\x04data').decode()
    p = fetch_drive_docx(lambda i: json.dumps({'content': good(i)}),
                         {'id': 'x', 'name': 'ok.docx', 'fileSize': 8}, '/tmp/ci_ok')
    check('io_fetch_writes_file', os.path.exists(p) and os.path.getsize(p) == 8)

    # ── upload resolution: identity, not filename, not recency ──────────────
    up = '/tmp/ci_uploads'
    os.makedirs(up, exist_ok=True)
    for f in os.listdir(up):
        os.remove(os.path.join(up, f))
    for fn in ['E_02-May-2010_Sorted (1).docx', 'E_2011_Sorted.docx',
               'Unrelated_2099.docx', '~$lock.docx']:
        open(os.path.join(up, fn), 'w').write('x')
    want = [bc.canonical_paper_key('E_02May2010_Sorted.docx'),
            bc.canonical_paper_key('E_2012_Sorted.docx')]
    res = resolve_uploaded_papers(want, up)
    check('io_upload_matches_through_suffix', len(res['matched']) == 1)
    check('io_upload_reports_missing',
          res['missing'] == [bc.canonical_paper_key('E_2012_Sorted.docx')])
    check('io_upload_flags_unexpected', len(res['unexpected']) == 2)
    check('io_upload_ignores_lockfiles',
          not any('~$' in p for p in res['unexpected']))
    check('io_upload_missing_dir_safe',
          resolve_uploaded_papers(['k'], '/tmp/does_not_exist')['missing'] == ['k'])

    # ── vision probe ─────────────────────────────────────────────────────────
    check('io_probe_scores_exact', score_vision_probe('ABC12345', 'ABC12345'))
    check('io_probe_scores_prefixed', score_vision_probe('PROBE ABC12345', 'ABC12345'))
    check('io_probe_lowercase', score_vision_probe('probe abc12345', 'ABC12345'))
    check('io_probe_rejects_wrong', not score_vision_probe('ZZZZZZZZ', 'ABC12345'))
    check('io_probe_rejects_empty', not score_vision_probe('', 'ABC12345'))
    check('io_probe_rejects_none', not score_vision_probe(None, 'ABC12345'))

    # ── figural cross-check ──────────────────────────────────────────────────
    mp = {1: ['i1.png'], 5: ['i2.png'], PREAMBLE: ['i0.png']}
    fc = figural_consistency(mp, {1: 'FIGURAL', 5: 'TEXT', 9: 'FIGURAL'})
    check('io_figural_flags_image_not_figural', fc['image_not_figural'] == [5])
    check('io_figural_flags_figural_no_image', fc['figural_no_image'] == [9])
    check('io_figural_preamble_ignored', 'preamble' not in str(fc))
    fc2 = figural_consistency(mp, {1: 'FIGURAL', 5: 'TEXT', 9: 'FIGURAL'}, overrides=(5, 9))
    check('io_figural_overrides_respected',
          not fc2['image_not_figural'] and not fc2['figural_no_image'])

    # ── structural corruption must ALWAYS surface as a NAMED gate ────────────
    # Regression guard: python-docx raises a bare KeyError and zipfile a bare
    # BadZipFile from deep inside their readers. Both previously escaped as raw
    # tracebacks instead of gate verdicts. Found by adversarial mutation testing.
    _bad = '/tmp/_ci_badzip.docx'
    with open(_bad, 'wb') as _fh:
        _fh.write(b'PK\x03\x04' + b'\x00' * 400)
    for _label, _fn in (
            ('refs', lambda: count_image_refs(_bad)),
            ('extract', lambda: extract_images(_bad, '/tmp/_ci_badx')),
            ('display', lambda: media_display_inches(_bad)),
            ('governor', lambda: optimize_docx(_bad, '/tmp/_ci_o.docx', 1)),
            ('invariants', lambda: docx_invariants(_bad))):
        try:
            _fn()
            check(f'io_corrupt_named_{_label}', False)
        except IntegrityError:
            check(f'io_corrupt_named_{_label}', True)
        except Exception:
            check(f'io_corrupt_named_{_label}', False)

    _missing_ok = True
    try:
        _safe_document(_bad)
        _missing_ok = False
    except IntegrityError:
        pass
    except Exception:
        _missing_ok = False
    check('io_safe_document_named', _missing_ok)

    # ── v1.0.1 parity must not fire on a legitimate rename ───────────────────
    _pdir = f'/tmp/corpus_io_parity/{os.getpid()}'
    os.makedirs(_pdir, exist_ok=True)
    try:
        import random as _rnd
        from PIL import Image as _Im
        import docx as _dx
        _rnd.seed(11)
        _png = os.path.join(_pdir, 'photo.png')
        _im = _Im.new('RGB', (600, 400))
        _im.putdata([(_rnd.randrange(256), _rnd.randrange(256), _rnd.randrange(256))
                     for _ in range(600 * 400)])
        _im.save(_png)                      # PNG source -> jpeg route -> RENAME
        _d = _dx.Document()
        _d.add_paragraph('Q.1 figure').add_run().add_picture(_png)
        _src = os.path.join(_pdir, 'src.docx')
        _dst = os.path.join(_pdir, 'dst.docx')
        _d.save(_src)
        _ok, _rep, _log = optimize_docx(_src, _dst, budget=os.path.getsize(_src) // 2)
        check('io_parity_rename_engaged', _rep['tier'] == 'T1')
        _renamed = ('word/media/photo.png' not in zipfile.ZipFile(_dst).namelist())
        check('io_parity_rename_happened', _renamed)
        _before = docx_invariants(_src)['px']
        _after = docx_invariants(_dst)['px']
        check('io_parity_rename_dims_unchanged',
              sorted(_before.values()) == sorted(_after.values()))
        try:
            assert_docx_parity(_src, _dst, allow_resample=False)
            check('io_parity_rename_no_false_stop', True)
        except IntegrityError:
            check('io_parity_rename_no_false_stop', False)
        # and a REAL dimension change must still be caught
        _ok2, _rep2, _ = optimize_docx(_src, _dst, budget=1, force_tier='T4')
        _shrunk = docx_invariants(_dst)['px']
        if sorted(_shrunk.values()) != sorted(_before.values()):
            try:
                assert_docx_parity(_src, _dst, allow_resample=False)
                check('io_parity_real_resize_still_caught', False)
            except IntegrityError:
                check('io_parity_real_resize_still_caught', True)
            check('io_parity_real_resize_allowed_when_permitted',
                  bool(assert_docx_parity(_src, _dst, allow_resample=True)))
    except DependencyMissing:
        pass                                # optional deps absent — nothing to assert

    # ── CLUSTER K — ANALYSIS DOC (GAP-2026-07-25-002) ──────────────────────
    import tempfile as _tf
    with _tf.TemporaryDirectory() as _tmp:
        _ck_selftest(check, _tmp)

    print(f"SELF-TEST: {passed}/{total} PASS")
    if fails:
        print('FAILED: ' + ', '.join(fails))
    return passed == total


if __name__ == '__main__':
    import sys
    if '--self-test' in sys.argv:
        sys.exit(0 if self_test() else 1)
    print('corpus_io.py — corpus acquisition / image integrity / size governor. '
          'Run with --self-test.')
