# Agent report — 09_COMPETITIVE_INTELLIGENCE (GLOBAL part)

**Date:** 2026-10-27 · **Source-ID block used:** ATH-SRC-0800 … ATH-SRC-0868 (69 IDs used; 0869–0899 free) · **KO code:** 09

## Counts
- Sources verified and catalogued: **69**. All are in `sources.jsonl`, and every line is valid JSON (checked with Python). Each was confirmed through a WebFetch of the official, store or press page, or through a Wikipedia page used only for basic game facts.
- Competitor and product records: **55** rows in `competitors_global.csv`. Each `source_ids` value resolves to a record in the catalog.
- Deep cards: **5**. They are ATH-SRC-0808 (CSI: Web Adventures), 0811 (Bad News / Go Viral!), 0819 (Hidden Door), 0822 (AI-interrogation games), and 0831 (Golden Idol).
- Knowledge objects: **8** product opportunities, KO-PO-09-001 to 008. All cite catalogued sources. KO-PO-09-008 is marked `design_hypothesis`.
- Market-size sources: **1**, HolonIQ 2020. No other market number is used.

## Files produced
- `09_COMPETITIVE_INTELLIGENCE/GLOBAL_COMPETITOR_INTELLIGENCE.md`
- `09_COMPETITIVE_INTELLIGENCE/_data/competitors_global.csv`
- `09_COMPETITIVE_INTELLIGENCE/_data/sources.jsonl`
- `09_COMPETITIVE_INTELLIGENCE/_data/knowledge_objects.jsonl`
- `09_COMPETITIVE_INTELLIGENCE/_data/agent_report.md`
- `09_COMPETITIVE_INTELLIGENCE/cards/ATH-SRC-0808.md`, `ATH-SRC-0811.md`, `ATH-SRC-0819.md`, `ATH-SRC-0822.md`, `ATH-SRC-0831.md`

I did not touch any `_arab` file.

## Search strategy
- I first ran category searches for board and hybrid games, mystery boxes, daily puzzles, classroom escape rooms, labs, misinformation games, AI storytelling, and AI-interrogation games on Steam.
- I then fetched official pages directly: developer or product sites, Steam store pages, App Store and Google Play listings, university press releases, the FTC, and a Wikipedia page only for basic facts about historic games.
- Ratings come only from Steam, App Store and Google Play, with the date I saw them. Critic aggregates (Metacritic, OpenCritic) appear only where Wikipedia reports them, and they are labelled as critic scores.

## Blockers
1. **The shared WebSearch budget ran out** after about 10 searches. The 200-call limit per turn is shared by all agents. Every later verification was done by fetching known official URLs.
2. **The shared WebFetch budget ran out** after about 100 fetches (800 per hour shared). Retries still failed when I wrote this report.
3. Some sites refused or failed: brilliant.org/pricing (client error), goviralgame.com (robots), missionus.org (robots), canadianmysteries.ca (error), the Google Play page for Duskwood (error), Wikipedia "Uncover the Smoking Gun" (not found), the Wikipedia page for Exit: The Game (not found), the L.A. Noire Steam page (age gate), and the Harmony Square page (it returned only metadata).
4. A guessed Steam app ID returned an unrelated game (Bus Driving Sim 22). I discarded it and did not catalog it.

## Unverified candidates (not in sources.jsonl)
| Candidate | Why not verified |
|---|---|
| Uncover the Smoking Gun (ReLU Games / Krafton, LLM robot-suspect interrogation) | Search budget exhausted; the Wikipedia URL did not exist; I had no Steam ID |
| Dead Meat, Steam page details (Meaning Machine) | Only the studio page was verified; release date, price and languages are unknown |
| EXIT: The Game (KOSMOS; Kennerspiel 2017) | KOSMOS and Wikipedia fetches failed |
| Mission US (WNET) | robots.txt blocked the fetch |
| Great Unsolved Mysteries in Canadian History | Site error |
| L.A. Noire | Steam age gate |
| Duskwood store ratings and chat format | Store fetches failed; only the studio homepage was verified |
| Brilliant consumer pricing | Pricing page failed |
| Character.AI c.ai+ pricing and languages | The homepage returned only metadata |
| Harmony Square partners (US DHS/CISA, State Dept) and languages | The page returned only metadata |
| Labster forensic-science simulations | Not shown on the homepage; the catalog was not checked |
| Inworld "Origins" detective demo | Not on the current homepage |
| Murdle book sales and "Murdle Pro" | Not stated on the homepage |
| Academic critiques of inoculation games (response-bias, replication) | Search budget exhausted; passed to teams 06 and 07 |
| Other candidates found in search results but not checked: Detective Grimoire, Overboard!, Telling Lies, Sherlock Holmes: The Awakened, Mystery Case Files, Clue/Cluedo apps, Episode/Chapters story apps, Inkitt, Wattpad, Scrimba-like story platforms, Legends of Learning, Prodigy, BrainPOP, CSI-themed Labster sims, Smithsonian forensic anthropology lab, 'Whodunnit?' NYT-style puzzles | No budget left to verify |

## Top 5 findings that should change ATHAR's design
1. **No single global product combines all of ATHAR's elements.** These are free investigation with linked evidence, forensic labs, validated reasoning assessment, Arabic-original content, and a teen focus. Of the 55 products, only 3 have validated assessment (all misinformation-focused) and 4 have labs. ATHAR's novelty is in how it integrates these pieces, not in any single feature. This is limited by an incomplete scan.
2. **Free-form LLM suspects are not a moat, and they carry real risk.** The niche is small and fragmented: Doki Doki scores 81% of 488 reviews and Vaudeville 47% of 287. Middleware makes the feature cheap to copy. Character.AI removed open-ended chat for under-18 users by 25 Nov 2025 amid lawsuits and an FTC inquiry. The MVP should use a case truth ledger, guided questions, a question quota, and rewards for exposing contradictions rather than "pressure to confess".
3. **Structured deduction is the best-proven fun mechanic**, as in Golden Idol (98%) and Obra Dinn (96%, with Arabic support). ATHAR can turn the same structure into an assessment by adding "supporting evidence" and "what weakens my theory" fields.
4. **Arabic UI is no longer a differentiator.** June's Journey, Obra Dinn and Disco Elysium already ship in Arabic. The scarce assets that take years to build are fair Arabic case content, reasoning data, validated measures, and Arabic language quality for teens.
5. **Only measured claims are safe and credible.** FTC v. Lumosity, and the self-reported efficacy figures of most competitors, mean ATHAR should build pre/post measurement in both directions, modelled on Go Viral!, from day one. Its marketing should claim only what it measures.

## Top 5 open questions and gaps for human or expert review
1. Re-run the scan when budgets reset. Priority items are: Uncover the Smoking Gun, Dead Meat, EXIT, Mission US, Labster's forensic catalogue, Brilliant pricing, and Duskwood store data.
2. Do Arabic versions of Bad News, Go Viral! or COR exist? Coordinate with team 09A.
3. What do independent replications and response-bias critiques say about inoculation games? This is for teams 06 and 07.
4. What rules govern AI characters for minors in the UAE, KSA, Egypt and Lebanon? This is for team 11.
5. Can Hidden Door or other AI story engines handle Arabic, and is there a regional LLM provider ready to partner? This is for team 10.

## Notes on data quality
- Figures that companies report about themselves (users, efficacy) are labelled as self-reported in `key_findings` and `limitations`.
- `similarity_to_athar` and `user_freedom` are analyst judgements on a 1–5 scale. They are not measurements.
- "Arabic support = no" means Arabic was missing from the languages list on the verified store or official page. "unknown" means no list was available.

## Gap-fill round (2026-10-27)

**Agent:** gap-filling researcher (second pass after the shared budget ran out). **Method:** about 12 WebSearch calls shared with the Arab pass. Most checks used official store data endpoints instead of the shared WebFetch quota: Steam `appdetails`, store pages and tag-filtered search, the Apple iTunes Search and Lookup API, and App Store listing pages. A few official pages were fetched with curl after checking robots.txt (Mission US, KOSMOS, Labster sitemap and pages, inoculation.science). Nothing was deleted. Original rows were edited only where new evidence filled an `unknown` or `not verified` field, and each edited row got the new source ID appended to `source_ids`.

### Counts
- New sources: **25**, ATH-SRC-0869 … ATH-SRC-0893 (block 0894–0899 still free). All lines are valid JSON. All 94 IDs are contiguous with no duplicates.
- New competitor rows: **10**, GC-056 … GC-065. These are Uncover the Smoking Gun, EXIT: The Game, Mission US, Frogwares Sherlock Holmes, L.A. Noire, Telling Lies, Detective Grimoire, Overboard!, An Elmwood Trail and Enigmic. The CSV now has 65 rows, every row has 24 columns, and every `source_ids` value resolves.
- Rows updated (unknown values resolved): 13 rows. GC-014, 017, 019, 024, 029, 033, 037, 040, 049, 050 and 054 had `arabic_support` unknown and are now "no". GC-053 was already "no"; its rating, price and format are now filled. GC-019 also changed `reasoning_assessment` from unknown to validated (RCT per ATH-SRC-0882).
- No new global KO is warranted. The new evidence sharpens KO-PO-09-002 and 003 but does not create a new gap. The Arab-side KO-PO-09A-008 records the positioning change.

### Unverified candidates — resolution
| Candidate | Result |
|---|---|
| Uncover the Smoking Gun | **Verified** (Steam) → 0869 / GC-056 |
| Dead Meat, Steam details | **Verified** (Steam: 2026, English only, unreleased) → 0870 / GC-040 |
| EXIT: The Game | **Verified** (KOSMOS product page) → 0874 / GC-057 |
| Mission US | **Verified**: the old domain was blocked, but www.mission-us.org allows crawling → 0875 / GC-058 |
| L.A. Noire | **Verified** (Steam with an age-gate cookie) → 0885 / GC-060 |
| Duskwood store data | **Verified** (App Store US) → 0880 / GC-053 |
| Brilliant pricing | **Partly**: /pricing returned 404. App Store IAP prices were captured, but billing periods are not shown → 0879 |
| Character.AI pricing/languages | **Verified** (App Store US) → 0881 |
| Harmony Square partners/languages | **Verified** (inoculation.science) → 0882 |
| Labster forensic sims | **Resolved**: the sitemap of about 311 sims has no forensic or crime slug. Two mystery-framed sims and a Jordan case study were catalogued → 0876–0878 |
| Great Unsolved Mysteries in Canadian History | **Abandoned** after 2 failures (site error, then 404) |
| Inworld "Origins" demo; Murdle sales/"Murdle Pro" | Not attempted (low priority) |
| Academic critiques of inoculation games | Not attempted; still with teams 06/07 |
| Detective Grimoire, Overboard!, Telling Lies, Sherlock Holmes: The Awakened | **Verified** (Steam) → 0883–0888 |
| Mystery Case Files, Clue apps, Episode/Chapters, Inkitt, Wattpad, Legends of Learning, Prodigy, BrainPOP, Smithsonian lab | Not checked. Wattpad Arabic was checked on the Arab side |

### Arabic support check (task 3)
Store or official language lists now resolve 11 of the 22 previous `unknown` values to **no**. Earlier lists already gave 4 "yes" values; this round adds 2 more (Frogwares Sherlock Holmes and Enigmic). The 13 rows still `unknown` include Deadbolt, SHCD, Detective (board game), MicroMacro, Cranky Uncle, Checkology, Kialo, Khanmigo (the Khan Academy iOS app lists 26 languages without Arabic, but Khanmigo itself was not checked), Interland, Hidden Door (its FAQ and pricing pages do not state languages), Choice of Games, and the new rows EXIT and Mission US.

### Findings that change conclusions
1. **AI interrogation is now proven at publisher scale** (KRAFTON co-publishing, 96% positive) **and has Arabic entrants** (see the Arab report). This weakens free-text suspects further as a differentiator.
2. **The "short case-embedded forensic lab" slot is still open globally** (Labster has none). In Arabic, an adult PC game (Homicide Desk) now partly fills it.
3. **Arabic is rare across the catalog**: about 4.6% of Steam "Detective" games (ATH-SRC-0893). Arabic is not a differentiator against the top titles, but it is a gap in volume.
4. **A phone-evidence mystery has a very large audience**: An Elmwood Trail has 264,946 US ratings at 4.9 and was built by a solo developer.
5. The global MD sections were updated surgically: header, §1 item 1, §2.1, §2.2, §2.3, §2.6, §2.7, §2.8, §2.9, §2.10, §3, §4.1, §4.2, §5 and §6 rec. 3.

### Still open
- Hidden Door languages and teen policy.
- Khanmigo languages.
- Arabic support for the remaining 13 `unknown` rows.
- Brilliant billing periods.
- Independent replications for inoculation games.
- Canadian Mysteries.

## Synthesis round (2026-10-27)

**Agent:** competitive-strategy analyst. This round synthesized the existing library; it did not collect new sources beyond one decisive check.

**Files written** (all in `09_COMPETITIVE_INTELLIGENCE/`):
- `FEATURE_GAP_MATRIX.csv`: 35 competitors (13 Arab, 22 global) × 16 ATHAR capabilities, plus similarity, threat and sources, and 3 summary rows. The summary rows were computed in Python. Coding rules are in WHITE_SPACE §Annex A. Similarity values were checked programmatically against `competitors_*.csv`.
- `INNOVATION_COMPETITOR_CHECK.csv`: the 15 §18 innovation directions × competitor evidence.
- `WHITE_SPACE_OPPORTUNITIES.md`: 8 gaps (W1–W8) with confidence levels, plus a "not a gap" list.
- `ATHAR_DEFENSIBILITY_ANALYSIS.md`: copy-time tiers, ranked moats, threats, kill criteria and a revised novelty-claims table.

**New source (1):** ATH-SRC-0894, the Golden Idol App Store listing (SA). The iOS app is English-only, rated 13+, and priced SAR 20.99. Its sequel ships in 11 languages, none of them Arabic. The ID block now runs to 0894; 0895–0899 are free. One WebSearch was used. The Netflix help page returned no language list. Note: the header counts in `GLOBAL_COMPETITOR_INTELLIGENCE.md` (94 sources) are now one short, and the file was not edited per scope.

**Matrix facts (computed):**
- Among the 23 investigation products, these capabilities have 0 "yes": reasoning-process assessment (9 partial), teacher mode (2 partial, both English), learning analytics, validated assessment, and teen-safety design (7 rows are "no").
- No product in the matrix has an insufficient-evidence verdict (7 unknown).
- Arabic UI has 13 yes and Arabic-original content has 9 yes, so neither is a differentiator.
- Homicide Desk is the closest product, with 6 of 16 capabilities "yes".
- 18.2% of cells are unknown.

**Conclusions that change the earlier reports:**
1. The defensible space is institutional, not mechanical: measured reasoning, a teen-safe reviewed library, and school trust. Every play mechanic can be copied in under 6 months.
2. The insufficient-evidence verdict (W7) may be ATHAR's most novel mechanic, but confidence is low because it was never searched for.
3. The cheapest kill-test is K1: do teens enjoy teen-safe cases? It should run before any large content spend.

**Still open:** Golden Idol's Netflix and Google Play languages; offline behaviour of competitors (28 of 35 unknown); hint-ladder data (21 unknown); Shu'la Lab team and funding.
