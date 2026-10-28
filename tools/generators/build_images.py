#!/usr/bin/env python3
"""Merge the 600-image licensed register into content/assets.json and public/assets/img.
Usage: python3 -I tools/generators/build_images.py <register.csv> <unzipped_webp_root> <repo>
Keeps existing audio entries; replaces image entries. Licences are those recorded in the register (all CC0/PD/CC BY/CC BY-SA)."""
import csv, json, os, shutil, sys
from PIL import Image
reg, root, repo = sys.argv[1:4]
rows = list(csv.DictReader(open(reg, encoding="utf8")))
cur = json.load(open(f"{repo}/content/assets.json", encoding="utf8"))
audio = [a for a in cur["items"] if a["kind"] != "image"]
out = f"{repo}/public/assets/img"; os.makedirs(out, exist_ok=True)
byid = {}
for d, _, fs in os.walk(root):
    for f in fs:
        if f.endswith(".webp"): byid[f.split("_", 1)[0]] = os.path.join(d, f)
items, missing = [], []
for r in rows:
    p = byid.get(r["asset_id"])
    if not p: missing.append(r["asset_id"]); continue
    shutil.copyfile(p, f"{out}/{r['asset_id']}.webp")
    w, h = Image.open(p).size
    folder = r["path"].split("/images/")[-1].split("/")[0]
    items.append({"id": r["asset_id"], "kind": "image", "file": f"/assets/img/{r['asset_id']}.webp", "title": r["title"], "creator": r["creator"],
        "date": r["date"] or None, "institution": r["institution"] or None, "source": r["source_page_url"], "license": r["license"],
        "attribution": r["attribution_text"], "use": r["intended_use"], "w": w, "h": h, "tags": [t for t in r["tags"].split(";") if t and ":" not in t][:8],
        "collection": folder, "modified": "نسخة مصغّرة بصيغة WebP؛ لم يُعدَّل المحتوى"})
for it in items:
    for k in [k for k, v in it.items() if v is None]: del it[k]
cur["items"] = items + audio
cur["note"] = "Every item is CC0, public domain, CC BY or CC BY-SA per the library register; attribution shown on /credits. CC BY-SA images are resized copies and stay under their own licence."
json.dump(cur, open(f"{repo}/content/assets.json", "w", encoding="utf8"), ensure_ascii=False, indent=1)
print("images", len(items), "missing", missing, "audio kept", len(audio))
