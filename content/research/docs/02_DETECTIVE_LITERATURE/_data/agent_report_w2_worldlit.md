# Agent report — W2-WORLDLIT (world, Japanese/Chinese, YA & children's mystery; PD story corpus)

Date: 2026-10-27 · ID block ATH-SRC-1300…1399 (used 1300–1387) · KO code 02W

## 1. Counts
- **Sources verified:** 88 new records (`sources_w2_worldlit.jsonl`), schema-validated, no duplicate of the master catalog or other wave-2 files.
  - By rights: 53 PUBLIC_DOMAIN, 28 COPYRIGHTED_RESTRICTED, 7 OPEN_LICENSE.
  - By verification method: 59 fetched official page/text, 19 Wikipedia (bibliographic only), 8 DOI/catalog, 2 search-confirmed.
  - Evidence grades: A 70 (primary texts), B 8 (peer-reviewed), C 4, D 6.
- **Knowledge objects:** 26 (`knowledge_objects_w2_worldlit.jsonl`): 20 NP (KO-NP-02W-001…020) + 6 CD (KO-CD-02W-001…006). All source_ids resolve.
- **Stored texts:** 62 new files, **25.9 MB** (plus 9 wave-1 files back-filled into the manifest as TXT-W-000a…000i, sha256 recomputed and matching README prefixes). Total under my manifest rows: 71 rows, 30.5 MB. All sha256 values re-verified after writing.
- **Story corpus:** `STORY_CORPUS_INDEX.csv`, 102 works (SC-001…SC-102), 66 with stored paths; all KO and source IDs in it resolve.
- **Rights register:** 51 rows appended to `LITERARY_RIGHTS_REGISTER.csv` (append-only; file now 106 rows, all 12 columns).
- **Design principles:** 24 new (ATLAS-51…74) in `WORLD_AND_YA_MYSTERY_EXPANSION.md`; 65 source IDs and 24 KO IDs cited, all resolve.
- Deep cards: none written (not requested in the wave-2 brief; time spent on texts and verification instead).

## 2. Files produced / touched
- NEW `02_DETECTIVE_LITERATURE/_data/sources_w2_worldlit.jsonl`
- NEW `02_DETECTIVE_LITERATURE/_data/knowledge_objects_w2_worldlit.jsonl`
- NEW `02_DETECTIVE_LITERATURE/_data/agent_report_w2_worldlit.md` (this file)
- NEW `02_DETECTIVE_LITERATURE/WORLD_AND_YA_MYSTERY_EXPANSION.md`
- NEW `15_STORY_MEDIA_AND_ASSETS/STORY_CORPUS_INDEX.csv`
- APPENDED `02_DETECTIVE_LITERATURE/LITERARY_RIGHTS_REGISTER.csv`
- APPENDED/CREATED `99_LEGAL_SOURCE_ASSETS/ASSET_MANIFEST_W2_TEXTS.csv` (created with header; TXT-W rows; heritage team appends TXT-H rows to the same file — file locking used)
- NEW folders under `99_LEGAL_SOURCE_ASSETS/PUBLIC_DOMAIN_VERIFIED/` (45 slugs): Doyle ×3, Green ×2, Futrelle, Orczy ×2, Freeman ×4, Bramah ×2, Morrison, Collins, Gaboriau ×2 (French), Zangwill, Hume, Chesterton ×4, Leroux (French), Leblanc ×2 (French original; Teixeira de Mattos tr.), Felix, Dickens, Voltaire ×2, Huxley, Twain ×2, Reeve, Mason, Poe (5 tales in one folder), Post (OCR), Ranpo (9 stories + 2 figures), Okamoto Kidō (3 stories), gong'an ×5 (Di/Shi/Peng/Bao Gong An, Tangyin Bishi).

## 3. Method and interpretations (owner away — decisions recorded)
1. **Mirror choice.** GITenberg lacks most titles, so texts came from the **official PG mirror `gutenberg.pglaf.org`** (listed by PG; ≥2 s between requests; catalog via `cache/epub/feeds/pg_catalog.csv` from the same mirror). Files kept byte-identical with PG headers/licence.
2. **Standard Ebooks** (CC0 for their contributions) used for Poe's five ratiocination tales and *The Incredulity of Father Brown*; XHTML converted to plain text with a provenance header, wording unchanged. I avoided the PG "Raven Edition" Poe volumes because they include 1903 editorial essays by an unidentified "W. H. R." whose death date I could not establish.
3. **Three-regime storage rule applied to each file:** US (published ≤1930, or 1926/1927 volumes that became US-PD in 2022/2023) + UK/EU life+70 + Arab life+50. Author death years from PG authority data, Aozora author pages, NDL, Wikipedia.
4. **Translations:** stored only when the translator's death year was established (Alexander Teixeira de Mattos d.1921; anonymous 1749 *Zadig*). **Not stored:** Gaboriau English (no translator named), Leroux *Yellow Room* 1908 English (Brentano's, translator unnamed), Lupin tr. George Morehead (dates unknown), van Gulik (d.1967), Massee's *Emil* (UK-protected to 2036). French originals stored instead.
5. **Japanese originals:** Ranpo d.1965 → Japanese term ended end-2015; the 2018 life+70 extension is not retroactive (Agency for Cultural Affairs page fetched). UK CDPA s.12(6) and EU Dir. 2006/116 Art.7(1) apply comparison of terms for non-UK/EU-origin works by non-nationals → PD. Only stories first published ≤1930 (US) stored. **Counsel should confirm the UK post-Brexit comparison-of-terms reading** (CDPA s.12(6) text fetched; still in force as amended).
6. **Uncle Abner:** stored only the IA OCR text of the 1918 Appleton edition (item marked PDM 1.0). Noisy — research/search use only.
7. **Recorded but not stored:** *Trent's Last Case* (Bentley d.1956; UK/EU PD from 1 Jan 2027), *Scandal of Father Brown* (US to 2030), Hardy Boys #1 and Nancy Drew #1 (US-PD only; ghostwriters d.1977/2002), *Emil and the Detectives*. Downloaded copies of these were deleted from scratch.
8. **Wikisource (zh):** 棠陰比事 and 包公案 (100 chapters) fetched as raw wikitext via `action=raw` with ≥3 s spacing; two 429 responses were retried after 30 s back-off. Wiki markup retained.
9. Edited my own file once (rewrote `sources_w2_worldlit.jsonl` in place to fix the rights wording of ATH-SRC-1365); no other team's file was rewritten.

## 4. Search strategy
PG catalog CSV queries by author/title/subject → mirror directory listings → header verification of each file. Aozora author pages and cards (初出 first-publication data). Open Library search API for first-publication years; Crossref/OpenAlex for DOIs and abstracts; WebFetch on Wikipedia for literary bibliography; WebSearch for discovery (Arabic YA, reader research, Korean, Chinese contemporary).

## 5. Blockers
- Wikidata, en.wikisource API: HTTP 429 (not hammered). Wikipedia via WebFetch only.
- Scholastic 5th-edition report (2015) with mystery percentages: 404; 7th edition fetched but has no genre data.
- National Literacy Trust 2013/2015 reports fetched — no genre data.
- Wikipedia pages for *The Bad Kids (novel)* and *13.67* not found; used Complete Review, Leeds Writing Chinese and Kirkus instead (grade C).
- No arabic-language catalogue (e.g., Dar al-Hilal archive) reachable to verify *Al-Shayatin al-13* issue dates.

## 6. Unverified candidates (not cataloged)
- *Al-Shayatin al-Thalatha 'Ashar* (Mahmoud Salem, Beirut/Dar al-Hilal, 1970s) — only Goodreads hits; wave-1 ATH-SRC-0140 already mentions it from a press source.
- Scholastic KFRR 5th ed. (2015) "mystery or problem to solve" by age — numbers not available on fetched pages.
- *Encyclopedia Brown* original publisher (Thomas Nelson) — from general knowledge, flagged in record.
- Gaboriau English translators (possibly multiple 1880s US translations) — unidentified.
- *Max Carrados Mysteries* (1927, US-PD since 2023) and further Freeman/Orczy titles published 1927–1930 — PD-eligible but not downloaded this round.
- Kim Nae-sung texts (d.1957: life+70 PD from 2028) — future candidate.
- Korean contemporary YA mystery — not searched in depth.
- Peer-reviewed study on Arab adolescents' mystery reading motivations — none found.

## 7. Top 5 findings that should change ATHAR's design
1. **The storable corpus is now large enough for a "classics lab"** (66 stored works across EN/FR/JA/ZH); every original-language PD text can be freshly translated into Arabic without third-party rights — prefer that to any existing translation (ATLAS-73).
2. **Daily micro-cases need a "knowledge requirement" field.** Encyclopedia Brown proves the format works but many solutions depend on outside trivia; fairness check must cover required knowledge (ATLAS-51).
3. **Default to medium complexity and adaptive reveal screens.** Two experiments show complexity lowers enjoyment and that low-confidence readers dislike surprise endings (ATLAS-63/64) — test on Arab teens before relying on it.
4. **Gong'an and Arabic qadi tales share a "reaction test" trope that teaches the wrong lesson** (demeanour = guilt). Use them only as "was this fair?" discussion items (ATLAS-58).
5. **Replace the "bumbling policeman" of classic children's series with a competent, overloaded official**; Iskander (1993) is the only peer-reviewed comparison of Arab vs. American teen-detective values and should be read in full by the narrative lead (ATLAS-70).

## 8. Top 5 open questions for human/expert review
1. Counsel: comparison-of-terms for Japanese originals in the UK post-Brexit; and whether house-pseudonym (work-for-hire) series count as pseudonymous works (70 years from publication) in UK/EU.
2. Counsel: Egypt's death-date counting (wave-1 issue) also affects Ranpo/Okamoto — no practical effect (long expired), but note for 1950s–1970s authors.
3. Narrative lead: read Iskander (1993, ATH-SRC-1375) and McGee (2024, ATH-SRC-1374) in full.
4. Research: commission or locate a survey of Arab 13–18 readers' genre preferences (mystery/crime) — current evidence is US/adult.
5. Bias audit of stored texts before any teen-facing excerpt (Poe *Gold-Bug*, Twain, *Three Gables*, Ranpo, gong'an torture scenes).
