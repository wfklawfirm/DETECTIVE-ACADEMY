#!/usr/bin/env python3
# Builds content/knowledge/{ko.json,sources.json,ko_names.json} from the research library (reference data).
# Usage: build_knowledge.py <LIBRARY_ROOT> <OUT_DIR>
import json, glob, os, sys, collections
LIB, OUT = sys.argv[1], sys.argv[2]
KO = os.path.join(LIB, "12_KNOWLEDGE_OBJECTS")
PUBLIC = {"forensic_concept", "reasoning_skill", "narrative_pattern"}      # shown to players
EXTRA = {
  "forensic_concept": ["discipline", "what_it_can_show", "what_it_cannot_show", "error_sources", "tv_myth", "safe_simulation", "reliability_note", "scientific_difficulty"],
  "reasoning_skill": ["operational_definition", "common_errors", "evidence_strength", "transfer_notes"],
  "narrative_pattern": ["plot_type", "mystery_principle", "fairness_criterion", "athar_use", "strengths", "weaknesses"],
  "case_mechanic": ["user_action", "state_change", "evidence_output", "learning_value", "mobile_fit", "risks"],
  "character_design_pattern": ["narrative_function", "risks"],
  "learning_assessment": ["educational_claim", "observable_behavior", "task_design", "risks"],
  "product_opportunity": ["gap", "mvp_priority", "defensibility"],
}
kos = []
for f in sorted(glob.glob(os.path.join(KO, "*.jsonl"))):
    if "rag_chunks" in f: continue
    for l in open(f, encoding="utf8"):
        if not l.strip(): continue
        d = json.loads(l)
        o = {k: d.get(k) for k in ("ko_id", "type", "name", "name_ar", "summary_ar", "source_ids", "confidence", "status", "tags", "age_band", "library")}
        o["name_ar"] = o["name_ar"] or o["name"]
        o["audience"] = "player" if d["type"] in PUBLIC else "studio"
        o["extra"] = {k: d[k] for k in EXTRA.get(d["type"], []) if d.get(k) not in (None, "", [])}
        kos.append(o)
kos.sort(key=lambda o: o["ko_id"])
cited = {s for o in kos for s in o["source_ids"]}
src = []
for l in open(os.path.join(LIB, "01_SOURCE_CATALOG", "sources_master.jsonl"), encoding="utf8"):
    if not l.strip(): continue
    d = json.loads(l)
    src.append({"id": d["source_id"], "title": d["title"], "title_ar": d.get("title_ar"), "authors": d.get("authors") or [], "year": d.get("year"),
                "type": d.get("type"), "url": d.get("url"), "rights": d.get("rights_status"), "license": d.get("license"),
                "grade": d.get("evidence_grade"), "library": d.get("library"), "cited": d["source_id"] in cited})
os.makedirs(OUT, exist_ok=True)
json.dump({"version": "1.0.0", "generated_from": "ATHAR_LIBRARY_v2_CORE/12_KNOWLEDGE_OBJECTS", "items": kos}, open(os.path.join(OUT, "ko.json"), "w", encoding="utf8"), ensure_ascii=False, indent=0)
json.dump({"version": "1.0.0", "generated_from": "ATHAR_LIBRARY_v2_CORE/01_SOURCE_CATALOG/sources_master.jsonl", "items": src}, open(os.path.join(OUT, "sources.json"), "w", encoding="utf8"), ensure_ascii=False, indent=0)
json.dump({o["ko_id"]: o["name_ar"] for o in kos}, open(os.path.join(OUT, "ko_names.json"), "w", encoding="utf8"), ensure_ascii=False, indent=1)
print(len(kos), collections.Counter(o["type"] for o in kos), len(src), sum(s["cited"] for s in src))
