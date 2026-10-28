#!/usr/bin/env python3
"""Build content/heritage/{catalog,excerpts,summary}.json from 99_LEGAL_SOURCE_ASSETS.

Usage: python3 -I tools/generators/build_heritage.py <packs_dir>
Only reads the source texts. Excerpts are verbatim windows (heritage_lib.window) located by tools/generators/heritage_picks.tsv,
and are produced ONLY for texts whose rights verdict is public-domain / CC0 and that are not on the quality/safety hold list.
Texts under CC BY-NC(-SA) (OpenITI) and anything not confirmed stay catalogue-only.
"""
import csv, hashlib, importlib.util, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))


def imp(n):
    sp = importlib.util.spec_from_file_location(n, os.path.join(HERE, n + ".py")); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return m


L = imp("heritage_lib"); META = imp("heritage_meta")
SRC = sys.argv[1]
BASE = os.path.join(SRC, "ATHAR_LIBRARY_v2_CORE", "ATHAR_RESEARCH_LIBRARY", "99_LEGAL_SOURCE_ASSETS")
OUT = os.path.join(ROOT, "content", "heritage")
csv.field_size_limit(1 << 30)
MAX_PER_TEXT = 6
ORD = {1: "الأول", 2: "الثاني", 3: "الثالث", 4: "الرابع", 5: "الخامس", 6: "السادس", 7: "السابع", 8: "الثامن", 9: "التاسع", 10: "العاشر", 11: "الحادي عشر", 12: "الثاني عشر", 13: "الثالث عشر", 14: "الرابع عشر", 15: "الخامس عشر", 16: "السادس عشر", 17: "السابع عشر", 18: "الثامن عشر", 19: "التاسع عشر", 20: "العشرون"}
SKILL_AR = {"obs": "الملاحظة", "ded": "الاستنتاج", "hyp": "الفرضية والاختبار", "evd": "الأدلة والقرائن", "myst": "الغموض والتشويق", "crit": "التفكير النقدي"}
LANG_AR = {"en": "الإنجليزية", "fr": "الفرنسية", "ja": "اليابانية", "zh": "الصينية", "ar": "العربية"}
# words that must never appear in an excerpt shown to teens (operational harm / graphic content) - build fails if matched
BLOCK = re.compile(r"\b(rape|raped|dismember|disembowel|torture[sd]?|how to (make|build) (a )?(bomb|poison)|lethal dose)\b|拷問|強姦|凌辱", re.I)


def century_ar(y: int) -> str:
    c = (y - 1) // 100 + 1
    return f"القرن {ORD.get(c, str(c))} الميلادي"


def era_for(m, row):
    yr = m[5]
    if isinstance(yr, tuple):
        ah, ce = yr
        return f"{('القرن ' + ORD.get((ah - 1) // 100 + 1, '') + ' الهجري')} (نحو {ah}هـ / {ce}م)", ce
    if isinstance(yr, int):
        return f"{century_ar(yr)} ({yr})", yr
    return f"{yr}", None


def licence(kind, row):
    basis = row["license_or_pd_basis"]
    if kind == "openiti":
        return "CC BY-NC-SA 4.0 (الملف الرقمي)", "cc_by_nc_ref", "مرجع فقط: النص الأصلي قديم، لكن ملف OpenITI الرقمي بترخيص غير تجاري؛ لا اقتباس ولا نشر في منتج ATHAR."
    if kind == "se":
        return "ملك عام + CC0 1.0 (تحرير Standard Ebooks)", "pd_cc0", "ملك عام موثّق (النص) مع إهداء CC0 لتحرير الإصدار."
    if kind == "aozora":
        return "ملك عام (اليابان وأمريكا وأوروبا)", "pd_verified", "ملك عام موثّق: انقضت مدة الحماية في اليابان، ونُشر قبل 1931 في أمريكا؛ تسمح قواعد «أوزورا» بإعادة الاستعمال."
    if kind == "wiki":
        return "ملك عام (نص قديم؛ تفريغ ويكي مصدر)", "pd_verified", "ملك عام موثّق (نص صيني قديم)؛ التفريغ لا يضيف حقاً جديداً بحسب سجل الأصول."
    if kind == "ia":
        return "ملك عام (Public Domain Mark 1.0)", "pd_verified", "ملك عام موثّق، لكن النص مسح ضوئي رديء."
    return "ملك عام (نص Project Gutenberg بلا قيود)", "pd_verified", "ملك عام موثّق (الولايات المتحدة، ومدة الحماية منقضية في بلدان الحياة+70 والحياة+50)."


def ebook_no(row):
    for f in (row["edition_or_digitization"], row["source_url"]):
        m = re.search(r"(?:eBook|PG) ?#(\d+)", f) or re.search(r"/(\d+)(?:-\d)?\.txt", f)
        if m: return m.group(1)
    return None


def main():
    os.makedirs(OUT, exist_ok=True)
    rows = [r for r in csv.DictReader(open(os.path.join(BASE, "ASSET_MANIFEST_W2_TEXTS.csv"), encoding="utf-8")) if not r["path"].endswith(".png")]
    picks = {}
    for ln in open(os.path.join(HERE, "heritage_picks.tsv"), encoding="utf-8").read().split("\n"):
        if not ln.strip() or ln.startswith("#"): continue
        a = ln.split("|")
        if len(a) != 5: raise SystemExit("bad pick line: " + ln[:80])
        picks.setdefault(a[0], []).append(a[1:])
    catalog, excerpts, warnings = [], [], []
    for r in rows:
        aid = r["asset_id"]
        m = META.M[aid]
        slug, title_ar, ak, lang, kind, _yr = m
        era_ar, year = era_for(m, r)
        lic, verdict, verdict_ar = licence(kind, r)
        path = os.path.join(BASE, r["path"].split("99_LEGAL_SOURCE_ASSETS/", 1)[1])
        sha = hashlib.sha256(open(path, "rb").read()).hexdigest()
        if sha != r["sha256"]: warnings.append(f"{aid}: sha256 differs from manifest")
        hold = META.HOLD.get(aid)
        excerptable = verdict in ("pd_verified", "pd_cc0") and not hold and aid in picks
        reason = None
        if verdict == "cc_by_nc_ref": reason = verdict_ar
        elif hold: reason = hold
        elif aid not in picks: reason = "لم نجد مقطعاً مناسباً للاقتباس القصير (النص سردي طويل أو مغامراتي) أو لم يُراجَع بعد؛ يبقى في الفهرس."
        entry = {
            "id": slug, "asset_id": aid, "source_id": r["catalog_source_id"] or None, "kind": kind,
            "title": r["title"], "title_ar": title_ar, "author": r["author"], "author_ar": META.AUTH[ak],
            "era_ar": era_ar, "year": year, "lang": lang, "lang_ar": LANG_AR[lang],
            "licence": lic, "licence_basis": r["license_or_pd_basis"], "source_url": r["source_url"], "digitization": r["edition_or_digitization"],
            "rights": verdict, "rights_ar": verdict_ar, "excerptable": excerptable, "reference_reason_ar": reason, "ebook_no": ebook_no(r) if kind == "pg" else None,
            "file": r["path"].split("99_LEGAL_SOURCE_ASSETS/", 1)[1], "sha256": sha, "excerpt_count": 0,
        }
        if excerptable:
            txt = L.clean(L.read_text(path), kind)
            paras = L.paragraphs(txt, lang, kind == "pg")
            ps = picks[aid][:MAX_PER_TEXT]
            for n, (loc, skill, hook, gloss) in enumerate(ps, 1):
                t = L.window(paras, loc, lang)
                if not t.strip(): raise SystemExit(f"{aid} {loc}: empty window")
                words = L.wcount(t, lang)
                if L.over(t, lang) or words > 120:
                    raise SystemExit(f"{aid} {loc}: too long ({words} words)")
                if lang in ("ja", "zh") and (t.count("「") != t.count("」") or re.search(r"[�]", t)):
                    warnings.append(f"{aid} {loc}: unbalanced CJK quotes")
                if BLOCK.search(t): raise SystemExit(f"{aid} {loc}: blocked content word")
                if lang in ("en", "fr") and t.count('"') % 2 and not t.lstrip().startswith('"'): warnings.append(f"{aid} {loc}: odd number of straight quotes")
                excerpts.append({
                    "id": f"{slug}-{n}", "text_id": slug, "n": n, "lang": lang, "text": t, "words": round(words, 1), "locator": f"فقرة {loc.split(':')[0]}",
                    "skill": skill, "skill_ar": SKILL_AR[skill], "hook_ar": hook, "gloss_ar": gloss,
                    "attribution": f"{r['title']}، {r['author']} ({aid}" + (f"، {r['catalog_source_id']}" if r["catalog_source_id"] else "") + ")",
                })
            entry["excerpt_count"] = len(ps)
            if kind == "aozora": entry["edit_note_ar"] = "حُذفت علامات القراءة (الفوريغانا) وتعليقات المدخِلين الإلكترونية؛ النص لم يُغيَّر."
            if kind == "pg": entry["edit_note_ar"] = "حُذفت ترويسة المشروع وعلامات الخط المائل المؤقتة؛ نص المقطع كما في المصدر."
        catalog.append(entry)
    ids = [e["id"] for e in catalog]
    assert len(ids) == len(set(ids)), "duplicate slugs"
    st = {"texts": len(catalog), "excerpted": sum(1 for e in catalog if e["excerpt_count"]), "reference_only": sum(1 for e in catalog if not e["excerpt_count"]),
          "reference_cc_by_nc": sum(1 for e in catalog if e["rights"] == "cc_by_nc_ref"), "reference_other": sum(1 for e in catalog if not e["excerpt_count"] and e["rights"] != "cc_by_nc_ref"),
          "excerpts": len(excerpts), "excerpt_words": round(sum(x["words"] for x in excerpts)), "excerpt_words_latin": round(sum(x["words"] for x in excerpts if x["lang"] in ("en", "fr"))),
          "excerpt_words_cjk_halfchars": round(sum(x["words"] for x in excerpts if x["lang"] in ("ja", "zh"))), "max_words": max(x["words"] for x in excerpts), "by_lang": {}}
    for e in catalog: st["by_lang"][e["lang"]] = st["by_lang"].get(e["lang"], 0) + 1
    for name, data in (("catalog", {"version": 1, "items": catalog}), ("excerpts", {"version": 1, "items": excerpts}), ("summary", st)):
        with open(os.path.join(OUT, name + ".json"), "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=1)
    print(json.dumps(st, ensure_ascii=False, indent=1))
    for w in warnings: print("WARN", w)


if __name__ == "__main__":
    main()
