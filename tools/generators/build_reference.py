#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Builds content/reference/*.json (learner-facing reference pages) from the research library (reference data, read-only).

Usage: build_reference.py <LIBRARY_ROOT> <OUT_DIR>
  LIBRARY_ROOT = .../ATHAR_LIBRARY_v2_CORE/ATHAR_RESEARCH_LIBRARY

Rules: library Arabic text is kept as is (only internal tags, citations and file references are stripped);
protected literature is referenced, never excerpted; items unsafe for minors are age-gated or excluded and listed
in excluded.json with a reason. Nothing is dropped silently: counts_in / counts_out are written to counts.json.
"""
import csv, glob, json, os, re, sys, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import reference_authored as A

LIB, OUT = sys.argv[1], sys.argv[2]
os.makedirs(OUT, exist_ok=True)
EXCLUDED = []     # {page, id, title, kind, reason}
COUNTS = {}       # page -> {section: {"in": n, "out": n}}

def exclude(page, id_, title, kind, reason):
    EXCLUDED.append(dict(page=page, id=id_, title=title, kind=kind, reason=reason))

# ------------------------------------------------------------------ helpers
TAG = re.compile(r"\[(?:حقيقة موثقة|تفسير بحثي|افتراض تصميمي|استنتاج استثماري)[^\]]*\]")
SRC = re.compile(r"ATH-SRC-\d{4}")
SRCBR = re.compile(r"\[(?:ATH-SRC-[^\]]*)\]")
INTERNAL_PAREN = re.compile(r"\((?:أُضيف|عُدّل|دُقّق|تحديث|تنبيه|تحقق|عُدلت|حُسم)[^()]*\)")
MDFILE = re.compile(r"`[^`]*\.md[^`]*`")
HSREF = re.compile(r"\((?:HS-\d+[،, ]*)+\)")
HSREF2 = re.compile(r"\bHS-\d+\b")
KOID = re.compile(r"\(?KO-[A-Z]{2}-[0-9A-Z]+-\d{3}(?:[،, ]+\d{3})*\)?")

def clean(t):
    if not t: return ""
    t = SRCBR.sub("", t)
    t = TAG.sub("", t)
    t = INTERNAL_PAREN.sub("", t)
    t = MDFILE.sub("", t)
    t = HSREF.sub("", t)
    t = HSREF2.sub("", t)
    t = KOID.sub("", t)
    t = re.sub(r"\[[^\]]*ATH-SRC[^\]]*\]", "", t)
    t = re.sub(r"\[\d{3,4}\]|\[ص[^\]]*\]", "", t)
    t = re.sub(r"\((?:[^()]*?)(?:\bC\d{1,2}\b|HER-\d\d|LO-\d+|ATH-SRC|SAFE_VIRTUAL|الدفعة)(?:[^()]*?)\)", "", t)
    t = re.sub(r"\s*\((?:ARC-\d\d)\)", "", t)
    t = re.sub(r"\s*\(\d\d §[^)]*\)?", "", t)
    t = re.sub(r"[،,]?\s*بالتنسيق مع (?:المكتبة|فريق) \d\d[^.،]*", "", t)
    t = re.sub(r"خبير (?:04|08|11)\b", "خبير مختص", t)
    t = t.replace("المكتبة 11", "سياسة الحماية والخصوصية")
    t = re.sub(r"المكتبة \d\d", "مكتبة أثر البحثية", t)
    t = re.sub(r"\s*\([^()]*(?:§|أطلس \d|سياسة \d|مكتبة \d|فريق \d|KO-)[^()]*\)", "", t)
    t = t.replace("«نسبة الترجيح» لا «نسبة الأرجحية»", "«نسبة الترجيح»").replace("، لا «نسبة الأرجحية» التي تعني odds ratio", "")
    # product terminology wins over older library wording (the library's own glossary recommends the same)
    t = t.replace("سلسلة الحيازة", "سلسلة العهدة")
    t = t.replace("**", "").replace("`", "").replace("ATHAR", "أثر")
    t = re.sub(r"\(\s*\)", "", t)
    t = re.sub(r"\s+([،؛.:])", r"\1", t)
    t = re.sub(r"[،؛]\s*\.$", ".", t)
    t = re.sub(r"[ \t]{2,}", " ", t)
    t = re.sub(r"(?:\s+(?:بما يتسق مع|وانظر|انظر|راجع|وفق|كما في|ويرجع إلى))\s*\.?\s*$", ".", t)
    t = re.sub(r"\(\s*[،؛]\s*", "(", t)
    return t.strip(" \t،؛")

def srcs(raw):
    return sorted(set(SRC.findall(raw or "")))

def read(path):
    return open(os.path.join(LIB, path), encoding="utf-8").read()

def csvrows(path):
    return list(csv.DictReader(open(os.path.join(LIB, path), encoding="utf-8-sig")))

def dump(name, obj):
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=1)

def sections(md, pat):
    """split markdown into [(heading_match, body)] by a heading regex (multiline)."""
    ms = list(re.finditer(pat, md, re.M))
    out = []
    for i, m in enumerate(ms):
        end = ms[i + 1].start() if i + 1 < len(ms) else len(md)
        out.append((m, md[m.end():end]))
    return out

def fields(body):
    """parse '- **Label:** text' bullets (with indented sub-bullets) into {label: raw text}."""
    res, cur = collections.OrderedDict(), None
    for line in body.split("\n"):
        m = re.match(r"^- \*\*(.+?):?\*\*:?\s*(.*)$", line)
        if m and not line.startswith("  "):
            cur = m.group(1).strip().rstrip(":")
            res[cur] = m.group(2).strip()
        elif cur and (line.startswith("  ") or re.match(r"^\s*[-\d]", line)) and line.strip():
            res[cur] += "\n" + re.sub(r"^\s*(?:-|\d+\.)\s*", "", line).strip()
        elif cur and not line.strip():
            continue
        elif line.startswith("#") or line.startswith("---"):
            cur = None
    return res

def table(md_block):
    rows = []
    for line in md_block.split("\n"):
        if line.startswith("|") and not re.match(r"^\|\s*[-:| ]+\|?\s*$", line):
            rows.append([c.strip() for c in line.strip().strip("|").split("|")])
    return rows[1:] if rows else rows   # drop header

AR_DIACRITICS = re.compile(r"[ً-ْٰ]")
def norm_letter(s):
    s = AR_DIACRITICS.sub("", s).strip()
    s = re.sub(r"^(?:ال)", "", s) if len(s) > 3 else s
    s = s.lstrip("«»()\"' ")
    c = s[0] if s else "؟"
    c = {"أ": "ا", "إ": "ا", "آ": "ا", "ٱ": "ا", "ى": "ي", "ة": "ه"}.get(c, c)
    return c

# knowledge objects (for resolving ids/names and relating by source)
KO, KONAME = [], {}
for f in sorted(glob.glob(os.path.join(LIB, "12_KNOWLEDGE_OBJECTS", "*.jsonl"))):
    if "rag_chunks" in f: continue
    for l in open(f, encoding="utf-8"):
        if l.strip():
            d = json.loads(l); KO.append(d); KONAME[d["ko_id"]] = d.get("name_ar") or d.get("name")
PLAYER_TYPES = {"forensic_concept", "reasoning_skill", "narrative_pattern"}
SRC_MASTER = {}
for l in open(os.path.join(LIB, "01_SOURCE_CATALOG", "sources_master.jsonl"), encoding="utf-8"):
    if l.strip():
        d = json.loads(l); SRC_MASTER[d["source_id"]] = d

def known_src(ids):
    return [s for s in ids if s in SRC_MASTER]

def related_kos(src_ids, types=PLAYER_TYPES, limit=5):
    sset = set(src_ids)
    scored = []
    for k in KO:
        if k["type"] not in types: continue
        ov = len(sset & set(k.get("source_ids") or []))
        if ov: scored.append((-ov, k["ko_id"]))
    scored.sort()
    return [x[1] for x in scored[:limit]]

# ------------------------------------------------------------------ glossary
CAT_AR = {
    "general": "عام", "quality": "الجودة والاعتماد", "statistics": "الإحصاء والاحتمال", "dna": "الحمض النووي", "fingerprints": "البصمات",
    "legal_roles": "الأدوار القانونية", "ethics": "الأخلاقيات", "interpretation": "تفسير الأدلة", "documents": "فحص الوثائق", "medicine": "الطب الشرعي",
    "bias": "التحيز", "digital": "الأدلة الرقمية", "trace": "الآثار الدقيقة", "crime_scene": "مسرح الجريمة", "chain_of_custody": "سلسلة العهدة",
    "pattern": "أدلة الأنماط", "imaging": "التصوير الجنائي", "chemistry": "الكيمياء الجنائية", "toxicology": "علم السموم", "anthropology": "الأنثروبولوجيا الشرعية",
}
rows = csvrows("04_FORENSIC_SCIENCE/arabic_forensic_glossary.csv")
gl = []
for r in rows:
    alts = []
    for a in re.split(r"[؛;]", r["alternatives_ar"] or ""):
        a = clean(a)
        # internal remarks about ATHAR's own earlier usage are not learner information
        if not a or "ATHAR" in a or "أثر في الجولة" in a or "لم نجده" in a or "الجولة الأولى" in a: continue
        alts.append(a)
    ids = known_src(srcs(r["source_ids"]) + srcs(r["concept_source_ids"]))
    gl.append(dict(
        id=r["term_id"], term_en=r["term_en"], term_ar=r["term_ar"], alts_ar=alts, def_ar=clean(r["definition_ar"]),
        cat=r["discipline"], level=r["teen_level"],
        status={"sourced": "sourced", "sourced-variant": "variant", "proposed": "proposed"}[r["status"]],
        tier=r["source_tier"], letter=norm_letter(r["term_ar"]), src_ids=ids, ko_ids=related_kos(srcs(r["concept_source_ids"]) or ids, limit=4),
    ))
cats = collections.Counter(g["cat"] for g in gl)
dump("glossary.json", dict(version="1.0.0", generated_from="ATHAR_LIBRARY_v2_CORE/04_FORENSIC_SCIENCE/arabic_forensic_glossary.csv",
     hook_ar=A.PAGE_HOOKS["glossary"], categories=[dict(id=c, label_ar=CAT_AR[c], count=n) for c, n in sorted(cats.items(), key=lambda x: -x[1])], items=gl))
COUNTS["glossary"] = {"terms": {"in": len(rows), "out": len(gl)}}
# the glossary .md is the same 248 terms rendered as prose; verify that rather than assume
gmd_text = read("04_FORENSIC_SCIENCE/ARABIC_FORENSIC_GLOSSARY.md")
COUNTS["glossary"]["csv_terms_found_in_md"] = {"in": len(gl), "out": sum(1 for g in gl if g["term_ar"] in gmd_text)}

# ------------------------------------------------------------------ methods
mrows = csvrows("04_FORENSIC_SCIENCE/FORENSIC_METHOD_VALIDITY_MATRIX.csv")
assert len(mrows) == len(A.METHODS) == 24, (len(mrows), len(A.METHODS))
methods = []
for i, (r, a) in enumerate(zip(mrows, A.METHODS), 1):
    ids = known_src(srcs(r["source_ids"]))
    methods.append(dict(
        id=f"M{i:02d}", name_en=r["method"], name_ar=a["name_ar"], hook_ar=a["hook_ar"], discipline_en=r["discipline"],
        discipline_ar=A.DISCIPLINE_AR.get(r["discipline"].split(" / ")[0], r["discipline"]), tier=a["tier"], min_band=a["min_band"],
        can_ar=a["can_ar"], cannot_ar=a["cannot_ar"], errors_ar=a["errors_ar"], suitability_en=r["teen_education_suitability"],
        in_mvp=r["include_in_mvp"], confidence=r["confidence"], standards_en=r["relevant_standards"],
        original_en=dict(validity=r["foundational_validity_assessment"], error_rate=r["error_rate_evidence"], concerns=r["key_concerns"]),
        src_ids=ids, ko_ids=related_kos(ids, {"forensic_concept"}, 3)))
dump("methods.json", dict(version="1.0.0", generated_from="04_FORENSIC_SCIENCE/FORENSIC_METHOD_VALIDITY_MATRIX.csv",
     hook_ar=A.PAGE_HOOKS["methods"], tiers=A.TIERS, items=methods))
COUNTS["methods"] = {"methods": {"in": len(mrows), "out": len(methods)}, "adult_gated": {"in": 0, "out": sum(1 for m in methods if m["min_band"] == "18+")}}
for m in methods:
    if m["min_band"] == "18+":
        exclude("methods", m["id"], m["name_ar"], "age_gated_18plus", "الجدول يصنّف ملاءمتها للمراهقين «منخفضة» أو «للبالغين فقط» (سلاح/وفاة/خلائط معقدة)؛ تظهر للبالغين فقط ولا تظهر للقاصرين أو لمن لم تُحدَّد فئته العمرية.")

# ------------------------------------------------------------------ biases
bmd = read("06_COGNITIVE_SCIENCE/COGNITIVE_BIAS_CASE_LIBRARY.md")
biases = []
for m, body in sections(bmd, r"^### (B\d\d) — (.+)$"):
    bid, head = m.group(1), m.group(2)
    mm = re.match(r"(.+?)\s*\((.+)\)\s*$", head)
    name_ar, name_en = (mm.group(1).strip(), mm.group(2).strip()) if mm else (head, "")
    f = fields(body.split("\n### ")[0].split("\n## ")[0])
    rule = re.findall(r"\*\*([^*]{6,80})\*\*", f.get("الاستخلاص", ""))
    biases.append(dict(
        id=bid, name_ar=name_ar, name_en=name_en, research_ar=clean(f.get("ما يقوله البحث", "")), debrief_ar=clean(f.get("الاستخلاص", "")),
        golden_rule_ar=clean(rule[-1]) if rule else "", example_ar=A.BIAS_EXAMPLES[bid], src_ids=known_src(srcs(body)), ko_ids=[]))
assert len(biases) == 17, len(biases)
for b in biases: b["ko_ids"] = related_kos(b["src_ids"], {"reasoning_skill", "forensic_concept"}, 3)
exclude("biases", "B-retired-use", "«الاستخدام المسموح» لتحيزات فشل تكرارها", "not_learner_facing", "تعليمات تصميمية لوحدة اختيارية؛ المعروض قصتا الإيحاء الاجتماعي واستنزاف الأنا كدرس في أن العلم يصحح نفسه.")
retired_md = bmd.split("### ✗ — تحيزات لا تُبنى عليها آليات لعب")[1].split("\n## ")[0]
dump("biases.json", dict(version="1.0.0", generated_from="06_COGNITIVE_SCIENCE/COGNITIVE_BIAS_CASE_LIBRARY.md", hook_ar=A.PAGE_HOOKS["biases"],
     balance_ar=next(clean(x) for x in re.findall(r"^\d\. (.+)$", bmd.split("## 0.")[1].split("## 1.")[0], re.M) if x.startswith("**التحيز ليس دائماً")),
     self_correcting_ar=[clean(re.sub(r"^- ", "", x)) for x in re.findall(r"^- .+$", retired_md, re.M)][:2],
     items=biases))
exclude("biases", "BIAS-rules", "القواعد العامة الملزمة لكتّاب قضايا التحيز (البنود 1–5 و7) والتسلسل المقترح للموسم والفجوات", "not_learner_facing", "قواعد تصميم وخطط موسم داخلية؛ المعروض البند الذي يخص المتعلم: التحيز ليس دائماً خطأً.")
COUNTS["biases"] = {"bias_cards": {"in": 17, "out": len(biases)}}

# ------------------------------------------------------------------ reasoning
rd = "05_INVESTIGATIVE_REASONING/"
emd = read(rd + "COMMON_REASONING_ERRORS.md")
strength = {}
for row in table(emd.split("## جدول ملخص")[1].split("\n---\n")[0]):
    strength[int(row[0])] = clean(row[3])
errs = []
for m, body in sections(emd, r"^## (\d+)\. (.+)$"):
    n, head = int(m.group(1)), m.group(2)
    mm = re.match(r"(.+?)\s*\((.+)\)\s*$", head)
    name_ar, name_en = (mm.group(1).strip(), mm.group(2).strip()) if mm else (head.strip(), "")
    f = fields(body.split("\n## ")[0])
    errs.append(dict(n=n, name_ar=name_ar, name_en=name_en, definition_ar=clean(f.get("التعريف", "")), limits_ar=clean(f.get("حدود الدليل", "")),
                     strength_ar=strength.get(n, ""), practice_ar=A.ERROR_PRACTICE[n], src_ids=known_src(srcs(body))))
assert len(errs) == 14, len(errs)
for e in errs: e["ko_ids"] = related_kos(e["src_ids"], {"reasoning_skill", "forensic_concept"}, 3)

gmd = read(rd + "EVIDENCE_EVALUATION_GUIDE.md")
types_ = [dict(kind_ar=clean(r[0]), def_ar=clean(r[1]), example_ar=clean(r[2])) for r in table(gmd.split("## 0.")[1].split("**للمراهق")[0])]
criteria = []
for m, body in sections(gmd, r"^## ([1-5])\. (.+)$"):
    head = m.group(2)
    mm = re.match(r"^(.+?)\s*\((.+?)\)(?::.*)?$", head)
    teen = re.findall(r"\*\*للمراهق:\*\*\s*(.+)", body)
    teen_lines = [clean(t) for t in teen if clean(t)]
    # multi-line teen blocks (numbered questions) are folded in
    t2 = re.search(r"\*\*للمراهق:\*\*\s*سؤالان[^\n]*\n((?:\d\. .+\n?)+)", body)
    if t2: teen_lines = ["سؤالان منفصلان: " + " و".join(clean(x) for x in re.findall(r"\d\. (.+)", t2.group(1)))] + teen_lines[1:]
    professional = re.search(r"\*\*مهنياً:\*\*\s*(.+)", body)
    criteria.append(dict(n=int(m.group(1)), name_ar=(mm.group(1) if mm else head).strip(), name_en=(mm.group(2) if mm else ""), ask_ar=teen_lines[0] if teen_lines else "",
                         extra_ar=teen_lines[1:], pro_ar=clean(professional.group(1)) if professional else "", src_ids=known_src(srcs(body))))
assert len(criteria) == 5
unc_block = gmd.split("**السلّم العربي المقترح لـ ATHAR**")[1].split("لا نستخدم")[0]
ladder = [dict(level=int(r[0]), phrase_ar=clean(r[1]), range=r[2]) for r in table(unc_block)]
assert len(ladder) == 7
unc_teen = clean(re.search(r"\*\*للمراهق:\*\*\s*«(قل لنا أمرين.+?)»", gmd).group(1))
pocket = [clean(x) for x in re.findall(r"^\d\. (.+)$", gmd.split("## 8.")[1].split("## 9.")[0], re.M)]
assert len(pocket) == 7

pmd = read(rd + "ETHICAL_INVESTIGATION_PRINCIPLES.md")
ethics = []
for m, body in sections(pmd, r"^## المبدأ (\d): (.+)$"):
    body = body.split("\n## ")[0]
    mm = re.match(r"(.+?)\s*\((.+)\)\s*$", m.group(2))
    rules = []
    mr = re.search(r"- \*\*قواعد التصميم(?: الملزمة)?[^:]*:\*\*\s*(.*?)(?=\n- \*\*ما يتعلمه المستخدم)", body, re.S)
    if mr:
        rules = [clean(x) for x in re.findall(r"^\s+(?:\d+\.|-)\s+(.+)$", mr.group(1), re.M)] or [clean(mr.group(1))]
    ethics.append(dict(n=int(m.group(1)), name_ar=(mm.group(1) if mm else m.group(2)).strip(), name_en=(mm.group(2) if mm else ""),
                       learn_ar=clean(re.search(r"\*\*ما يتعلمه المستخدم:\*\*\s*(.+)", body).group(1)),
                       commitments_ar=[r for r in rules if r], src_ids=known_src(srcs(body))))
assert len(ethics) == 7
ethic_checks = []

smd = read("06_COGNITIVE_SCIENCE/REASONING_SKILLS_TAXONOMY.md")
area = None
skills = []
for line_blk in re.split(r"(?m)^(?=## |### RS-)", smd):
    h = re.match(r"## ([أ-ي]+)\. (.+)", line_blk)
    if h: area = h.group(2).strip(); continue
    m = re.match(r"### (RS-\d\d) — (.+)", line_blk)
    if not m: continue
    mm = re.match(r"(.+?)\s*\((.+)\)\s*$", m.group(2))
    f = fields(line_blk)
    skills.append(dict(id=m.group(1), name_ar=(mm.group(1) if mm else m.group(2)).strip(), name_en=(mm.group(2) if mm else ""), area_ar=area,
                       def_ar=clean(f.get("التعريف التشغيلي", "")), mistakes_ar=clean(f.get("أخطاء شائعة", "")), src_ids=known_src(srcs(line_blk))))
assert len(skills) == 24, len(skills)
ct = read("06_COGNITIVE_SCIENCE/CRITICAL_THINKING_ASSESSMENT_FRAMEWORK.md")
ct_lessons = [clean(m.group(1)) for m in re.finditer(r"^### الدرس \d — (.+)$", ct, re.M)]
assert len(ct_lessons) == 7
dump("reasoning.json", dict(version="1.0.0", generated_from="05_INVESTIGATIVE_REASONING + 06_COGNITIVE_SCIENCE", hook_ar=A.PAGE_HOOKS["reasoning"],
     errors=errs, evidence_types=types_, criteria=criteria, uncertainty=dict(ladder=ladder, teen_ar=unc_teen), pocket_questions=pocket,
     ethics=ethics, skills=skills, assessment_notes_ar=ct_lessons))
COUNTS["reasoning"] = {"reasoning_errors": {"in": 14, "out": len(errs)}, "evidence_criteria": {"in": 5, "out": len(criteria)}, "pocket_questions": {"in": 7, "out": len(pocket)},
                       "ethics_principles": {"in": 7, "out": len(ethics)}, "skills": {"in": 24, "out": len(skills)}, "assessment_notes": {"in": 7, "out": len(ct_lessons)}}
exclude("reasoning", "ETHICS-checklist", "قائمة فحص أخلاقية لكل قضية قبل النشر", "not_learner_facing", "قائمة تحقق داخلية لفريق التحرير قبل نشر القضايا؛ مبادئها السبعة معروضة في الصفحة.")
exclude("reasoning", "ETHICS-minors-handling", "التعامل مع الموضوعات الواقعية مع المراهقين / الرفاه النفسي", "not_learner_facing", "قواعد حماية داخلية (المكتبة 11)؛ لا تُعرض كمحتوى تعليمي بل تُطبَّق على القضايا.")
exclude("reasoning", "CTAF-3-5", "بنية التقييم المقترحة وخطة التحقق (الأقسام 3 إلى 6)", "not_learner_facing", "تصميم داخلي لقياس التعلم وخطط التحقق من الصلاحية؛ المعروض 7 دروس مختصرة عن حدود القياس.")
exclude("reasoning", "EEG-6", "تصنيف المصادر في أثر (القسم 6 من دليل تقييم الأدلة)", "not_learner_facing", "مقترح رموز واجهة داخلي يُختبر فهمه؛ لم يُعتمد بعد.")

# ------------------------------------------------------------------ rulebook
rb = read("02_DETECTIVE_LITERATURE/FAIR_PLAY_MYSTERY_RULEBOOK.md")
rule_secs = []
total_rules = 0
for m, body in sections(rb, r"^## ([أ-ي]ـ?)\. (.+)$"):
    letter = m.group(1)
    if letter not in A.RULEBOOK_SECTIONS: continue
    meta = A.RULEBOOK_SECTIONS[letter]
    rules = []
    for r in table(body.split("\n## ")[0]):
        code = re.sub(r"\*", "", r[0]).strip()
        txt = clean(r[1])
        breakable = "⚡" in r[-1] or "قابلة للكسر" in r[-1]
        origin = clean(r[2]) if len(r) > 3 else ""
        rules.append(dict(code=code, rule_ar=txt, breakable=breakable, origin_ar=origin))
    total_rules += len(rules)
    rule_secs.append(dict(letter=letter, id=meta["id"], title_ar=meta["title_ar"], plain_ar=meta["plain_ar"], icon=meta["icon"], rules=rules))
assert len(rule_secs) == 5
breakable_text = clean(rb.split("## و. القواعد القابلة للكسر")[1].split("\n---\n")[0])
dump("rulebook.json", dict(version="1.0.0", generated_from="02_DETECTIVE_LITERATURE/FAIR_PLAY_MYSTERY_RULEBOOK.md + 03_NARRATIVE_AND_GAME_DESIGN/HINT_AND_DIFFICULTY_SYSTEM.md",
     hook_ar=A.PAGE_HOOKS["rulebook"], sections=rule_secs,
     breakable_ar=["القاعدتان القابلتان للكسر فقط هما «الفاعل يظهر في الثلث الأول» و«الراوي غير الموثوق بالحذف».",
                   "تُكسران مرة واحدة في الموسم على الأكثر، وفي المستوى الأعلى فقط، ولمن هم 16 سنة فما فوق.",
                   "يشترط قرينتان تمهيديتان على الأقل تجعلان الكسر قابلاً للاكتشاف بإعادة القراءة.",
                   "الملخص الختامي يسمّي القاعدة المكسورة ويعرض القرائن التمهيدية."],
     hints=dict(title_ar="كيف تعمل التلميحات", ladder=A.HINT_LADDER_AR, rules_ar=A.HINT_RULES_AR, product_note_ar=A.HINT_PRODUCT_NOTE_AR,
                src_ids=known_src(srcs(read("03_NARRATIVE_AND_GAME_DESIGN/HINT_AND_DIFFICULTY_SYSTEM.md").split("## 3.")[0]))),
     ))
COUNTS["rulebook"] = {"fair_play_rules": {"in": len(re.findall(r"^\| \*\*(?:FP|NR|SC|BI|AG)-\d\d\*\*", rb, re.M)), "out": total_rules}}
exclude("rulebook", "FPR-G", "قواعد التقييم المرتبطة بالعدالة (AS-01 إلى AS-08)", "not_learner_facing", "قواعد تصحيح داخلية للتقييم؛ المعروض منها ما يخص اللاعب في قسم التلميحات.")
exclude("rulebook", "FPR-H", "قواعد الحقوق والأصالة (RT-01 إلى RT-06)", "not_learner_facing", "قواعد تحريرية قانونية داخلية لفريق المحتوى.")
exclude("rulebook", "FPR-I-J", "قائمة فحص المحرر وما لم يُحسم", "not_learner_facing", "أدوات عمل داخلية لفريق التحرير.")
exclude("rulebook", "HINT-4-7", "منحنى الصعوبة، قياس الإحباط، الخطة التجريبية (أقسام 4 إلى 7 من نظام التلميحات)", "not_learner_facing", "تصميم قياس وتجارب داخلية؛ المعروض سلّم التلميحات وقواعده.")

# ------------------------------------------------------------------ atlas
amd = read("02_DETECTIVE_LITERATURE/DETECTIVE_LITERATURE_ATLAS.md")
principles = []
sec_name = None
for blk in re.split(r"(?m)^(?=## القسم |### المبدأ )", amd):
    h = re.match(r"## (القسم [^:\n]+): (.+)", blk)
    if h: sec_name = h.group(2).strip(); continue
    m = re.match(r"### المبدأ (\d+) — (.+)", blk)
    if not m: continue
    f = fields(blk)
    principles.append(dict(n=int(m.group(1)), title_ar=clean(m.group(2)), section_ar=sec_name, principle_ar=clean(f.get("المبدأ", "")),
                           basis_ar=clean(f.get("الأساس الأدبي", "")), why_ar=clean(f.get("لماذا يعمل", "")), src_ids=known_src(srcs(blk))))
assert len(principles) == 50, len(principles)

wmd = read("02_DETECTIVE_LITERATURE/WORLD_AND_YA_MYSTERY_EXPANSION.md")
expansion = []
for m, body in sections(wmd, r"^### ATLAS-(\d+) — (.+)$"):
    f = fields(body.split("\n## ")[0])
    expansion.append(dict(n=int(m.group(1)), title_ar=clean(m.group(2)), principle_ar=clean(f.get("المبدأ", "")), basis_ar=clean(f.get("الأساس", "")),
                          why_ar=clean(f.get("لماذا يعمل", "")), src_ids=known_src(srcs(body))))
assert len(expansion) == 24, len(expansion)

hmd = read("02_DETECTIVE_LITERATURE/ARABIC_CLASSICAL_INFERENCE_HERITAGE.md")
corpus = []
for r in table(hmd.split("## 1. خريطة المتن")[1].split("**المصادر الثانوية")[0]):
    mm = re.match(r"(.+?)\s*\((.+?)\)\s*$", r[1])
    corpus.append(dict(work_ar=clean(r[0]), author_ar=clean(mm.group(1)) if mm else clean(r[1]), era_ar=clean(mm.group(2)) if mm else "", kind_ar=clean(r[2]),
                       idea_ar=clean(r[3]), src_ids=known_src(srcs(r[5]))))
assert len(corpus) == 14, len(corpus)
her = []
for m, body in sections(hmd, r"^### (HER-\d\d) — (.+)$"):
    f = fields(body.split("\n## ")[0])
    her.append(dict(id=m.group(1), title_ar=clean(m.group(2)), basis_ar=clean(f.get("الأساس", "")), src_ids=known_src(srcs(body))))
assert len(her) == 20, len(her)
limits = [clean(x) for x in re.findall(r"^\d\. (.+)$", hmd.split("## 3. ما لا يثبته هذا التراث")[1].split("\n---\n")[0], re.M)]
assert len(limits) == 8, len(limits)

pmd2 = read("02_DETECTIVE_LITERATURE/MYSTERY_PLOT_PATTERNS.md")
age_sym = {"✅": "مناسب", "⚠️": "بشروط", "⛔": "غير مناسب"}
ptab = {}
for r in table(pmd2.split("## جدول مرجعي سريع")[1].split("\n---\n")[0]):
    ptab[int(r[0])] = dict(diff=int(r[2]), a13=age_sym.get(r[3], r[3]), a16=age_sym.get(r[4], r[4]), a18=age_sym.get(r[5], r[5]))
patterns = []
for m, body in sections(pmd2, r"^### (\d+)\. (.+)$"):
    n = int(m.group(1))
    if n not in ptab: continue
    mm = re.match(r"(.+?)\s*\((.+)\)\s*$", m.group(2))
    f = fields(body.split("\n### ")[0].split("\n## ")[0])
    patterns.append(dict(n=n, name_ar=(mm.group(1) if mm else m.group(2)).strip(), name_en=(mm.group(2) if mm else ""), def_ar=clean(f.get("التعريف", "")),
                         pros_ar=clean(f.get("المزايا", "")), cons_ar=clean(f.get("العيوب", "")), **ptab[n]))
assert len(patterns) == 26, len(patterns)
avoid = [clean(x) for x in re.findall(r"^\d+أ?\. (.+)$", pmd2.split("## سادساً: الأنماط التي نوصي بعدم استخدامها مطلقاً")[1], re.M)]
exclude("atlas", "PLOT-examples", "«المثال التحليلي» في كل نمط من أنماط الحبكة (26)", "spoilers_and_protected_works", "الأمثلة تكشف حلول أعمال محمية بحقوق النشر وتُحلَّل بالاسم؛ تُركت خارج الصفحة (الإحالة فقط).")

myths = [clean(x) for x in re.findall(r"^(?:\d+أ?|1أ)\. (.+)$", amd.split("### ب. أين تكون الادعاءات المشهورة مبالغاً فيها؟")[1].split("### ج.")[0], re.M)]

# literary rights register: protected / uncleared works are listed as references only (title, author, year) - no excerpts, no characters
reg = csvrows("02_DETECTIVE_LITERATURE/LITERARY_RIGHTS_REGISTER.csv")
works = []
for r in reg:
    w = r["work_or_character"]
    if w == "_REGISTER_DISCLAIMER_":
        exclude("atlas", "REG-disclaimer", w, "register_note", "صف تنبيه داخلي في السجل (ليس عملاً)."); continue
    if re.search(r"\((?:characters?|manga & anime)|\bcharacters?\)|Hercule Poirot|Sherlock Holmes & Dr Watson|Arsene Lupin \(character", w) or "(characters" in w or w.endswith("(character)"):
        exclude("atlas", "REG-" + str(len(works)), w, "protected_character_or_trademark", "شخصية أدبية أو علامة تجارية محتملة؛ لا تُعرض شخصية محمية. يُشار إلى الأعمال نفسها فقط حيث وردت."); continue
    protected = bool(re.search(r"Protect", r["status_US"], re.I)) or r["status_US"].startswith("Protected")
    works.append(dict(title=w, author=r["author"], year=r["first_publication_year"], rights_ar="محمي بحقوق النشر: يُشار إليه فقط" if protected else "يُشار إليه فقط: حالة الحقوق قيد مراجعة قانونية"))
dump("atlas.json", dict(version="1.0.0", generated_from="02_DETECTIVE_LITERATURE/{DETECTIVE_LITERATURE_ATLAS,WORLD_AND_YA_MYSTERY_EXPANSION,ARABIC_CLASSICAL_INFERENCE_HERITAGE,MYSTERY_PLOT_PATTERNS}.md + LITERARY_RIGHTS_REGISTER.csv",
     hook_ar=A.PAGE_HOOKS["atlas"], hooks=A.ATLAS_HOOKS, principles=principles, expansion=expansion, corpus=corpus, heritage=her, heritage_limits_ar=limits,
     patterns=patterns, avoid_ar=avoid, myths_ar=myths, works=works,
     rights_note_ar="جميع بطاقات هذه الصفحة تحليلات بصياغة أثر. الأعمال المحمية والشخصيات المحمية يُشار إليها للمعرفة فقط: لا ننقل نصوصها ولا شخصياتها ولا تراجمها. هذه ملاحظات بحثية وليست استشارة قانونية."))
COUNTS["atlas"] = {"principles": {"in": 50, "out": len(principles)}, "world_ya_principles": {"in": 24, "out": len(expansion)}, "heritage_corpus": {"in": 14, "out": len(corpus)},
                   "heritage_principles": {"in": 20, "out": len(her)}, "plot_patterns": {"in": 26, "out": len(patterns)},
                   "rights_register_rows": {"in": len(reg), "out": len(works)}}

# ------------------------------------------------------------------ archetypes
arcs = [json.loads(l) for l in open(os.path.join(LIB, "13_CASE_DESIGN_REFERENCE", "case_archetypes.jsonl"), encoding="utf-8") if l.strip()]
out_arcs = []
for a in arcs:
    names = lambda ids: [KONAME[i] for i in ids if i in KONAME]
    lab = a.get("virtual_lab") or {}
    out_arcs.append(dict(
        id=a["archetype_id"], name_ar=a["name_ar"], name_en=a["name"], core_ar=clean(a["core_structure_ar"]),
        teaches_ar=names(a["primary_reasoning_skill_kos"]), concepts_ar=names(a["forensic_concept_kos"]), pattern_ar=names(a["narrative_pattern_kos"]),
        observables_ar=clean(a["assessment_observables_ar"]), narrative_pattern_kos=a["narrative_pattern_kos"], age_band=a["age_band"],
        age_variant_ar=clean(a["age_variant_ar"]), violence=a["violence_level"], violence_ar=clean(a["violence_level_ar"]),
        no_culprit=bool(a.get("no_culprit_case")), warnings_ar=[clean(x) for x in a["risks_ar"]], settings_ar=[clean(x) for x in a["arab_setting_variants_ar"]],
        lab_ar=lab.get("name_ar") or "", status=a["status"], min_band="18+" if a["age_band"] == "18+" else "all"))
dump("archetypes.json", dict(version="1.0.0", generated_from="13_CASE_DESIGN_REFERENCE/case_archetypes.jsonl (+ CASE_ARCHETYPES.md)", hook_ar=A.PAGE_HOOKS["archetypes"], items=out_arcs))
COUNTS["archetypes"] = {"archetypes": {"in": len(arcs), "out": len(out_arcs)}, "adult_gated": {"in": 0, "out": sum(1 for a in out_arcs if a["min_band"] == "18+")}}
for a in out_arcs:
    if a["min_band"] == "18+":
        exclude("archetypes", a["id"], a["name_ar"], "age_gated_18plus", "نمط مؤجل لفئة 18 فما فوق (جريمة قتل خارج الشاشة، مستوى عنف V3)؛ يظهر للبالغين فقط.")

# ------------------------------------------------------------------ output bookkeeping
dump("excluded.json", dict(version="1.0.0", note_ar="عناصر لم تُعرض أو عُرضت للبالغين فقط، مع السبب. لم يُحذف شيء بصمت.", items=EXCLUDED))
dump("counts.json", dict(version="1.0.0", counts=COUNTS))
for p, d in COUNTS.items():
    print(p, {k: f"{v['in']}→{v['out']}" for k, v in d.items()})
print("excluded entries:", len(EXCLUDED))
