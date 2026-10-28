# Agent report — W2-BUSINESS (pricing, business models, procurement, funding)

**Date:** 2026-10-27 · **ID block:** ATH-SRC-2200…2299 (used 2200–2264) · **KO code:** 09C

## 1. Counts
- **Sources verified:** 65 (ATH-SRC-2200 … ATH-SRC-2264) in `09_COMPETITIVE_INTELLIGENCE/_data/sources_w2_business.jsonl`. Validated as JSONL; no ID collisions. No URL duplicates against `sources_master.jsonl` or the other wave-2 files.
- **Existing sources reused rather than re-cataloged:** 0828, 0806, 0807, 0815, 0800, 0849, 0880, 0219, 0846, 0847, 0890, 0891, 0894, 0831, 0832, 0833, 0830, 0202, 0879, 0719, 1137, 1155, 1162, 1179, 1100, 1102, 1103, 1128, 1135, 1129, 1130, 1150, 1168, 1512–1516, 1541, 1545–1547, 1556, 1558, 1911, 1913, 0965.
- **Knowledge objects:** 7 product opportunities (KO-PO-09C-001 … 007) in `_data/knowledge_objects_w2_business.jsonl`.
- **Deep cards:** none. The brief did not ask for cards; the analysis lives in the three Markdown files.

## 2. Files produced
| File | Content |
|---|---|
| `09_COMPETITIVE_INTELLIGENCE/BUSINESS_MODEL_AND_PRICING_EVIDENCE.md` | B2C and B2B price benchmarks; business-model evidence; store fees and VAT; carrier billing; procurement routes in KSA, UAE, Egypt and Jordan; decision list P1–P7 |
| `09_COMPETITIVE_INTELLIGENCE/FUNDING_AND_PARTNERSHIP_LANDSCAPE.md` | VC climate from MAGNiTT and Wamda; an eligibility table for 12 programmes; national gaming strategies; foundations; platform and telco partners; a staged funding plan |
| `09_COMPETITIVE_INTELLIGENCE/UNIT_ECONOMICS_SCENARIOS.md` | Three scenarios (B2C, school, hybrid) with break-even logic and sensitivity tables, all tagged `[استنتاج استثماري]` |
| `_data/pricing_benchmarks.csv` | 637 dated rows: App Store SA/AE/EG/US for 21 apps (IAP lists), Steam regional prices for 5 games, and 23 web-verified school, teacher, box and telco prices; USD at the official peg; ex-VAT price |
| `_data/unit_economics_model.py` + `_data/unit_economics_model.csv` | Reproducible Python model, 237 rows; every row has `basis` (a source ID or library file) and `tag` (fact / calculation / assumption) |
| `_data/sources_w2_business.jsonl`, `_data/knowledge_objects_w2_business.jsonl`, this report | — |

## 3. Method
- **Store data:** apps.apple.com product pages expose up to about 10 IAP items each. I captured them for SA/AE/EG/US alongside the iTunes Lookup API, about 1.5 s per request. Steam prices came from `appdetails?cc=`. User-Agent: ATHAR-Research-Library/2.0.
- **Benchmarks:** RevenueCat SOSA 2026 figures were checked directly in the page text, because a summarizer had flagged internal inconsistencies. GameAnalytics figures were checked on gameanalytics.com.
- **Procurement and funding:** facts come only from official pages: MoF UAE, MoE UAE, ADEK, NeLC, KAUST, Hub71, MoET, MCIT, PIF, Dubai Media Office, QNA, RDIA, and the foundations' own sites. trade.gov and an open-access OBP chapter were used for Jordan and Egypt.
- **Searches:** WebSearch in English and Arabic.

## 4. Interpretations made autonomously (owner away)
1. **"Comparable apps" set.** I treated the following as comparable: mystery games (Golden Idol, Duskwood, Criminal Case, Elmwood, Enigmic, June's Journey), interactive story (Choices, Episode), Arabic edutainment (Lamsa, I Read Arabic, 3asafeer), learning subscriptions (Duolingo, Brilliant, Noon, Abwaab), and Arabic or regional audio and reading (Storytel, Audible, Abjjad, Wajeez, Rufoof, Anghami). Obra Dinn has no iOS listing in these storefronts, so I used Steam.
2. **Already-cataloged apps were not re-cataloged.** Duskwood, Enigmic, Elmwood, Golden Idol and Criminal Case keep their existing IDs; their new prices sit in the dataset record ATH-SRC-2200 and the CSV.
3. **Billing period** was inferred from SKU names only. 122 rows are left as "subscription_period_not_stated".
4. **Unit-economics price choice.** SAR 29.99/month and 249.99/year are my test points, placed inside the documented band. They are labelled as assumptions.
5. **Hourly cost grid.** 1× is the GASTAT all-sector Saudi average wage converted to an hourly rate. That is a floor, not a market rate for writers or engineers; 2× and 3× are assumption grid points. I found no official wage data for creative or tech specialists.
6. **LTV base.** RevenueCat's observed Education RLTV ($22.82) is the conservative base. My own build-up ($34.27) is shown only as optimistic, because MEA renewal and MRR trends are weaker.
7. **Fixed cost** covers MVP engineering hours plus season-1 content hours only. Platform, compliance, sales and marketing are excluded and stated as such.
8. **ARABIC_TOKEN_COST_MEASUREMENT.md** existed when I reached the model step. I used its session-cost examples (§3.3) for AI cost.

## 5. Blockers
- adjust.com returned 429 (Vercel checkpoint), so the Adjust CPI is taken from secondary summaries and flagged `needs_expert_review`.
- qstp.org.qa returned 403, qrdi.org.qa returned 404, and monshaat.gov.sa reset the connection. None of the three is cataloged.
- etimad.sa returns a JS shell; the Etimad process is cited via the existing 1513/1514.
- The ZATCA VAT page is JS-rendered, so I used PwC Tax Summaries for the 15% rate.
- MAGNiTT and Wamda full reports are gated; only public summaries were used, and they give no EdTech sector figures.
- Google Play IAP lists are not exposed on its pages, so no Android prices were captured.
- Shared scratchpad incident: another team overwrote my helper `lookup.py`, and I had briefly moved the shared `dl/` folder. I restored it immediately and moved my work to `scratchpad/w2biz/`. No library files of other teams were touched.

## 6. Unverified candidates (not cataloged)
- **Monsha'at programmes and Misk:** no fetchable official page with eligibility for a foreign company.
- **QSTP XLR8 / QRDI funding:** site blocked.
- **Liftoff 2025 Casual Gaming report CPI by region:** regional CPIs not on the public page.
- **AppMagic Monetization 2025:** fetch failed.
- **Dubai Future Foundation / Area 2071 current programmes:** only old press results found.
- **Berytech ScaleSmart 2026 terms:** the homepage shows "apply before Nov 30", but terms were not verified.
- **Kafalat current terms:** only a 2014 guide was found (cataloged as low-confidence history).
- **Apple Arcade regional price:** not on the SA/AE pages.
- **iEN (عين) content-partner process:** only unofficial blogs found.

## 7. Top 5 findings that should change ATHAR's design or plan
1. **Lead with school or class licences.** About 14–79 schools a year at $2,199 recover MVP plus season-1 cost across the grid; the mid case needs 28–53. B2C alone needs about 1,400–7,600 paying families, i.e. 68k–382k installs at a 2% conversion rate.
2. **Paid acquisition does not break even at category medians.** Break-even CPI is about $0.46 (2% × $22.82), against a $0.56 global gaming CPI. B2C must grow organically, through school-to-home, audio and referral.
3. **Price inside the Arabic band.** Use SAR 21–40/month and 205–350/year, add an Egypt tier at about 50–60%, offer a 7-day trial with one full case, and run monthly and annual plans together (MEA buyers lean 52–55% monthly).
4. **No currencies or paid hints.** F2P mystery revenue is concentrated in heavy spenders (top 5% of payers ≈ 48% of IAP revenue), which conflicts with R9 for minors.
5. **Procurement reality.** UAE federal registration is open to free-zone companies. Etimad requires a Saudi RHQ, Egypt buys centrally through EKB, and Jordan's realistic route is donor programmes. Selling to private schools and partnering with platforms are the fast routes.

## 8. Top 5 open questions / gaps for human review
1. **What price will a Gulf private school actually accept** for Arabic critical-thinking enrichment? No published Arab school price exists. Experiment 3 needs a real 3-tier price offer.
2. **Saudi legal opinion** on whether a certificate-free enrichment game falls outside NeLC licensing (Art. 7, ATH-SRC-2233).
3. **Real hourly costs** for an Arabic narrative writer, learning designer and engineer (Dubai vs Riyadh vs Beirut). The model's biggest lever is this cost and actual authoring hours.
4. **MENA-specific CPI for parent-targeted ads and the parental-consent drop-off.** Needs a fake-door test.
5. **Funding terms needing direct contact:** MBRIF guarantee amounts and whether IFZA companies qualify; Hub71 equity %; WISE funding terms; KAUST TAQADAM's next-cycle date.
