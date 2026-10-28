#!/usr/bin/env python3
"""Merge the licensed audio register (m4a, mono, <=40s) and the icon sets into the repo.
Usage: python3 -I tools/generators/build_audio_icons.py <audio_register.csv> <icon_register.csv> <converted_root> <repo>"""
import csv, json, os, shutil, subprocess, sys
areg, ireg, root, repo = sys.argv[1:5]
cur = json.load(open(f"{repo}/content/assets.json", encoding="utf8"))
imgs = [a for a in cur["items"] if a["kind"] == "image"]
byid = {}
for d, _, fs in os.walk(root):
    for f in fs:
        if f.endswith(".m4a"): byid[f.split("_", 1)[0]] = os.path.join(d, f)
out = f"{repo}/public/assets/audio"; os.makedirs(out, exist_ok=True)
items, skipped = [], []
for r in csv.DictReader(open(areg, encoding="utf8")):
    i = r["asset_id"]
    if "internal" in r["intended_use"].lower() or r["license"].startswith("Public Domain (legacy") or i == "AUD-0163":
        skipped.append((i, "internal-only / legacy PD")); continue
    p = byid.get(i)
    if not p: skipped.append((i, "no converted file")); continue
    shutil.copyfile(p, f"{out}/{i}.m4a")
    dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p], capture_output=True, text=True).stdout.strip() or 0)
    folder = r["path"].split("/audio/")[-1].split("/")[0]
    items.append({"id": i, "kind": "audio", "file": f"/assets/audio/{i}.m4a", "title": r["title"], "creator": r["creator"], "date": r["date"] or None,
        "source": r["source_page_url"], "license": r["license"], "attribution": r["attribution_text"], "use": r["intended_use"], "duration_s": round(dur, 1),
        "tags": [t for t in r["tags"].split(";") if t][:8], "collection": folder,
        "modified": "مضغوط AAC أحادي وقُصّ إلى 40 ثانية كحدّ أقصى"})
for it in items:
    for k in [k for k, v in it.items() if v is None]: del it[k]
cur["items"] = imgs + items
json.dump(cur, open(f"{repo}/content/assets.json", "w", encoding="utf8"), ensure_ascii=False, indent=1)
# icons
icons, sets = [], []
iconroot = [os.path.join(d) for d, _, _ in os.walk(root) if d.endswith("/icons")][0] if False else None
src_icons = os.path.join(root, "99_LEGAL_SOURCE_ASSETS/OPEN_LICENSE/icons")
sets_meta = {"tabler": ("Tabler Icons (outline)", "MIT"), "lucide": ("Lucide", "ISC"), "fluentui": ("Fluent UI System Icons", "MIT"),
             "material": ("Material Symbols (Outlined)", "Apache-2.0"), "phosphor": ("Phosphor Icons", "MIT"), "heroicons": ("Heroicons (24 outline)", "MIT")}
for sd in sorted(os.listdir(src_icons)):
    key = sd.split("_")[0]; name, lic = sets_meta[key]
    dst = f"{repo}/public/assets/icons/{key}"; os.makedirs(dst, exist_ok=True)
    n = 0
    for f in sorted(os.listdir(os.path.join(src_icons, sd))):
        p = os.path.join(src_icons, sd, f)
        if f.lower().endswith(".svg"):
            shutil.copyfile(p, f"{dst}/{f}"); icons.append({"set": key, "name": f[:-4], "file": f"/assets/icons/{key}/{f}"}); n += 1
        elif f.upper().startswith("LICENSE"): shutil.copyfile(p, f"{dst}/LICENSE.txt")
    sets.append({"key": key, "name": name, "license": lic, "count": n, "license_file": f"/assets/icons/{key}/LICENSE.txt"})
json.dump({"version": "1.0.0", "sets": sets, "icons": icons}, open(f"{repo}/content/icons.json", "w", encoding="utf8"), ensure_ascii=False, indent=1)
print("audio", len(items), "skipped", skipped, "icons", len(icons), [s['count'] for s in sets])
