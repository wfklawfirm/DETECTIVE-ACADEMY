# Agent Report — 02_DETECTIVE_LITERATURE

**Date:** 2026-10-27 | **Source ID block used:** ATH-SRC-0100 … ATH-SRC-0184 (85 of 100) | **KO lib code:** 02

## 1. Counts

| Item | Target | Delivered |
|---|---|---|
| Verified source records (`sources.jsonl`) | 45–70 | **85** |
| — of which literary works (novels, stories, series, 1 film) | 30–40 | **52** |
| — of which criticism / theory / rule documents (incl. ArabLit anthology issue) | — | **23** |
| — of which legal and rights anchors (6 statutes/directive, 2 cases, Duke CSPD, Christie Ltd) | — | **10** |
| Deep cards (`cards/`) | 8–10 | **10** |
| Knowledge objects: NP narrative_pattern | 25–35 | **32** |
| Knowledge objects: CD character_design_pattern | 10–15 | **15** |
| Atlas principles | 40–60 | **50** |
| Plot patterns (MYSTERY_PLOT_PATTERNS) | — | **26** + Season-1 composition + 7 "never use" patterns |
| Rulebook rules (each with a check method) | — | **59** (15 FP, 7 NR, 8 SC, 8 BI, 8 AG, 8 AS, 5 RT) |
| Rights register rows | — | **54** (incl. disclaimer row) |

Evidence grades in the catalog: A 59, B 17, C 6, D 3. Rights: 49 COPYRIGHTED_RESTRICTED, 29 PUBLIC_DOMAIN (jurisdiction always named), 5 UNKNOWN, 2 OPEN_LICENSE. Records marked `needs_expert_review`: none remain (UAE and EU were resolved late in the session). Records with `confidence: medium` flag partial verification.

## 2. Files produced

- `02_DETECTIVE_LITERATURE/DETECTIVE_LITERATURE_ATLAS.md`
- `02_DETECTIVE_LITERATURE/MYSTERY_PLOT_PATTERNS.md`
- `02_DETECTIVE_LITERATURE/FAIR_PLAY_MYSTERY_RULEBOOK.md`
- `02_DETECTIVE_LITERATURE/LITERARY_RIGHTS_REGISTER.csv`
- `02_DETECTIVE_LITERATURE/cards/` with 10 cards: ATH-SRC-0100 (Rue Morgue), 0114 (Ackroyd), 0120 (Five Little Pigs), 0124 (Poisoned Chocolates), 0126 (Hollow Man), 0127 (Daughter of Time), 0146 (Knox Decalogue), 0153 (Sign of Three), 0155 (Todorov), 0157 (Bayard)
- `02_DETECTIVE_LITERATURE/_data/sources.jsonl` (85 lines, validated JSON and schema enums, no dangling cross-references)
- `02_DETECTIVE_LITERATURE/_data/knowledge_objects.jsonl` (47 lines, validated; every object cites catalog IDs)
- `02_DETECTIVE_LITERATURE/_data/agent_report.md` (this file)

## 3. Search strategy

1. Primary works: Wikipedia was used **only** for bibliographic facts (first publication, publisher, dates, documented reception and criticism), per protocol. Plot mechanics were cross-checked against the same pages.
2. Rights: official legal texts via WIPO Lex (LB Law 75/1999 Art. 49; SA Royal Decree M/41 Art. 19; EG Law 82/2002 Art. 160), the UAE official legislation portal (Decree-Law 38/2021 Art. 20), legislation.gov.uk (CDPA s.12), EUR-Lex (Dir. 2006/116 Arts. 1, 7, 8), Duke CSPD Public Domain Day 2026, and the Klinger and Enola Holmes summaries.
3. Criticism and theory: publisher or catalog pages (WorldCat, National Humanities Center, Cambridge Core, Waterloo Genre Across Borders), and Crossref for DOIs (Snyder 2004, Brewer & Lichtenstein 1982, Ginzburg 1980, Rzepka 2007).
4. Christie's official sites: agathachristie.com (rule-breaking article, Lindbergh article) and agathachristielimited.com (licensing role).
5. Arabic tradition: English Wikipedia (Mahmoud Salem, Nabil Farouk, Ahmed Khaled Tawfik, Rewayat, Ahmed Mourad, The Three Apples), ArabLit (Summer 2020 CRIME issue; *The Djinn's Apple* preview).

## 4. Blockers

- **WebSearch budget exhausted** (shared limit of 200 per turn) after about 45 searches by this agent. The rest of the work used WebFetch on known authoritative URLs.
- **WebFetch hourly quota exhausted once** (shared limit of 800 per hour). Work continued offline until reset.
- **Arabic Wikipedia was unreachable** through the fetcher (every ar.wikipedia URL returned not-found), as were Wikidata and the Wikipedia API. This is the main reason the Arabic youth-mystery section is thinner than planned.
- Blocked or robots-disallowed: HarperCollins UK, Neem Tree Press, Open Library, Google Books API, Al-Monitor, UAE Ministry of Economy PDF, gov.uk copyright guidance, U. Chicago Press, JHU Press, Cambridge Companion to Sherlock Holmes page.
- The signed WIPO PDF link for the UAE law exceeded the proxy's URL length. Resolved through uaelegislation.gov.ae.

## 5. Unverified candidates (not in `sources.jsonl`)

| Candidate | Why not verified |
|---|---|
| Hafez Naguib (early Egyptian detective pastiches, "Johnson") | English Wikipedia page not found; Arabic Wikipedia unreachable |
| Early Arabic translations of Holmes and Lupin (e.g., early-20th-c. Cairo pulp translations) | No authoritative page reached |
| Publisher, issue count and Blyton influence of «المغامرون الخمسة» | Only the author page was confirmed; series article unreachable |
| Start years of Nabil Farouk's Ragol al-Mostaheel and Malaf al-Mostakbal | Not stated on the fetched page |
| Arabic broadcast history of Detective Conan («المحقق كونان»), e.g., Spacetoon | Not on the fetched page |
| *The Cambridge Companion to Sherlock Holmes* (Allan & Pittard, eds.) | Cambridge page blocked |
| Martin Edwards, *The Life of Crime* (2022); *The Story of Classic Crime in 100 Books* (2017) | No search budget left |
| Stephen Knight, *Crime Fiction since 1800* | No search budget left |
| John Curran, *Agatha Christie's Murder in the Making* (2011) | Not reached |
| Carr's "Locked Room Lecture" category list | Content not on fetched pages (intentionally not reproduced) |
| Higashino fair-play debate in Japan (Nikaido Reito vs Kasai Kiyoshi, reported) | Not on fetched page; omitted |
| Japanese term for Yokomizo (life+70 in Japan since 2018) | Not checked |
| Death dates of Van Dine, Knox, Hammett, Chandler, R. Austin Freeman, Eco | Not fetched; register marks them UNVERIFIED |
| Pierre Bayard English translations (translator and year) | Publisher page lacked the details |
| Seishi Yokomizo and Soji Shimada Pushkin Vertigo imprint details | Pages name Pushkin Press only |
| Todorov essay's French original date (1966?) and exact wording | Only the English bibliographic record was confirmed; content summarised from prior knowledge (confidence: medium) |
| Brewer & Lichtenstein, Ginzburg, Sternberg: argument details | Bibliographic data confirmed; content summarised from prior knowledge (confidence: medium) |

## 6. Top 5 findings that should change ATHAR's design

1. **Fairness has to be tested, not declared.** The canonical rules (Knox 1929, Van Dine 1928) mix real fairness conditions with class taste and an explicitly racist rule (Knox 5), and the most admired novels break them (Ackroyd, Orient Express; per Christie's own site). The Rulebook therefore turns the fairness core into **machine-checkable data constraints** (critical clue reachable before the gate; every crime event has a trace; no orphan events) plus **playtest solve-rate bands** and a mandatory **alternative-solution test** inspired by Bayard and Berkeley.
2. **Holmes is a model of attention, not a method.** His "deductions" are mostly abductive guesses that the author guarantees (Eco & Sebeok 1983; Ginzburg 1980), and his influence on forensic science is overstated (Snyder 2004). The UI should enforce *observation → hypothesis → test → conclusion*, reward generating alternative explanations and calibrated confidence, and **avoid "think like Sherlock" marketing**. That marketing would be both scientifically weak and a trademark and litigation risk (Klinger 2014; Enola Holmes suit 2020).
3. **The dossier / cold-case format is the best literary fit for mobile and for teens.** *The Moonstone*, *Five Little Pigs*, *The Appeal* and *A Good Girl's Guide to Murder* show that documents and testimony alone can carry a mystery without gore. Proposed default: cases presented as dossiers, with a cross-testimony matrix and a timeline-rebuild deliverable.
4. **The system voice must never lie.** The Ackroyd device works in print but would erode trust in a platform used daily. Unreliability is confined to in-world characters and documents, and every testimony is tagged (accurate, sincere error, or motivated distortion).
5. **Rights are split by jurisdiction, and global app stores force the strictest reading.** Christie (d. 12 Jan 1976): expected PD in LB and UAE from 1 Jan 2027 (calendar-year rule, verified Arts. 49 and 20); EG and SA count 50 years from death (Arts. 160 and 19), so the term appears already ended in Jan 2026 (counsel to confirm). UK and EU protection runs to end-2046; in the US, only works published by 1930 are PD. Tey's *Daughter of Time* is the reverse case: PD in UK/EU but protected in the US to 2046. **Recommendation: no classic characters or texts in the product; only original cases built on borrowed structures.** A PD "classics library" (Poe, Doyle, Collins, Leroux in new Arabic translations) is feasible after counsel review.

## 7. Top 5 open questions or gaps for human or expert review

1. **Counsel:** treatment of foreign works and calendar-year rounding in EG and SA; whether new translations of PD originals avoid claims by existing Arabic translators and publishers; trademark status of "Sherlock Holmes", "Poirot", "Miss Marple", «المغامرون الخمسة».
2. **Arabic literature specialist:** a verified history of Arabic detective fiction: early translations and pastiches (Hafez Naguib and others), Mahmoud Salem's publisher and issue run, Nabil Farouk's series years, pre-modern sources (al-Tanukhi, al-Jawbari), and modern Arab crime fiction beyond Mourad. Arabic Wikipedia and Arabic sources could not be reached this session.
3. **Learning and assessment team (07):** how to score interpretive solutions (cold cases) and alternative-hypothesis quality reliably; target solve-rate bands per tier.
4. **Cognitive team (06):** evidence on memory distortion over time, apophenia and overconfidence, to back the witness-error and calibration mechanics; cognitive-load limits for the number of testimonies and red herrings on mobile.
5. **Narrative and game team (03) with technical architecture (10):** can the alternative-solution test be automated by modelling cases as logical constraints? And how can open exploration coexist with the "all critical clues reachable" guarantee?

## 8. Notes on method and honesty

- Every catalog record was confirmed this session through the URL in `verification_url`. Where content claims rely on prior knowledge (Todorov, Brewer & Lichtenstein, Ginzburg, Sternberg, Edmund Wilson), the record says so and carries `confidence: medium`.
- US public-domain dates for 1920–1929 works are **inferred** from the 95-year rule and Duke CSPD's 2026 listing; they are not individually fetched.
- No text from any copyrighted work is reproduced. All plot and critical content is paraphrased, and spoilers appear only as analysis.
- Bias audit: racist and stereotyped elements are documented as findings (Knox Rule 5; The Three Gables; the original title of And Then There Were None; the Mormon depiction in A Study in Scarlet; disability stigma in The A.B.C. Murders; class exclusions in Van Dine) and converted into rules BI-01 to BI-08.

## Gap-fill round (2026-10-27)

**Agent:** gap-filling researcher (Arabic tradition). **Scope:** `_data/sources.jsonl`, this report, and the Arabic-tradition passages of `DETECTIVE_LITERATURE_ATLAS.md` only (the rights register was not touched; it is owned by another agent).

**New verified sources: 10 (ATH-SRC-0185 … 0194).** The 02 block now runs 0100–0194 (95 records).

| ID | Source | Verified via |
|---|---|---|
| 0185 | Selim (2010), "Fiction and Colonial Identities: Arsène Lupin in Arabic", *Middle Eastern Literatures* 13(2) | Crossref + full Arabic translation (Boring Books) |
| 0186 | Selim (2019), *Popular Fiction, Translation and the Nahda in Egypt* (Palgrave) | Crossref + ArabLit report of the author's 2015 talk |
| 0187 | Zachs & Bawardi (2020), detective translations in *al-Ḍiyāʾ*, *Die Welt des Islams* 60(1) | Crossref (abstract) |
| 0188 | Ghosn & Tadié (eds.) (2021), *Le récit criminel arabe / Arabic Crime Fiction* (Harrassowitz, Mîzân 32), incl. Shahin's chapter on Mahmoud Salem | Publisher page + Crossref chapter records |
| 0189 | Alghureiby (2015), "The Curious Case of Crime Fiction in Arabic Literature", AWEJ | Fetched PDF |
| 0190 | Qualey, *Arabic Detective Novels* (LEILA project) | Fetched PDF |
| 0191 | Qualey (2014), Al Jazeera opinion on the Arab crime novel | Fetched page |
| 0192 | Youm7 (2019) profile of Mahmoud Salem | Fetched page |
| 0193 | Hafez Naguib (bibliographic record) | Arabic Wikipedia via MediaWiki API (revid 76679930) + 0189/0190/0191 |
| 0194 | Ahram Online (2014), IPAF shortlist (The Blue Elephant, Dar al-Shorouk) | Fetched page |

**Changes to existing records (each logged):**
- **ATH-SRC-0140** (المغامرون الخمسة): `publisher` changed from "Not confirmed this session (commonly Dar al-Maaref)" to Dar al-Maaref (per retailer listing of issue 1; original imprint still to be confirmed from a catalogue), plus Dar al-Shorouk for the 2010+ instalments. Added: first issue «لغز الكوخ المحترق» (1968), monthly until 1972, Arabisation of Enid Blyton's *Five Find-Outers*, and the 13 Devils series. Source conflicts recorded in `limitations`: start/end 1968–1972 vs 1967–1973 (AWEJ), and death date 24 vs 13 Feb 2013. `verification_url` now points to Arabic Wikipedia.
- **ATH-SRC-0141** (روايات مصرية للجيب): `year` changed from null to 1984. Added: *Malaf al-Mostaqbal* ran 1984–2010 with 160 issues (first issue c. 1985 after the 1984 competition win); *Ragol al-Mostaheel* ran to 160 titles, 1984–2009 (AWEJ).
- **ATH-SRC-0142** (Mourad): `publisher` partly filled (*The Blue Elephant*: Dar al-Shorouk).
- **ATH-SRC-0143** (Lupin): `limitations` updated with the verified 1910 Arabic translation.
- No `review_status` changes were needed (none were `needs_expert_review`).

**Deliverable edits (`DETECTIVE_LITERATURE_ATLAS.md`):**
- Header range updated to 0100 … 0194.
- Principle 49 now gives the first issue and run of «المغامرون الخمسة», adds the correction that the series is an adaptation of Blyton, and adds the 13 Devils series. One interpretive line was added: borrow nostalgia, not devices.
- Annex B: new item 7, "Detective fiction is a modern import into Arabic", corrected using 0185–0194.
- Annex C: lists what was resolved and what remains open.

**Unverified candidates after this round (two attempts each, then abandoned):**
| Candidate | Status |
|---|---|
| Original 1968 publisher imprint and total issue count of «المغامرون الخمسة» | Arabic Wikipedia series pages rate-limited (HTTP 429); only a retailer lists Dar al-Maaref. Shahin's chapter in 0188 is the source to obtain |
| First Arabic translation of Sherlock Holmes (year, translator, periodical) | Not found; 0185 says it came "years after" the originals; 0189 gives the 1990s (probably modern editions). Conflict left open |
| Hafez Naguib's "Johnson" detective: whether original or adapted, and which titles | Wikipedia lists «زواج جونسون» among translations; secondary sources say "Johnson's Son". Unresolved |
| Publishers of *Vertigo* (2007) and *Diamond Dust* (2010) | Not reached |
| Arabic broadcast history of Detective Conan | Not searched (budget) |
| Taghreed Najjar, «لغز عين الصقر» (2014), teen mystery | Named only in 0190; publisher page not fetched. A high-value comparator for library 09A |
