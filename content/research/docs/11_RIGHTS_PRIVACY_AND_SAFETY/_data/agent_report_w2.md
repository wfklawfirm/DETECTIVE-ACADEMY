# Agent report — W2-LEGAL (wave 2)

Date: 2026-10-27 · Block: ATH-SRC-1800 … 1899 (used 1800–1859) · KO code 11

> Legal research for product design, not legal advice. Every jurisdiction-level conclusion requires review by licensed counsel in that jurisdiction.

## Counts

**Sources:** 60 new records in `_data/sources_w2.jsonl` (ATH-SRC-1800–1859, sequential, no gaps). Validated with python: 60 unique IDs, all schema enums valid, no dangling cross-references.

| Breakdown | Values |
|---|---|
| Library | 47 × `11_RIGHTS_PRIVACY_AND_SAFETY`; 13 × `05_INVESTIGATIVE_REASONING` (1820–1831, 1856) |
| Grade | A 25 · B 9 · C 13 · D 13 |
| Review status | 48 verified · 12 needs_expert_review |

**Duplicates removed before final numbering:** 4 records duplicated existing catalog items.
- ALLaM 1173, Jais 1174, Fanar 1175, OWASP 0952.
- Their new findings are logged below as proposed updates, so wave-1 IDs are reused.
- The other new records were renumbered sequentially.

**Knowledge objects:** 4 in `_data/knowledge_objects_w2.jsonl`.
- KO-PO-11-003: country-keyed guardian consent.
- KO-PO-11-004: regional/sovereign AI processing.
- KO-PO-11-005: school-mode compliance pack.
- KO-CD-11-001: procedurally realistic Arab justice officials.

**Deep cards:** none (not requested for W2-LEGAL).

## Files produced or edited

**New:**
- `11_RIGHTS_PRIVACY_AND_SAFETY/ARAB_MARKET_LAUNCH_COMPLIANCE_MATRIX.md`: 10 countries × 9 requirement columns, plus a launch verdict per country.
- `11_RIGHTS_PRIVACY_AND_SAFETY/TRADEMARK_AND_LICENSE_REGISTER.csv`: 33 rows; columns per the brief, plus jurisdiction, classes and status.
- `05_INVESTIGATIVE_REASONING/ARAB_CRIMINAL_PROCEDURE_CONTEXT.md`
- `_data/sources_w2.jsonl`, `_data/knowledge_objects_w2.jsonl`, this report.

**Surgical edits:**
- `CHILD_AND_TEEN_PRIVACY_REQUIREMENTS.md`
  - Header note.
  - Qatar and Lebanon rows rewritten from the primary texts.
  - "Not yet verified" paragraph replaced with closed/open lists.
  - New §1.1أ: capacity table for 10 countries.
  - §1.3 launch order and new point 8 (school AI rules).
  - Sources line.
- `INTELLECTUAL_PROPERTY_RESEARCH.md`
  - Executive summary items 6–7.
  - New §8.1 (trademark search results) and §12.1 (tool, model and content licences).
  - CC BY-SA row.
  - §13.2: Kadrey status, Ross appeal, NYT/OpenAI MDL, revised interpretation.
  - §13.3: Getty appeal. §13.3أ: GEMA commentary.
  - Counsel questions 5 and 5أ; sources line.
- `COMMERCIAL_USE_DECISION_MATRIX.md`
  - Row 3b rewritten from the legal code.
  - Row 7 expanded; new rows 7b and 7c.
  - Decision-tree step 2 now points to the register.
  - Step 6 adds the Ross update and the no-competitor-materials rule.
- `CONTENT_AND_SAFETY_GOVERNANCE.md`
  - G5 expanded with procedural realism; new G4أ store-rating gate.
  - Model-licence note; P0 breach deadlines completed for Bahrain, Qatar and Lebanon.
  - New §6أ: regional platform risks.

## Method

**Network:** official portals were reached through curl with the addendum User-Agent and at least 1 s between requests:
- Lebanese University CIJ (legiliban.ul.edu.lb), through its GET search parameters.
- WIPO Lex PDFs; qanoon.om; LLOC Bahrain; MISA (official Saudi Civil Transactions Law translation).
- USPTO trademark-search JSON backend and WIPO Madrid Monitor record pages.
- Hugging Face API and raw READMEs; ai.google.dev; GitHub raw LICENSE files; heptapod (Harlowe).
- creativecommons.org; phet.colorado.edu; Third Circuit opinion PDF; CourtListener RECAP PDFs.
- National Archives Find Case Law; Constitute Project; IARC; Google Play Help; u.ae; Embassy of India UAE.

**Quota use:** about 40 WebSearch calls (discovery) and 5 WebFetch calls (CoE study, College of Policing, Tamimi media law, MediaLaws GEMA, Upsilon Morocco).

**Quotes:** none reproduced beyond short phrases; findings paraphrased.

## Gaps closed (relative to RESEARCH_GAPS)

**G01 (data protection):**
- **Qatar Law 13/2016:** full Arabic text read (Al-Sharq reproduction of 3 Nov 2016).
  - Children's data is "special nature" data requiring a permit (Art. 16).
  - Guardian express consent for child-directed sites (Art. 17).
  - Controllers must not restrict cross-border flows (Art. 15).
  - Breach notice without an hour limit (Art. 14).
- **Lebanon Law 81/2018:** official text on legiliban (Arts. 85–109).
  - Declaration to MoET (Art. 95) with exemptions (Art. 94).
  - Transfers mentioned in the declaration but not prohibited (Arts. 96(12), 98(8)).
  - No child rule, no breach duty, no authority.
- **Egypt:** Executive Regulations 816/2025 adopted 1 Nov 2025 and in force 2 Nov 2025 (DPA tracker). The licensing and transfer-permit content is from a law-firm summary.
- **UAE PDPL executive regulation:** still not issued per the latest source (Pinsent Masons, modified Dec 2025; u.ae page lists none). This is a negative finding.
- **Bahrain:** 72-hour breach notice; adequacy list of 83 countries incl. US/EU (Resolutions 42–43/2022, secondary).
- **Oman:** "child" = under 18 Gregorian (Child Law 22/2014).
- **Capacity ages for all 10 countries:** KSA 18 Hijri (official translation); Jordan 18; Lebanon 18; Oman 18; Morocco 18 (discernment 12); Egypt 21; Kuwait 21; Bahrain 21; Qatar 18 (secondary); UAE 18 Gregorian since 1 Jun 2026 (press).

**G02 (age ratings):**
- Gmedia (KSA) joined IARC in 2024 and started rating in 2026.
- Google Play maps the UAE to PEGI and other Arab states to IARC Generic (16+ allows depiction of criminal activities); refused classification removes an app per territory.
- UAE Media Law 55/2023 covers e-games; its Executive Regulation has been effective since 31 Oct 2024; Cabinet Decision 42/2025 fines failure to follow age classifications (AED 5k–100k), secondary.
- Egypt's SCMR blocked Roblox (Feb 2026, press).
- Still open: whether Gmedia or the UAE Media Council require a separate rating or licence for a foreign educational app distributed only via app stores.

**G12 (trademarks):**
- USPTO: 29 live Agatha Christie Ltd records and 23 live Conan Doyle Estate records, with numbers and classes.
- Third-party SHERLOCK marks identified.
- Madrid Monitor: designations of 6 IRs; no Arab designations in those.

**G13 (AI litigation):**
- Ross affirmed by the 3d Cir. (29 Sep 2026, official PDF).
- Kadrey: remaining torrenting/distribution claims; SJ hearing 25 Feb 2027; interlocutory appeal denied 8 Jul 2026 (tracker).
- Getty: permission to appeal granted to Getty on secondary infringement; Stability's TM appeal refused (official).
- NYT/OpenAI MDL at summary-judgment stage; DOJ Statement of Interest of 1 Sep 2026 (cited in the 3d Cir. opinion).

**G15 (licences):**
- Twine: editor GPL-3.0; formats zlib/BSD-2/MIT.
- PhET: CC BY 4.0 only for sims published before 29 Mar 2026; trademark terms.
- CC BY-SA 4.0 s.3(b) read; OWASP CC BY-SA; College of Policing NCL default.
- Gemma Terms (1 Apr 2026) and Prohibited Use Policy; Gemma 4 is Apache-2.0.
- ALLaM: no LICENSE file; Fanar-2 is a Gemma-3 derivative.

**G23 (Arab criminal procedure):**
- Official or primary texts: Lebanon CCP (incl. Art. 91, minors heard "for information") and Law 422/2002; Egypt CPL 174/2025 (in force 1 Oct 2027); KSA LCP 2001.
- Secondary: Jordan CCP and Juveniles Law 2014; UAE juvenile law (u.ae); UAE CPL (embassy note); Saudi Juveniles Law.
- Constitutional innocence clauses for 8 states; UN child-witness model law.

## Interpretations made autonomously (owner away)

1. **"Official or authoritative texts".** Accepted as primary when:
   - the Lebanese University CIJ database and qanoon.om are official-like legal databases;
   - the newspaper reproduction of Qatar's law is the full promulgated text, graded A but flagged for gazette check;
   - the MISA-hosted Bureau of Experts translation counts as official.

   Law-firm and press items are D/C and mostly needs_expert_review.
2. **Library assignment.** Criminal-procedure sources went to library `05_INVESTIGATIVE_REASONING`, even when they are legal texts, as instructed. Data-protection, capacity and licence items stayed in 11.
3. **Capacity versus "valid consent for minors".** Recorded civil majority and discernment ages. The application to data-protection consent is marked as interpretation wherever the PDPL does not define the age.
4. **Launch verdict scale:** "go" was not given to any country; best is "go-with-conditions". Egypt's verdict is "blocked" only for the AI-chat feature, and Kuwait "blocked pending counsel".
5. **Wave-1 records not edited.** Wave-1 files outside my list were not touched. Proposed updates are listed below for the merge step.

## Proposed updates to existing records (for the merge step)

| ID | Proposed change | Basis |
|---|---|---|
| ATH-SRC-1063 (DLA Piper, Qatar) | Mark as superseded for article content by 1800; keep as secondary. Its "72-hour" figure is regulatory guidance, not in the Law | ATH-SRC-1800 |
| ATH-SRC-1064 (DLA Piper, Lebanon) | Superseded by 1801. Correct "Ministry of Economy and Trade licence for health data": licences come from the Health/Justice/Defence-Interior ministers (Art. 97); MoET receives declarations | ATH-SRC-1801 |
| ATH-SRC-1173 (ALLaM) | Add limitation: the repo has no LICENSE file despite the card's reference; licence is the metadata tag only; last modified 14 Jul 2025 | HF API |
| ATH-SRC-1175 (Fanar-2) | Add: base_model google/gemma-3-27b-pt, so Gemma Terms likely flow down; no LICENSE/NOTICE file | README + ATH-SRC-1836 |
| ATH-SRC-1174 (Jais 3) | Add out-of-scope list and custom remote code note; modified 25 Oct 2026 | README |
| ATH-SRC-0952 (OWASP) | Set rights_status OPEN_LICENSE, license "CC BY-SA 4.0 (unless otherwise specified)" | site footer |
| ATH-SRC-0902 (Twine) | Add story-format licences (zlib/BSD-2/MIT) | ATH-SRC-1837 |
| ATH-SRC-0400–0402 (College of Policing) | rights_status LICENSED (Non-Commercial College Licence), commercial_reuse no | ATH-SRC-1840 |
| ATH-SRC-1074 (Ross certification) | Add outcome: affirmed by the 3d Cir. on 29 Sep 2026 | ATH-SRC-1841 |
| ATH-SRC-1032 (Getty) | Add: permission to appeal granted to Getty on secondary infringement (16 Dec 2025) | ATH-SRC-1843 |
| ATH-SRC-1062 (CMS Egypt) | Add in-force date 2 Nov 2025 per the DPA tracker | ATH-SRC-1805 |
| RESEARCH_GAPS G01/G02/G12/G13/G15/G23 | Update "what remains" per the "Still open" list below | this report |

## Blockers

**Blocked by Cloudflare or a JavaScript challenge** (not bypassed):
- uaelegislation.gov.ae (UAE CTL, Media Law, Juvenile Law, CPL texts)
- alp.unescwa.org; merlin.obs.coe.int; WIPO Global Brand Database (CAPTCHA); tamimi.com (read via WebFetch)

**Connection reset by the egress proxy:**
- adala.justice.gov.ma (Morocco 09-08 official text); portal.jordan.gov.jo; alkarama.org
- college.police.uk licence pages (read via WebFetch); prod.hrsd.gov.sa (KSA juveniles law PDF)

**Other access failures:**
- Al Meezan Qatar: HTTP 500.
- JS-only pages: EUIPO/TMview, SAIP, UAE MoE trademark search, OMPIC, Egypt PDPC portal, PhET's post-2026 licensing page, Constitute terms.

**Image-only PDF:** the Manshurat Egypt Child Law PDF (no Arabic OCR available). The CRIN Arabic .doc was used instead.

## Unverified candidates (not catalogued)

| Candidate | Why |
|---|---|
| UAE Federal Decree-Law 25/2025 Civil Transactions Law (official text) | Portal blocked; only the Al Bayan report (1858) |
| UAE Federal Law 6/2022 on juveniles (text); UAE Media Law 55/2023 text and Media Council game-rating guide | Portal blocked |
| Saudi Juveniles Law (BOE/HRSD official text) and the MoE/SDAIA generative-AI guidebook PDF | Host refused; press/Saudipedia only |
| Egypt Executive Regulations 816/2025 Arabic gazette text | Not located publicly |
| Morocco Law 09-08 Bulletin Officiel text | adala.justice.gov.ma reset |
| Qatar Civil Code Law 22/2004 text | Only the CRIN/DLA Piper 2014 report |
| Bahrain Resolutions 42–46/2022 texts | Only the Clyde & Co summary |
| GEMA v OpenAI appeal (OLG München) | No source found stating appeal status |
| Getty v Stability Court of Appeal hearing/outcome | Not found as of 27 Oct 2026 |
| Kadrey order of 8 Jul 2026 (text) | Tracker report only (RECAP entry not available) |
| Kuwait comprehensive PDPL | Searches returned only the CITRA regulation |
| Arab national trademark registers for Christie/Doyle marks and «المغامرون الخمسة» | No public machine-searchable access |

## Top 5 findings that should change ATHAR's design

1. **Consent age is country- and calendar-specific.** It is 17.5–21 years, never 13: KSA 18 Hijri; Egypt, Kuwait and Bahrain 21; the UAE moved to 18 Gregorian on 1 Jun 2026. Build a per-country age table and a guardian path that can extend to 21 for payments (KO-PO-11-003).
2. **Qatar is stricter on children than assumed and looser on transfers:**
   - Children's data needs a prior permit (Art. 16) and guardian consent plus a parental dashboard (Art. 17).
   - Transfers abroad cannot be restricted (Art. 15).

   Lebanon, by contrast, regulates via an MoET declaration and has no child rule.
3. **Egypt is the hardest market for AI chat.** Its regulations (in force since Nov 2025) require a licence plus a destination-specific transfer permit and transfer consent. The media regulator has already blocked Roblox. Ship authored content first, or process in-region (KO-PO-11-004).
4. **Brand and marketing must avoid every Christie/Doyle name.** Live US/EU marks cover games, education and entertainment (POIROT, MARPLE, SHERLOCK, HOLMES, WATSON, MORIARTY). "Think like Sherlock" is out.
5. **Store ratings and school AI policies are now hard product constraints:**
   - Gmedia now rates via IARC, and IARC Generic puts "depiction of criminal activities" at 16+. Keep cases at 12+ (non-graphic, consequences shown).
   - The UAE MoE bans GenAI under 13 and bars student PII going into AI. Send only pseudonymous case text to models (KO-PO-11-005).

## Top 5 open questions for counsel or experts

1. **Bahrain, Kuwait and Egypt:** is "full capacity" for data-protection consent and paid subscriptions 21? How should 18–20-year-olds be treated?
2. **Egypt:**
   - actual licence and transfer-permit procedure, fees and timelines under 816/2025;
   - whether in-Egypt processing avoids the permit;
   - the SCMR's stance on crime-themed educational games.
3. **KSA and UAE:** does a foreign educational app distributed only through app stores need a separate Gmedia/Media Council rating, clearance or licence beyond IARC/PEGI? Are UAE "education platforms" exempt under the Child Digital Safety Law?
4. **Licences:** is Fanar-2 governed by Apache-2.0 or by the Gemma Terms? Can ALLaM's metadata-only Apache tag be relied on? What are PhET's terms after 29 Mar 2026?
5. **Trademarks:** national register searches (UAE, KSA, Egypt, Lebanon, Morocco, EUIPO) for the Christie/Doyle marks and «المغامرون الخمسة»; whether a descriptive literary mention in lessons is safe in each market.

## Still open (for RESEARCH_GAPS)

**G01:**
- Egypt and Morocco official regulation texts; UAE PDPL regulation (watch).
- Kuwait CITRA scope; Qatar gazette check.
- Lebanon reform bill status.

**G02:** applicability of Gmedia or Media Council rules to app-store-only educational apps; the UAE game-rating guide itself.

**G12:** national registers.

**G13:**
- GEMA appeal; Getty Court of Appeal.
- Kadrey SJ (Feb 2027); OpenAI MDL SJ ruling.
- Bartz final judgment effects.

**G15:** PhET post-2026 terms; Gemma/Fanar licence stacking.

**G23:** official texts for the UAE CPL and juvenile law, the Saudi Juveniles Law and the Jordan CCP; Arabic research on false confessions (not reached).
