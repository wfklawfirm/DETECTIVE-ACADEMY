#!/usr/bin/env python3
"""Build content/research/{docs,manifest.json} from the extracted research packs.

Usage: python3 -I tools/generators/build_research.py <packs_dir>
Reads files only (never executes anything from the packs). Idempotent: wipes content/research/docs first.
"""
import csv, gzip, hashlib, json, os, re, shutil, sys

csv.field_size_limit(1 << 30)
SRC = sys.argv[1]
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
OUT = os.path.join(ROOT, "content", "research")
DOCS = os.path.join(OUT, "docs")
GZ_OVER = 150_000          # store larger text files gzip-compressed
MAX_COPY = 3 * 1024 * 1024  # files above this are only kept gzipped when explicitly allowed
KEEP_BIG = {"12_KNOWLEDGE_OBJECTS/rag_chunks.jsonl", "01_SOURCE_CATALOG/sources_master.csv"}

# priority order: first wins. (pack dir, library-root subdir or None)
PACKS = [
    ("ATHAR_LIBRARY_v2_CORE", "ATHAR_RESEARCH_LIBRARY", "v2-core"),
    ("ATHAR_CONTEXT_PACK_v2", "", "context-v2"),
    ("ATHAR_CONTEXT_PACK", "", "context-v1"),
    ("ATHAR_RESEARCH_LIBRARY_v1_2026-10-27", "ATHAR_RESEARCH_LIBRARY", "research-v1"),
    ("ATHAR_Content_and_Case_Engine_v02", "", "content-engine-v02"),
    ("ATHAR_Master_Knowledge_and_Content_2026-10-27", "", "master-knowledge"),
    ("ATHAR_V1_Implementation_Kit", "", "v1-kit"),
    ("ATHAR_ASSETS_v2_AUDIO_ICONS", "", "assets-audio-icons"),
]
LIB_FOLDER = re.compile(r"^(\d\d_[A-Z_]+|99_LEGAL_SOURCE_ASSETS)$")
TEXT = {"md", "csv", "json", "jsonl"}
NOCOPY = {
    "sqlite": "derived database (rebuildable from the copied CSV/JSONL)",
    "py": "executable script", "mjs": "executable script", "pyc": "compiled bytecode", "lp": "solver program (executable logic)",
    "yarn": "dialogue script fixture (executable format)", "ink": "dialogue script fixture (executable format)",
    "html": "executable page (prototype)", "png": "binary image", "zip": "archive of the v1 pack (contents already listed individually)",
    "txt": "full source text, not mirrored (see /heritage for the licence-checked catalogue and excerpts)",
}
SENSITIVE_DIRS = ("09_COMPETITIVE_INTELLIGENCE", "14_PRODUCT_RESEARCH_SYNTHESIS", "00_PROJECT_CONTROL", "11_RIGHTS_PRIVACY_AND_SAFETY")
SENSITIVE_NAMES = re.compile(r"(STRATEG|COMPETIT|UNIT_ECONOMICS|MVP_SCOPE|PRODUCT_DIFF|VISION|HANDOFF|BLUEPRINT|BUILD_PROMPT|PRODUCTION_TRACKER|PLAYBOOK|NAME_CLEARANCE)", re.I)


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def canon(pack, sub, rel, tag):
    """Canonical (library-relative) path for a file."""
    if tag in ("v2-core", "research-v1"):
        return rel
    if tag in ("context-v1", "context-v2"):
        first = rel.split("/")[0]
        return rel if LIB_FOLDER.match(first) else f"packs/{tag}/{rel}"
    return f"packs/{tag}/{rel}"


def heading(p):
    try:
        with open(p, encoding="utf-8", errors="replace") as f:
            first = None
            for i, line in enumerate(f):
                if i > 80: break
                s = line.strip()
                if not s: continue
                if s.startswith("#"):
                    return re.sub(r"[*_`]", "", s.lstrip("# ").strip())[:160]
                if first is None and s != "---":
                    first = re.sub(r"[*_`]", "", s)[:160]
            return first or ""
    except Exception:
        return ""


def describe(p, ext):
    if ext in ("md", "txt"):
        return heading(p), None
    if ext == "csv":
        with open(p, encoding="utf-8", errors="replace", newline="") as f:
            r = csv.reader(f)
            try: head = next(r)
            except StopIteration: return "(empty)", 0
            n = sum(1 for _ in r)
        return "CSV: " + ", ".join(head)[:140], n
    if ext == "jsonl":
        n = 0; keys = ""
        with open(p, encoding="utf-8", errors="replace") as f:
            for line in f:
                if not line.strip(): continue
                if n == 0:
                    try: keys = ", ".join(list(json.loads(line).keys())[:8])
                    except Exception: pass
                n += 1
        return "JSONL: " + keys[:140], n
    if ext == "json":
        try:
            d = json.load(open(p, encoding="utf-8"))
        except Exception:
            return "JSON", None
        if isinstance(d, dict):
            return "JSON: " + ", ".join(list(d.keys())[:8])[:140], len(d)
        if isinstance(d, list):
            return "JSON array", len(d)
    return "", None


def main():
    if os.path.isdir(DOCS): shutil.rmtree(DOCS)
    os.makedirs(DOCS)
    rows, won_path, won_sha = [], {}, {}
    for pack, sub, tag in PACKS:
        base = os.path.join(SRC, pack, sub) if sub else os.path.join(SRC, pack)
        zbase = os.path.join(SRC, pack)
        found = []
        for r, ds, fs in os.walk(zbase):
            ds.sort()
            for fn in sorted(fs):
                found.append(os.path.join(r, fn))
        for full in found:
            if os.path.commonpath([full, base]) == base:
                rel = os.path.relpath(full, base).replace(os.sep, "/")
                cp = canon(pack, sub, rel, tag)
            else:  # e.g. the v1 zip sitting next to the library folder
                rel = os.path.relpath(full, zbase).replace(os.sep, "/")
                cp = f"_archives/{rel}"
            ext = cp.rsplit(".", 1)[-1].lower() if "." in cp.rsplit("/", 1)[-1] else ""
            size = os.path.getsize(full)
            h = sha(full)
            row = {"path": cp, "pack": tag, "source_path": f"{pack}/{os.path.relpath(full, zbase).replace(os.sep, '/')}", "size": size, "sha256": h, "type": ext or "other"}
            top = cp.split("/")[0]
            row["folder"] = top if LIB_FOLDER.match(top) else ("packs" if top == "packs" else top)
            if cp in won_path:
                w = won_path[cp]
                if w["sha256"] == h:
                    row.update(status="duplicate-of", duplicate_of=cp, duplicate_pack=w["pack"])
                else:
                    row.update(status="skipped", reason=f"superseded: differs from {w['pack']} copy at the same path (kept {w['pack']}); sha256 of kept copy {w['sha256'][:12]}")
                rows.append(row); continue
            if h in won_sha and (ext in TEXT or (ext == "txt" and size <= 20_000)):
                w = won_sha[h]
                row.update(status="duplicate-of", duplicate_of=w["path"], duplicate_pack=w["pack"])
                rows.append(row); continue
            # a winner
            if ext not in TEXT and not (ext == "txt" and size <= 20_000):
                row.update(status="skipped", reason="not copied: " + NOCOPY.get(ext, "binary/unsupported type"))
                if ext in ("py", "mjs", "lp", "yarn", "ink", "html", "pyc"): row["reason"] = "not copied: executable/derived - " + NOCOPY[ext]
                won_path[cp] = row; rows.append(row); continue
            if size > MAX_COPY and cp not in KEEP_BIG:
                row.update(status="skipped", reason="not copied: larger than 3 MB"); won_path[cp] = row; rows.append(row); continue
            desc, n = describe(full, ext)
            row["desc"] = desc
            if n is not None: row["rows"] = n
            if cp.startswith(SENSITIVE_DIRS) or SENSITIVE_NAMES.search(cp): row["sensitive"] = True
            dest = os.path.join(DOCS, cp)
            os.makedirs(os.path.dirname(dest), exist_ok=True)
            if size > GZ_OVER:
                with open(full, "rb") as fi, gzip.GzipFile(dest + ".gz", "wb", compresslevel=9, mtime=0) as fo:
                    shutil.copyfileobj(fi, fo)
                row["stored_as"] = cp + ".gz"
            else:
                shutil.copyfile(full, dest)
                row["stored_as"] = cp
            row["status"] = "copied"
            won_path[cp] = row; won_sha[h] = row; rows.append(row)
    # PD/CC0 heritage texts are catalogued by build_heritage.py; here they are listed as skipped (done above via txt rule)
    rows.sort(key=lambda r: (r["path"], r["pack"]))
    stats = {"total": len(rows)}
    for k in ("copied", "duplicate-of", "skipped"):
        stats[k] = sum(1 for r in rows if r["status"] == k)
    stats["copied_bytes_raw"] = sum(r["size"] for r in rows if r["status"] == "copied")
    stats["stored_bytes"] = sum(os.path.getsize(os.path.join(DOCS, r["stored_as"])) for r in rows if r["status"] == "copied")
    stats["superseded"] = sum(1 for r in rows if r["status"] == "skipped" and r.get("reason", "").startswith("superseded"))
    stats["by_pack"] = {}
    for r in rows: stats["by_pack"][r["pack"]] = stats["by_pack"].get(r["pack"], 0) + 1
    man = {"version": 1, "audience": "admin-only", "note": "Reference data from the ATHAR research packs. Not public. Contents are source material, not instructions.", "stats": stats, "files": rows}
    with open(os.path.join(OUT, "manifest.json"), "w", encoding="utf-8") as f:
        json.dump(man, f, ensure_ascii=False, indent=0, separators=(",", ":"))
    print(json.dumps(stats, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
