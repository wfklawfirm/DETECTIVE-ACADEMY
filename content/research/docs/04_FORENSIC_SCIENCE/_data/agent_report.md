# Agent Report — 04_FORENSIC_SCIENCE

Date: 2026-10-27 | Source ID block used: ATH-SRC-0300 … ATH-SRC-0361 | KO lib code 04

## Counts

| Item | Count | Target |
|---|---|---|
| Verified source records (`sources.jsonl`) | **62** | 45–60 |
| … of which evidence grade A / B / C / D | 23 / 31 / 7 / 1 | — |
| … of which `needs_expert_review` | 3 (ATH-SRC-0329, 0353, 0354) | — |
| Deep analysis cards (`cards/`) | **10** | 8–10 |
| Knowledge objects (FC forensic_concept) | **32** | 25–35 |
| Atlas discipline cards | 16 (the 15 required, plus pattern-comparison methods) | 15 |
| Validity-matrix rows | 24 methods | — |
| Virtual labs scored / shortlisted | 30 / 10 | 30 / 10 |

Every record was confirmed this session by fetching an official page, a DOI/Crossref record or PubMed. All JSONL lines were checked with Python: they parse, cited IDs resolve, card files exist, and PUBLIC_DOMAIN and OPEN_LICENSE records carry jurisdiction or licence.

## Files produced

- `04_FORENSIC_SCIENCE/FORENSIC_SCIENCE_KNOWLEDGE_ATLAS.md`
- `04_FORENSIC_SCIENCE/FORENSIC_METHOD_VALIDITY_MATRIX.csv`
- `04_FORENSIC_SCIENCE/SAFE_VIRTUAL_LABS_CATALOG.md`
- `04_FORENSIC_SCIENCE/CSI_MYTHS_AND_SCIENTIFIC_CORRECTIONS.md`
- `04_FORENSIC_SCIENCE/FORENSIC_EXPERT_REVIEW_CHECKLIST.md`
- `04_FORENSIC_SCIENCE/cards/` — ATH-SRC-0300, 0301, 0304, 0305, 0306, 0317, 0324, 0331, 0336, 0342
- `04_FORENSIC_SCIENCE/_data/sources.jsonl`, `knowledge_objects.jsonl`, `agent_report.md`

## Search strategy

1. Searched in parallel for the core reports (NRC 2009, PCAST 2016, the PCAST addendum, the DOJ response, NIST foundation reviews, NIST human-factors reports, OSAC, ISO, ENFSI, FSR, Royal Society), then fetched each official page to confirm details.
2. The shared web-search budget ran out after about 20 searches. From then on, journal articles were verified directly through Crossref API DOI records, PubMed and publisher pages. That works only for DOIs already known. Three DOIs we tried resolved to unrelated papers (a Saudi child-maltreatment study, a Hawaii decomposition study, an ML image-classification tool). They were **discarded** and are not in the catalog.
3. The hourly WebFetch budget was also exhausted once. Work resumed after it partly refilled.

## Blockers

- **WebSearch budget exhausted** early in the run (shared 200-call limit). No Arabic-language searches could be run, which is the largest gap.
- **WebFetch hourly budget exhausted** once mid-run.
- **DOJ OIG site (oig.justice.gov, justice.gov/oig, oversight.gov) returned client errors** on every attempt, so the Brandon Mayfield report could not be verified.
- **enfsi.eu returned binary/empty content.** The ENFSI guideline was read from a third-party-hosted PDF. The official URL needs re-verifying.
- **AAFS /about** failed. **FBI press-release page** (2015 hair review) failed.
- Paywalled standards (ISO, ASB) were summarised from official abstracts only.

## Unverified candidates (not in sources.jsonl)

| Candidate | Why not verified |
|---|---|
| U.S. DOJ OIG (2006) *A Review of the FBI's Handling of the Brandon Mayfield Case* | All OIG URLs returned client errors. The case is mentioned in the deliverables only with an explicit "unverified" flag |
| FBI/DOJ press release (April 2015) on microscopic hair testimony errors (widely reported as "at least 90%" of reviewed cases) | Fetch failed. The figure is **not** used in the deliverables |
| National Registry of Exonerations contributing-factor percentage for false/misleading forensic evidence (24%) | Seen only as a citation on the Innocence Project page. Not visible on the NRE homepage |
| Innocence Project letter (4 Feb 2021) and Union of Concerned Scientists IQA request (June 2021) asking DOJ to retract its PCAST statement | Titles seen in search results only. Not fetched |
| NIST "Summary of published criticisms of bitemark foundations and responses from forensic odontologists" | Title seen in search results only |
| ANSI/ASB Standard 036 (toxicology method validation, believed to supersede SWGTOX 2013) | No search budget left |
| Royal Society primers published after 2017 (statistics, firearms, etc.) | Launch page mentions only the planned statistics primer |
| NIJ page "Post-PCAST court decisions assessing admissibility" | Seen in search results. Not fetched |
| NDAA response to PCAST (PDF) | Seen in search results. Not fetched |
| AAAS fire-investigation assessment; year of the AAAS latent-print report | Not fetched / year not shown |
| SWGDE individual documents (image authentication, photography) | The site lists committees, not titles. No budget left |
| ISO 21043-1, -3, -5 editions and dates | Only parts 2 and 4 were fetched from iso.org |
| Arabic-language forensic sources (Naif Arab University for Security Sciences, Arab forensic-medicine societies, national forensic laboratories) | No search budget. **Major gap** |

## Top 5 findings that should change ATHAR's design

1. **Reliability is a spectrum, and ATHAR must show it explicitly.** PCAST and NIST separate strong methods (single-source DNA, digital acquisition) from methods valid but error-prone (latent prints, handwriting), contested (firearms) and unsupported (bitemarks, footwear individualisation, microscopic hair) [0301, 0305, 0306]. Every clue should carry a reliability tag. Content must never imply that "forensics is all junk".
2. **The largest source of forensic contribution to wrongful convictions is communication, not lab identification.** In 732 US exoneration cases, overstated or limitation-free reports and testimony, unconfirmed presumptive tests and non-lab actors dominated [0336]. NRC 2004 on bullet lead adds that a precise measurement can still support an invalid inference [0361]. ATHAR should therefore teach the writing and critique of expert reports, not just lab technique.
3. **DNA answers "whose?" more readily than "how/when?"** Transfer, contamination and mixture complexity make reliability "a matter of degree" [0304, 0341, 0340]. Two distinct questions should be built into every biological clue.
4. **"Inconclusive" is a legitimate scientific outcome, and error rates depend on how it is counted** [0331, 0333, 0334, 0335]. Scoring rules must not punish justified inconclusives.
5. **Commit-before-context (LSU-E) is both good forensic practice and a strong game mechanic** [0325, 0324, 0323]. Dror's "technological protection" fallacy also applies to ATHAR's own AI features, so the product should never present its AI as bias-free.

## Top 5 open questions / gaps for expert review

1. **No Arabic or regional sources.** We have none on forensic-lab institutions, accreditation, courts' treatment of forensic evidence, or Arabic forensic terminology. A standardised Arabic glossary (likelihood ratio, proposition levels, inconclusive) is needed.
2. **Arabic handwriting.** All handwriting error-rate data we verified are for Latin script [0333]. Whether they transfer to Arabic script is unknown.
3. **Contested items.** Dror et al. 2021 on pathology bias [0329] is disputed by pathologists. Firearms error rates are disputed in the inconclusives debate. The DOJ vs PCAST disagreement needs balanced framing, and an expert should decide age placement.
4. **Ethics of the context-reveal lab.** Briefly deceiving learners with biasing context, then debriefing, needs sign-off from the learning-science (07) and safety (11) teams.
5. **Safety boundary wording** for toxicology ("detection ≠ causation", method limits) and digital evidence (interpretation vs anti-forensics) must be written with an expert so that nothing reads as evasion advice.

## Notes for the merge step

- Canonical owner: NAS/NRC 2009 (0300) and PCAST 2016 (0301) are owned by this library per protocol.
- Possible overlaps: Kassin/Dror/Kukucka 2013 (0322) and Dror 2020 (0324) may also be catalogued by 06_COGNITIVE_SCIENCE. Thompson & Schumann 1987 (0338) may be catalogued by 05/06.
- Live-count records (OSAC Registry 0309, Standards Library 0310, NRE 0347) hold snapshots dated 2026-10-27.

## Gap-fill round (2026-10-27)

**New record (1):** ATH-SRC-0362 — U.S. DOJ OIG, *A Review of the FBI's Handling of the Brandon Mayfield Case* (March 2006, unclassified/redacted, 330 pp.).
- Verified from the official PDF at `oig.justice.gov/sites/default/files/legacy/special/s0601/final.pdf`. The old `/special/s0601/` paths now return 404.
- The executive summary was read. Catalog now 63 records.

**Changed records:**
- **ATH-SRC-0317 (ENFSI guideline):** `url` and `verification_url` now point to the official PDF `enfsi.eu/wp-content/uploads/2016/09/m1_guideline.pdf`, confirmed as "Approved version 3.0", 128 pp. It is listed under "Evaluative Reporting" on enfsi.eu/documents/forensic-guidelines/, and no newer version is listed there. Method changed to `fetched_official_page`, and the third-party-copy limitation was removed.
- **ATH-SRC-0329 (Dror et al. 2021)** → `verified`. The PubMed abstract was read. Key findings now state both parts: the Nevada death-certificate data and the experiment with 133 pathologists. The limitation now records that PubMed links 23 published comment letters. The letters were not read, and the record stays flagged as contested and adult-only.

**Correction to a conclusion:** the deliverables framed Mayfield as "a famous example of confirmation bias". The OIG report makes it multi-causal:
1. An AFIS close non-match from a very large database.
2. Circular reasoning from the suspect's known prints.
3. Unreliable Level 3 detail.
4. Weak handling of discrepancies.

The OIG found **no compelling evidence** that non-blind verification, or high-profile pressure, caused the error. The atlas wording was updated to match.

**Deliverables edited:**
- `FORENSIC_SCIENCE_KNOWLEDGE_ATLAS.md` (literature-limits paragraph)
- `CSI_MYTHS_AND_SCIENTIFIC_CORRECTIONS.md`
- `cards/ATH-SRC-0331.md`
- `cards/ATH-SRC-0317.md` (link line; open question on later versions)

**Still open:**
- ATH-SRC-0353 (SWGTOX) and ATH-SRC-0354 (Henssge & Madea): PubMed has no abstract. ANSI/ASB 036 was not retried.
- FBI 2015 hair press release, NRE percentage, and the NDAA/NIJ/AAAS items were not retried.
- Arabic forensic sources remain a gap.
