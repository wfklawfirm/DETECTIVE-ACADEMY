# ATHAR Research Protocol — shared rules for every research team

This file is binding for every library team. Read it fully before starting.
Project root: `/home/claude/ATHAR_RESEARCH_LIBRARY`
Original brief (Arabic): `00_PROJECT_CONTROL/MASTER_PROMPT_ORIGINAL.md`
Today's date: 2026-10-27 (use it as `verified_at`).

---

## 1. Non‑negotiables

1. **No fabrication.** A source enters the catalog only if you confirmed it exists during this session, through WebSearch results or a WebFetch of an authoritative page (publisher, DOI landing page, journal, official org site, library catalog, developer/official product page, government site, Wikipedia only for basic bibliographic facts of literary works/games). Record the page you used in `verification_url`. If you cannot confirm it, it goes in your `_data/agent_report.md` under "Unverified candidates", never in `sources.jsonl`.
2. **Never invent** DOIs, ISBNs, years, page numbers, prices, user counts, study results or quotations. Unknown → `null` and say so.
3. **Copyright.** Write findings in your own words. At most ONE direct quote per source, under 15 words, in quotation marks, only when exact wording matters. Never reproduce passages, plot text, dialogue, lyrics or poems. For copyrighted novels: bibliographic data + official link + your own analytical summary only. No piracy sites, no shadow libraries, no bypassing paywalls.
4. **Safety.** No operational instructions for committing crimes, poisoning, weapons, hiding evidence, defeating forensic methods, coercive interrogation, or evading detection. Forensic material stays at the level of principles, interpretation, limits and safe virtual simulations with fictional data. No gore/real-victim imagery suggestions for teens.
5. **Separate claim types** in every analytical document. Tag statements when it matters:
   - `[حقيقة موثقة]` documented fact (with source IDs)
   - `[تفسير بحثي]` research interpretation
   - `[افتراض تصميمي]` design assumption / hypothesis for ATHAR
   - `[استنتاج استثماري]` business/investment inference
6. **Be critical.** Report contradicting evidence, replication problems, criticisms, competitor strength — even when it weakens ATHAR's novelty.
7. **No filler.** Generic, repetitive prose is worse than a shorter accurate file. Every section should change a product, design, or research decision.

## 2. Language

- Analytical Markdown deliverables: **Modern Standard Arabic**, with standard English terms in parentheses on first use (e.g. الاستدلال الافتراضي (Abductive reasoning)). Source titles, product names and author names stay in their original language.
- Data files (`.jsonl`, `.csv`): **English keys**; values in concise English, plus Arabic fields where the schema has `_ar`.
- Write RTL-friendly Markdown: headings, short paragraphs, tables where they help. Cite inline as `[ATH-SRC-0123]`.

## 3. Source IDs — your reserved block

Each team uses ONLY its own block, sequentially, zero-padded to 4 digits:

| Team | Folder | Source ID block | KO lib code |
|---|---|---|---|
| Detective literature | 02_DETECTIVE_LITERATURE | ATH-SRC-0100 … 0199 | 02 |
| Narrative & game design | 03_NARRATIVE_AND_GAME_DESIGN | ATH-SRC-0200 … 0299 | 03 |
| Forensic science | 04_FORENSIC_SCIENCE | ATH-SRC-0300 … 0399 | 04 |
| Investigative reasoning | 05_INVESTIGATIVE_REASONING | ATH-SRC-0400 … 0499 | 05 |
| Cognitive science | 06_COGNITIVE_SCIENCE | ATH-SRC-0500 … 0599 | 06 |
| Learning science | 07_LEARNING_SCIENCE | ATH-SRC-0600 … 0699 | 07 |
| Arab audience & culture | 08_ARAB_AUDIENCE_AND_CULTURE | ATH-SRC-0700 … 0799 | 08 |
| Competitors — global | 09_COMPETITIVE_INTELLIGENCE | ATH-SRC-0800 … 0899 | 09 |
| Technical architecture | 10_TECHNICAL_ARCHITECTURE | ATH-SRC-0900 … 0999 | 10 |
| Rights, privacy & safety | 11_RIGHTS_PRIVACY_AND_SAFETY | ATH-SRC-1000 … 1099 | 11 |
| Competitors — Arab/MENA | 09_COMPETITIVE_INTELLIGENCE | ATH-SRC-1100 … 1199 | 09A |

Overlaps are expected (e.g. the NAS 2009 report may matter to several teams). Catalog what you use; the merge step de-duplicates by DOI/ISBN/URL/title and remaps IDs. Canonical owners for well-known overlaps: NAS 2009 & PCAST 2016 → forensic; Kahneman/Tversky → cognitive; Evidence-Centered Design (Mislevy et al.) → learning; Knox/Van Dine rules → literature; College of Policing guidance → investigative; COPPA/GDPR/children's codes → rights. If you are not the owner, you may still catalog it in your block.

## 4. Files every team must write

```
<YOUR_FOLDER>/
  <deliverable files named in the brief>.md / .csv
  cards/ATH-SRC-XXXX.md          # deep analysis cards for your most important sources
  _data/sources.jsonl             # one JSON object per line, schema §5
  _data/knowledge_objects.jsonl   # one JSON object per line, schema §6
  _data/agent_report.md           # counts, method, blockers, unverified candidates, gaps
```

Write `sources.jsonl` incrementally (append as you verify) so work survives interruption.

## 5. Source record schema (`_data/sources.jsonl`)

```json
{
  "source_id": "ATH-SRC-0301",
  "title": "Strengthening Forensic Science in the United States: A Path Forward",
  "title_ar": null,
  "authors": ["National Research Council"],
  "publisher": "The National Academies Press",
  "year": 2009,
  "edition_version": null,
  "language": "en",
  "type": "report",
  "library": "04_FORENSIC_SCIENCE",
  "topics": ["forensic validity", "standards"],
  "url": "https://...",
  "doi": "10.17226/12589",
  "isbn": null,
  "verified_at": "2026-10-27",
  "verification_method": "fetched_official_page",
  "verification_url": "https://...",
  "evidence_grade": "A",
  "relevance": "high",
  "rights_status": "COPYRIGHTED_RESTRICTED",
  "rights_jurisdiction": null,
  "license": null,
  "legal_text_access": "free_official",
  "internal_storage_permission": "not_established",
  "commercial_reuse_permission": "no",
  "key_findings": ["paraphrased finding 1", "paraphrased finding 2"],
  "athar_applications": ["how ATHAR uses it"],
  "limitations": ["criticism / scope limits"],
  "supports": [],
  "conflicts_with": [],
  "age_band": null,
  "confidence": "high",
  "review_status": "verified",
  "deep_card": "04_FORENSIC_SCIENCE/cards/ATH-SRC-0301.md"
}
```

Allowed values:
- `type`: book | book_chapter | journal_article | conference_paper | report | standard | guideline | legal_text | game | game_talk_or_postmortem | interview | video | website | documentation | software_tool | dataset | thesis | course | product | news_article | market_report
- `verification_method`: fetched_official_page | doi_or_catalog_record | search_result_confirmed | publisher_page | wikipedia_bibliographic
- `evidence_grade`: A (standards, primary sources, strong systematic reviews/meta-analyses) | B (peer-reviewed research, academic books, recognized specialist references) | C (official product/company docs, documented professional practice) | D (expert analysis, opinion, user reports, journalism) | E (weak/unproven — keep only for review lists, never to assert scientific facts)
- `relevance`: high | medium | low
- `rights_status`: PUBLIC_DOMAIN | OPEN_LICENSE | LICENSED | COPYRIGHTED_RESTRICTED | UNKNOWN (PUBLIC_DOMAIN requires `rights_jurisdiction`, e.g. "US"; "life+50: LB, AE"; OPEN_LICENSE requires `license`, e.g. "CC BY 4.0")
- `legal_text_access`: free_official | open_access | public_domain_text | paywalled | purchase | not_applicable | unknown
- `internal_storage_permission` / `commercial_reuse_permission`: yes | no | not_established | not_applicable
- `confidence`: high | medium | low
- `review_status`: verified | needs_expert_review

Note: "free to read online" is NOT permission to store or reuse commercially.

## 6. Knowledge object schema (`_data/knowledge_objects.jsonl`)

Common fields for every object:
```json
{"ko_id": "KO-FC-04-001", "type": "forensic_concept", "name": "...", "name_ar": "...",
 "summary_ar": "2–4 sentence Arabic summary", "source_ids": ["ATH-SRC-0301"],
 "confidence": "high|medium|low", "status": "evidence_based|expert_practice|design_hypothesis",
 "tags": [], "age_band": "13-15|16-18|18+|all|null"}
```
ID format: `KO-<TYPE>-<LIBCODE>-<NNN>`. Types and their extra fields:

- `NP` narrative_pattern: plot_type, mystery_principle, information_distribution, surprise_mechanism, difficulty (1–5), fairness_criterion, strengths, weaknesses, athar_use
- `RS` reasoning_skill: operational_definition, practice_task_pattern, assessment_method, observable_evidence, common_errors, evidence_strength, transfer_notes
- `FC` forensic_concept: discipline, what_it_can_show, what_it_cannot_show, error_sources, tv_myth, safe_simulation, scientific_difficulty (1–5), reliability_note, expert_review_questions
- `CM` case_mechanic: user_action, state_change, evidence_output, example_titles, learning_value (1–5), excitement (1–5), tech_cost (1–5, 5 = expensive), mobile_fit (1–5), risks
- `LA` learning_assessment: educational_claim, observable_behavior, task_design, scoring_criteria, limitations, validation_needed
- `CD` character_design_pattern: narrative_function, motives, knowledge_scope, knowledge_boundaries, dialogue_rules, risks
- `PO` product_opportunity: gap, evidence, user_segment, edu_value (1–5), fun_value (1–5), competitors_present, defensibility (1–5), mvp_priority (must|should|later), risks

Every object must cite at least one `source_ids` entry from the catalog, OR be marked `"status": "design_hypothesis"` with an explanation in `summary_ar`.

## 7. Deep analysis cards (`cards/ATH-SRC-XXXX.md`)

Arabic, ~400–900 words each, structure:
```
# <Title> — بطاقة تحليل [ATH-SRC-XXXX]
- البيانات الببليوغرافية | الرابط | درجة الدليل | حالة الحقوق
## الفكرة المركزية
## أهم النتائج أو المبادئ (بصياغتنا)
## ما الذي لا يثبته هذا المصدر / حدوده والانتقادات
## مصادر داعمة أو معارضة
## التطبيق على ATHAR (قرارات تصميم ملموسة)
## أسئلة مفتوحة تحتاج خبيراً
```

## 8. Quality gates (apply before adding any record)

1. Source exists; link works or a catalog/DOI record confirms it; author/publisher/year correct; newer edition checked.
2. Claim actually supported by the source; contradicting evidence noted; no hype.
3. Rights status explicit; never assume reuse rights.
4. Product value: improves plot, learning, interaction, scientific accuracy — else leave it out.
5. Usable: organized, cross-linked by IDs, retrievable.

Records failing a gate: fix, mark `needs_expert_review`, or exclude.

## 9. `_data/agent_report.md` must contain

- Sources verified (count) / cards written / knowledge objects written
- Files produced (list)
- Search strategy used (short)
- Blockers (sites refused, paywalls, missing data)
- Unverified candidates (title + why not verified)
- Top 5 findings that should change ATHAR's design
- Top 5 open questions / gaps for human or expert review
