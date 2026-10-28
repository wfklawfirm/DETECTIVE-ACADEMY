# Agent Report — 08_ARAB_AUDIENCE_AND_CULTURE

**Date:** 2026-10-27 · **Source block used:** ATH-SRC-0700 … ATH-SRC-0746 (47 IDs; 0747–0799 free)

## Counts

| Item | Count | Target |
|---|---|---|
| Sources verified (`sources.jsonl`) | **47** (of which 11 flagged `needs_expert_review`: bibliographic record verified, but content or findings not read) | 25–35 |
| Deep cards | **6** (0701, 0707, 0710, 0719, 0721, 0725) | 4–6 |
| Knowledge objects | **15**: 7 PO, 4 CD, 4 NP | 5–8 PO, 3–5 CD, 3–5 NP |

Evidence grades: A 4 · B 16 · C 16 · D 11 · E 0.

## Files produced

- `ARAB_AUDIENCE_RESEARCH.md`
- `ARABIC_MYSTERY_WORLD_BUILDING.md`
- `AGE_APPROPRIATE_CONTENT_POLICY.md`
- `ARABIC_LANGUAGE_AND_DIALECT_STRATEGY.md`
- `LOCAL_STORY_OPPORTUNITIES.md` (25 original premises)
- `cards/ATH-SRC-0701.md`, `0707.md`, `0710.md`, `0719.md`, `0721.md`, `0725.md`
- `_data/sources.jsonl`, `_data/knowledge_objects.jsonl`, `_data/agent_report.md`

All JSONL lines were validated as JSON. Allowed enum values were checked. Every `[ATH-SRC-…]` cited in the Markdown exists in the catalog, and every catalog record is cited at least once.

## Search strategy

1. Searched in English and Arabic (extended mode for Arabic and recent data): ASDA'A BCW, NU-Q, DataReportal, Niko Partners, Saudi/UAE rating systems, and the Saudi gaming strategy.
2. Fetched official pages directly: DataReportal country reports (7), the Niko Partners Substack, SPA, Gulf News, ESRB, QDL, UNESCO, WHR 2026, SSRN, and the Arab Youth Center.
3. Checked academic records through the **Crossref API** (DOI metadata) and publisher pages: Ferguson, Saiegh-Haddad ×3, Abu-Rabia, Ibrahim and Aharon-Peretz, Di Giovanni, Shaheen, Saleem et al. ×2, Harrison and Cantor, Livingstone and Helsper, Portelli, Al-Khalili, Tbakhi and Amr.
4. Used Wikipedia **only for bibliographic facts** about Arab Netflix series and authors.

## Blockers

- **The WebSearch budget (shared, 200 per turn) ran out early**, after about 20 of my searches. The **WebFetch budget (shared, 800 per hour) ran out next.** About 50% of the planned coverage could not be searched, and I did not try any workarounds.
- `pegi.info` blocks automated fetching (robots), so PEGI is used as a general reference only.
- `mideastmedia.org` (NU-Q) was under maintenance, so newer editions after 2018 could not be checked.
- `arabyouthsurvey.com` redirects to Burson MENA. No edition after 2023 (the 15th) was found.
- The Vision 2030 HCDP page returned only a meta description. Full texts of academic papers are behind paywalls (abstracts only).
- The IFCN signatory list loads by JavaScript, so Misbar's IFCN status is unconfirmed.

## Unverified candidates (not in the catalog)

| Candidate | Why not verified |
|---|---|
| ASDA'A BCW Arab Youth Survey 16th (2024) and 17th (2025) editions | No evidence found that they exist; the series may have stopped |
| NU-Q *Media Use in the Middle East* 2019–2025 editions (incl. entertainment and youth chapters) | Site under maintenance; search budget exhausted |
| Newzoo MENA games reports; PwC Global Entertainment & Media Outlook ME | Search budget exhausted |
| Saudi National Gaming & Esports Strategy official document (2022), GDP and jobs targets | Only secondary journalism (Al Jazeera) verified; Arab News article fetch failed |
| Saudi GAMR official age-rating guide (categories and descriptors) | Fetch budget exhausted; categories confirmed only from secondary sources |
| UAE Media Council official classification criteria (uaemc.gov.ae) | Not fetched |
| PEGI official descriptors | robots-blocked |
| PIRLS 2021 Arab country scores | Results page lacked the exhibit data |
| Arabic mystery, true-crime or science creators (beyond the existence of the Da7ee7 channel and Thmanyah) | Search budget exhausted; **no names listed without verification** |
| Arab parental-mediation studies; ministry critical-thinking curricula (KSA, UAE, Egypt, Jordan, Morocco) | Search budget exhausted |
| Bibliotheca Alexandrina manuscript collections (detail and reuse terms); Al-Qarawiyyin library digitisation | Only the BA index page was fetched |
| Arab fact-checkers Fatabyyano, Matsda2sh, Akeed, AFP Arabic | Not searched |
| Iftah Ya Simsim (MSA children's TV) | Fetch budget exhausted |
| Arab Youth Priority Survey 2026: actual findings | Landing page only |

## Top 5 findings that should change ATHAR's design

1. **"Puzzle is #1 on mobile" is not evidence of demand for narrative deduction.** Industry puzzle categories are mostly casual. The design response is a daily micro-puzzle bridge into long cases, and Arab mystery-game demand stays an open question [ATH-SRC-0719].
2. **Arabic-first must earn its place.** 54% of 18–24-year-olds say Arabic matters less to them than to their parents [ATH-SRC-0707]. Use simplified MSA narration plus lightly dialect-coloured dialogue, and keep comprehension separate from reasoning in assessment, since diglossia carries a processing cost [ATH-SRC-0701] [ATH-SRC-0702].
3. **Backlash triggers are romance, profanity and "misrepresenting our society", not mystery or mild crime** [ATH-SRC-0738] [ATH-SRC-0740] [ATH-SRC-0720]. Design 13–15 content to pass Saudi and UAE "12" ratings without edits, with no romance. Saudi reviewers also check background art and music [ATH-SRC-0722].
4. **Extreme regional asymmetry:** UAE ARPU is $84.60 and Egypt's is $3.39, and Egypt has 20.6M people offline [ATH-SRC-0719] [ATH-SRC-0714]. ATHAR needs two-tier pricing with wallet or carrier billing, plus light, low-data builds.
5. **Heavy social-media use is linked (correlationally) to worse wellbeing among Arab Gen Z** [ATH-SRC-0710]. Use bounded sessions and no public leaderboards for 13–15, and add a verification case line. Do not claim health benefits.

## Top 5 open questions / gaps for human or expert review

1. **No representative data on Arab 13–17-year-olds** (digital use, gaming, reading). Every verified survey starts at 15+ or 18+, and field research is required.
2. Do Saudi, UAE and Egyptian game age-rating rules apply to **educational interactive apps**? (→ library 11 / legal counsel)
3. Simplified MSA versus dialect dialogue: is there any evidence on **teens'** comprehension and enjoyment? Run an A/B text test across four capitals.
4. Do Arab parents and schools accept "teen investigators" and off-screen death in the 16–18 band? This needs focus groups.
5. Verify the regional creator landscape (mystery, true crime, science) and fact-checkers, and their legal-risk exposure (the creator prosecutions in Egypt in 2025 [ATH-SRC-0711]).

## Notes for the merge step

- Possible overlaps: ESRB [ATH-SRC-0724] and stereotype/media-effects papers may also be catalogued by library 11 or 06. Livingstone & Helsper [ATH-SRC-0729] → library 11 or 07. Ibn al-Haytham sources → possibly library 05 or 06.
- **A data error was fixed after writing:** in `ARAB_AUDIENCE_RESEARCH.md` §6, the identity row is now set out per region (GCC religion 25% / family 20%; Levant 30% / 21%; North Africa 27% / 37%), as reported in Communicate Online's coverage of the 15th survey.

## Gap-fill round (2026-10-27)

**Agent:** gap-filling researcher (Arabic and Arab-region evidence). **Method:** WebSearch (standard and extended, Arabic and English) used sparingly. Records were verified through WebFetch of official pages, the Crossref and arXiv APIs (curl, so no web quota), the GAMR public CMS API (`/api/public/pages/age-classification`), the MediaWiki API for Arabic Wikipedia (bibliographic facts only), and direct PDF download for the MOE study-plans guide and the UNICEF Innocenti tables, both read with pdftotext.

### Counts
- **New verified sources: 40 (ATH-SRC-0747 … 0786).** The 08 catalogue now has 87 records (0700–0786; 0787–0799 free). 39 are `verified`; 0760 is `needs_expert_review`.
- New grades: A 3 (0749, 0752, 0758) · B 13 · C 12 · D 11 · E 1 (0760). Whole catalogue: 77 `verified` and 10 `needs_expert_review` (previously 11; 0708 and 0745 were promoted and 0760 was added).
- **New deliverable:** `ARABIC_LANGUAGE_RESEARCH_EVIDENCE.md` (Arabic; 5 evidence strands, each with implications for ATHAR's assessment and content).
- **Edited deliverables:** `ARAB_AUDIENCE_RESEARCH.md` (header, exec summary items 6–7, §2 table rows, §3 teen-gaming evidence, §5 creators table, §7 parents and curricula, §8 data-gaps list rewritten with ✅/◐/✗ status, §9 recommendations 4–6) and `AGE_APPROPRIATE_CONTENT_POLICY.md` (official Saudi descriptors, Saudi film scale, UAE 2018/2025 updates, new "crime must have consequences" rule, trailer rule, parent-tool rule, checklist items, open question 2).
- No knowledge objects or cards were added. The KO file was left unchanged.

### Changes to existing records (logged)
| ID | Change |
|---|---|
| ATH-SRC-0708 | `needs_expert_review` → `verified`. The top-5 priority ranking for 2026 was added from 0769 (WAM). Limitation narrowed: percentages remain unverified |
| ATH-SRC-0721 | Limitation corrected: the categories are now confirmed on the official GAMR page (0752), so they no longer rest on secondary sources only |
| ATH-SRC-0742 | `publisher` changed from null to Modern Arab Association (Arabic Wikipedia). Birth and death dates and the 1984 competition / first *Malaf al-Mostaqbal* issue added |
| ATH-SRC-0745 | `needs_expert_review` → `verified`. Host (Ahmed El-Ghandour), 2014 start and 2021 reach added from 0767/0768 |

### Task A: audience data, findings and status
- **Arab Youth Survey after 2023:** none found in two further searches. PSB Insights (0770) says it led the survey 2008–2022; the 2023 edition was run by SixthFactor. Treat 2023 (0707) as the latest edition, and assume the series is paused (not confirmed by Burson).
- **NU-Q:** 2019 wave (0747) and 8th wave 2021–22 (0748: N=7,382 adults 18+, CATI telephone interviews, gaming chapter showing about 40% play and phone-first play). No wave after 2022 was found.
- **13–17 representative data:** UNICEF Innocenti 2025 tables (0749) with PISA 2022 / PIRLS 2021 home-internet access by SES for KSA, UAE, Qatar, Jordan, Morocco, Palestine, Egypt and others. Disrupting Harm has no named Arab country yet. Non-representative teen gaming studies: Jordan (0750) and Lebanon (0751). **Still missing:** representative time-use, genre and reading data. ITU youth-by-region data was not on the fetched page.
- **Ratings:** official GAMR page (0752; Arabic and English text; last modified 2026-09-14). The UAE remains secondary only (0753 for 2018, 0754 for 2025): uaemc.gov.ae is robots-blocked and failed TLS validation through the proxy. TLS checks were not bypassed.
- **Parents:** Saudi Arabia 0755 (technical mediation is associated with *more* cyberbullying), Qatar 0756, UAE 0757. Egypt and the Levant are still missing.
- **Curricula:** KSA confirmed by the official MOE guide (0758): a Critical Thinking subject for grade 9 and the first secondary year from 1443H. The 2018 pilot is documented in 0759. The reported 1448H expansion (0760) comes from an aggregator and needs review. UAE (0761) places critical thinking inside Moral Education. Jordan (0762) integrates it into science and maths. Qatar (edu.gov.qa robots-blocked), Egypt and Morocco are not verified.
- **Creators:** 0763–0768 (Ahraz/Sowt, Sky News Arabia *Evidence*, *Al-Qissa al-Kamila*/Sameh Sanad, Da7ee7, Egycology/Dystopia/Al-Esbetalia). Current audience metrics are not verified.

### Task B: cross-library Arabic evidence
- CT instruments: 0771 and 0772. **No verified Arabic CCTST or CRT validation** after two searches. Arabic CCTST studies (Jordan, via e-Marefa; Iraq, via Shamra) were seen in results, but e-Marefa is robots-blocked and Shamra lacks journal metadata, so they are not catalogued. The Saudi nursing CT-disposition study (SAGE Open Nursing 2024, DOI 10.1177/23779608241296069) was verified but not catalogued (adult disposition scale, low relevance).
- AES and LLM grading: 0773–0777. **No study directly testing dialect vs MSA effects on automated grading** was found (2 attempts). The gap is recorded.
- Arabic NLP benchmarks: 0778–0782 (ArabicMMLU, DialectalArabicMMLU, EDRAC, DAR-MGSM, AraDiCE).
- Forensic education: 0783 (AJFSFM via Crossref journal record; ISSN 1658-6786) and 0784 (NAUSS MSc page). No civilian or school-level Arab forensic education was found.
- Interactive fiction: 0785 (Wojdan, 2016) and 0786 (itch.io snapshot, 24 Arabic VNs).

### Unverified candidates added in this round
| Candidate | Reason |
|---|---|
| Arab Youth Survey 16th/17th editions | Not found after 4 searches total; presumed paused |
| NU-Q wave after 2022 | Not found |
| UAE Media Council official classification descriptors | robots-blocked; TLS chain failure via proxy |
| Qatar National Curriculum Framework competencies | edu.gov.qa robots-blocked |
| Saudi 1448H study-plans guide (6th edition) | MOE URLs for 1446–1448 return HTML, not PDF; only the aggregator report (0760) |
| Arabic CCTST validations (Jordan: e-Marefa BIM-297075; Iraq: University of Baghdad, Rasch model) | Catalogue pages blocked or lacking metadata |
| Arabic CRT validation | Not found (2 attempts) |
| Dialect vs MSA effect on automated scoring of student answers | Not found (2 attempts). Recorded as a research gap |
| ITU Facts and Figures, Arab States youth (15–24) internet use | Regional figure not on the fetched page |
| Disrupting Harm North-Africa country reports | Countries anonymised pending national reports |
| Peer-reviewed parental mediation studies in Egypt, the Levant and the Maghreb | Not searched after budget prioritisation |
| *Communication & Society* and *Qscience* article pages | Bot-protection or site errors; verified via Crossref instead |

### Top findings that change ATHAR's design (round 2)
1. **The Saudi rating rule turns "no glorified crime" into a compliance requirement:** crime shown positively or without consequences means a 16+ rating (0752). Every case ending must show consequences.
2. **Saudi Arabia has a compulsory Critical Thinking school subject** for ages ~14–15 (0758). This is the clearest B2B/B2G entry point; obtain the course outcomes before claiming alignment.
3. **Do not let a general LLM grade Arabic free text.** Fine-tuned small models beat LLMs (QWK 0.88 vs 0.67), and trait-level LLM agreement is low (0.28) (0775, 0776). V1 scoring should rest on structured evidence tasks.
4. **Parent tools should open a conversation, not a surveillance view.** Technical mediation is linked to worse outcomes in a Saudi sample (0755).
5. **Equity:** about 30% of the poorest 15-year-olds in Jordan, Morocco and Palestine lack home internet (0749), so offline or low-data case packs are needed.
