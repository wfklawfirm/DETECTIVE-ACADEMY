# Agent report — 06_COGNITIVE_SCIENCE

**Date:** 2026-10-27 · **Source ID block used:** ATH-SRC-0500 … ATH-SRC-0566 · **KO lib code:** 06

## 1. Counts

| Item | Count |
|---|---|
| Source records in `sources.jsonl` | **67** (target 35–45; exceeded) |
| — of which `review_status: verified` | 58 |
| — of which `needs_expert_review` (record exists, but content/details not fully extracted) | 9 (0525, 0535, 0536, 0537, 0542, 0545, 0551, 0557, 0564) |
| Evidence grades | A: 9 · B: 50 · C: 6 · D: 2 |
| Deep analysis cards | **8** (0500, 0506, 0511, 0518 [+0517], 0523 [+0519–0522], 0524, 0528, 0531 [+0530]); ~585–660 words each |
| Knowledge objects | **31** = 24 `reasoning_skill` (KO-RS-06-001…024) + 7 `learning_assessment` (KO-LA-06-001…007) |

All JSONL lines were validated with Python: valid JSON, unique IDs, allowed enum values, every `supports`/`conflicts_with`/`source_ids` reference resolves to the catalog, and every OPEN_LICENSE record has a `license`.

## 2. Files produced

- `06_COGNITIVE_SCIENCE/REASONING_SKILLS_TAXONOMY.md`: 24 sub-skills in 6 domains, each with an operational definition, task pattern, assessment, observable evidence and confidence level; plus an age-band map.
- `06_COGNITIVE_SCIENCE/COGNITIVE_BIAS_CASE_LIBRARY.md`: 17 biases plus an explicit "do not use" list (social priming, ego depletion). Each bias has its research and replication status, a fair elicitation, a debrief and a measure of change. Includes binding rules and a season-1 sequence.
- `06_COGNITIVE_SCIENCE/CRITICAL_THINKING_ASSESSMENT_FRAMEWORK.md`: an instrument map (Watson-Glaser, HCTA, CAT, CART, CRT, H&B task batteries, CCTST, Cornell, COR, conceptual frameworks), 7 design lessons, a layered ATHAR assessment design, a 7-stage validation plan, and a licensing decision table.
- `06_COGNITIVE_SCIENCE/LEARNING_TRANSFER_RESEARCH.md`: answers the core question. It covers the evidence for and against transfer, why players memorize patterns, 10 design principles with confidence levels, and a transfer-measurement plan.
- `06_COGNITIVE_SCIENCE/cards/ATH-SRC-0500.md`, `0506`, `0511`, `0518`, `0523`, `0524`, `0528`, `0531`
- `06_COGNITIVE_SCIENCE/_data/sources.jsonl`, `_data/knowledge_objects.jsonl`, `_data/agent_report.md`

## 3. Search strategy

1. Six WebSearch calls (standard) confirmed the anchor works: T&K 1974, the Doyen priming replication, Many Labs 1, the Schimmack R-Index critique, the Hagger ego-depletion RRR, and the TFS bibliographic record. **After that, the shared 200-search turn budget was exhausted by other agents**, so no further WebSearch was possible.
2. Verification continued by WebFetch against authoritative records: Crossref API (`api.crossref.org/works/<DOI>` and `query.bibliographic`), OpenAlex (abstract reconstruction), Semantic Scholar API, ERIC, publisher pages (PLOS, AEA, Annual Reviews, Routledge, City Univ. repository, APS), official product/organisation pages (TalentLens, Schuhfried, Tennessee Tech, criticalthinking.org, Digital Inquiry Group, ALA/ACRL), the Stanford Encyclopedia of Philosophy, and Open Library ISBN records.
3. Rule: a record enters `sources.jsonl` only when its DOI, catalog or official page was fetched this session. Content claims that come only from domain knowledge are labeled as such inside the record and set to `needs_expert_review`.

## 4. Blockers

- **WebSearch budget exhausted** after 6 searches (shared limit across agents). Arabic-language and very recent (2024–2026) literature could not be searched at all.
- **Hourly WebFetch budget exhausted** once (~00:40–01:00 local time); work resumed after the reset.
- Sites that refused fetching: PubMed/PMC (reCAPTCHA), the MIT Press page (robots), Insight Assessment product pages (client error), criticalthinking.net test pages (client error), the Cambridge Core book page, some Crossref query endpoints, and the U-Michigan Deep Blue PDF.
- Publisher-elided abstracts (APA journals in Semantic Scholar/OpenAlex) meant some effect sizes could not be extracted: McDowell & Jacobs pooled estimates, Barnett & Ceci dimension names, Fong et al. results, and Toplak 2011 CRT results.

## 5. Unverified candidates (NOT in sources.jsonl)

| Candidate | Why not verified |
|---|---|
| California Critical Thinking Skills Test (CCTST) / CCTDI — Insight Assessment product pages | Product page fetch failed; home page does not name the tests |
| Cornell Critical Thinking Tests (Levels X, Z); Ennis-Weir Critical Thinking Essay Test | criticalthinking.net test-list page failed to load |
| Ennis (1987/1996/2011) definitions of CT ("reasonable reflective thinking…"), *Critical Thinking* (1996, Prentice Hall) | Not searchable after budget exhausted |
| Paul & Elder, *Critical Thinking: Tools for Taking Charge of Your Learning and Your Life* (Pearson) | Crossref query failed |
| Baron, *Thinking and Deciding* 5th edition (2023?) | Could not confirm whether a newer edition exists (4th edition is cataloged) |
| Argument-mapping meta-analysis (e.g., Alvarez Ortiz 2007 thesis, University of Melbourne) | No search budget |
| Haran, Ritov & Mellers (2013) on actively open-minded thinking and calibration | Crossref query was rate-limited |
| Lewandowsky & van der Linden (2021) review "Countering misinformation and fake news through inoculation and prebunking" | Crossref returned an unrelated item |
| Roozenbeek/van der Linden reply to Modirrousta-Galian & Higham (2023) | Not found in the query results; Leder et al. 2024 was found instead and cataloged |
| Many Labs 3–5; Stanford/DIG lateral-reading effect sizes (McGrew et al. 2019 BJEP; Axelsson et al. 2021) | No search budget |
| Kahneman, Sibony & Sunstein *Noise*; Kahneman & Klein 2009 "Conditions for intuitive expertise" | No search budget |
| Evans / Johnson-Laird work on the psychology of deductive reasoning | No search budget (logged as a taxonomy gap) |
| Any Arabic-language CT instrument or Arab-sample replication of H&B effects | No search budget; a priority for team 08 |

## 6. Top 5 findings that should change ATHAR's design

1. **Puzzle-solving alone will not transfer.** Far transfer of general abilities from domain practice (chess, music, working-memory training) shrinks to near zero with active controls [ATH-SRC-0533]. What does transfer is *explicitly taught, named principles* practiced with personalized feedback. One serious-game session cut biases by roughly 24–32% for 2+ months [ATH-SRC-0517], and it cut confirmatory choices by 29% in an unannounced field case [ATH-SRC-0518]. → Every case needs an explicit principle, a personalized debrief, varied surfaces, and spaced re-encounters. Learning is judged only on unannounced, different-surface cases weeks later.
2. **Measure discernment, not rejection.** Reanalysis of the Bad News/Go Viral! studies showed the games mainly made players distrust everything [ATH-SRC-0523]. Adding feedback exercises on both true and false items restored discernment [ATH-SRC-0560]. → Score every credibility task with signal detection, include genuine "suspicious-looking" evidence, and report skepticism bias to the player.
3. **Choose biases by replication status.** Anchoring replicated in every Many Labs sample, with effects larger than the original [ATH-SRC-0504]. Social priming and ego depletion failed [ATH-SRC-0503][ATH-SRC-0505], and Kahneman conceded his priming chapter over-trusted weak studies [ATH-SRC-0502]. → Build no mechanics on non-replicated effects, and plan for published effects shrinking (median d 0.60 → 0.15 in Many Labs 2 [ATH-SRC-0561]).
4. **Present probabilistic evidence as natural frequencies with visuals, and teach representation, not formulas** [ATH-SRC-0506][ATH-SRC-0507][ATH-SRC-0508]. But always make the reference class explicit, or the "correct" answer is contestable and the case is unfair [ATH-SRC-0510].
5. **Reasoning quality is not intelligence.** Myside bias barely correlates with IQ [ATH-SRC-0514], and rational-thinking skills are still developing in the 13–18 age range [ATH-SRC-0515]. → Report a profile of separate skills, never a single "detective IQ". Put myside and motivated-reasoning challenges at every difficulty tier. Use structured dialogue (the strongest teen-specific transfer evidence here [ATH-SRC-0558]) for argument skills.

## 7. Top 5 open questions / gaps for expert review

1. **No Arab or adolescent replication data** for any bias or debiasing effect in this catalog. ATHAR needs its own pilot with a partner university, using an active-control design (KO-LA-06-006).
2. **Psychometrics of in-game measurement:** how many items per player are needed for stable discernment (d′) and calibration estimates? What agreement threshold should apply to LLM scoring of Arabic and dialect justifications?
3. **Full-text checks needed:** Barnett & Ceci's 9 dimensions; Abrami 2008 results by Ennis category; McDowell & Jacobs pooled effects; Fong et al. 1986 transfer results; the Delphi report's skill list; Kuhn 1991 claims.
4. **Licensing:** whether HCTA/Watson-Glaser/CART can be licensed for an external-validity study, and which Civic Online Reasoning items are CC BY 4.0 and can be adapted into Arabic.
5. **Ethics of eliciting bias in minors:** how much "trap" and emotional attachment (motivated-reasoning cases) is acceptable for ages 13–15. This needs review with team 11 (rights & safety) and team 08 (culture), especially to avoid stereotypes in representativeness cases.

## 8. Cross-team notes

- Gentner et al. 2003 (analogical encoding, ATH-SRC-0563) and the spacing/interleaving claims are canonically owned by Learning Science (07); they are cataloged here only because the transfer rules depend on them.
- Blind/instrumented measurement (RS-03, B16) should be coordinated with Forensic Science (04).
- Lateral reading in Arabic information ecosystems (WhatsApp, Telegram, TikTok) needs input from team 08.

## Gap-fill round (2026-10-27)

**New records (9):** ATH-SRC-0567–0575. Catalog now 76 records. `needs_expert_review`: 9 → 2 (0545 Baron, 0557 Kuhn: books with no abstract).

| ID | Source | Verification |
|---|---|---|
| 0567 | CCTST official product page (Insight Assessment) | Fetched. 40 items, 55 min, 8 skills, college-calibrated, vendor calls it "legacy". **Vendor lists an Arabic version.** |
| 0568 | Ennis, criticalthinking.net test list (Cornell X/Z, Ennis-Weir) | Fetched. **Cornell Level X covers grades 4–14.** |
| 0569 | Ennis-Weir 2005 supplement (norms, reliability) | Official PDF. Inter-rater about .72–.99 in high school and college. |
| 0570 | Bataineh & Zghoul 2006 (Cornell Z, Jordanian sample) | ERIC + Crossref DOI |
| 0571 | Fawkes et al. 2005 critique of CCTST content (9/34 items defective) | ERIC + Crossref DOI |
| 0572 | Lin et al. 2026 meta-analysis of argument-visualisation tools | ERIC abstract. Journal DOI not confirmed; preprint DOI 10.2139/ssrn.5643672 exists. |
| 0573 | Nesbit & Liu 2025 systematic review of argument mapping | ERIC + Crossref DOI |
| 0574 | Swaryandini et al. 2025, *Nat Hum Behav*, meta-analysis of educational debiasing | PubMed abstract |
| 0575 | Simchon et al. 2026, SDT meta-analysis of inoculation | PubMed abstract |

**Changed records (→ `verified`, abstracts read):**
- **0525** Wineburg 2022: ERIC abstract. Matched-control design, n = 271 vs 228.
- **0535** Leary 2017: volume, issue and pages confirmed as 43(6) 793–813.
- **0536** Porter 2022: PubMed abstract.
- **0537** Flavell 1979: ERIC abstract.
- **0542** Byrne: OpenAlex abstract.
- **0551** Toplak 2011: PubMed abstract. The CRT is a unique predictor beyond ability.
- **0564** Fong 1986: ERIC abstract. Effect sizes still not extracted.

**Conclusions changed:**
1. **Top finding #2 (discernment, not rejection) is now contested, not settled.** A 2026 SDT meta-analysis of 33 experiments reports improved discrimination with **no** shift in response bias [0575]. Some of its authors are intervention developers, which is declared. It conflicts with 0523. The design rule is kept, because measuring discrimination and bias separately is how ATHAR's own data would settle the question. The framework, bias library and transfer document now say this.
2. **Expected debiasing effects are smaller.** The 2025 meta-analysis of 54 RCTs gives g = 0.26 [0574], with all studies at unclear or high risk of bias and representativeness hard to shift. Morewedge's 24–32% [0517] is now framed as an optimistic ceiling.
3. **Argument mapping:** the bias-adjusted g is about 0.87, but gains show mostly in argumentative-essay quality, not in standardised critical-thinking tests [0572]. Only higher-education samples exist.
4. **Assessment map:** the CCTST and Cornell/Ennis-Weir rows are no longer "unverified". Cornell X is the only verified critical-thinking test whose stated range covers ages 13–15. The CCTST is the only verified external measure with an Arabic version, adults only.

**Deliverables edited:**
- `CRITICAL_THINKING_ASSESSMENT_FRAMEWORK.md`: instrument rows, Lesson 4, gap 1.
- `COGNITIVE_BIAS_CASE_LIBRARY.md`: rules 4–5.
- `LEARNING_TRANSFER_RESEARCH.md`: tables 3.1/3.2, open questions 4–5.
- `REASONING_SKILLS_TAXONOMY.md`: RS-02, RS-15, RS-16, RS-18 sources.

**Still open:**
- Cornell publisher page (blocked by a JavaScript gate) and Cornell/CCTST Arabic licensing.
- Alvarez Ortiz 2007 thesis (not found in ERIC).
- Lewandowsky & van der Linden 2021, and Haran et al. 2013 (Crossref rate-limited; not retried).
- Baron 5th edition.
- Any Arabic critical-thinking instrument or Arab-adolescent replication: still none found.
