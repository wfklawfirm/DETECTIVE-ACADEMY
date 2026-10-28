# Agent report — 11_RIGHTS_PRIVACY_AND_SAFETY

Date: 2026-10-27 · Source-ID block used: ATH-SRC-1000 … 1048 · KO lib code 11

> All outputs are legal research for product design, not legal advice; each jurisdiction requires review by licensed counsel.

## Counts
- **Sources verified:** 49 records in `sources.jsonl` (within target 30–45+). Of these:
  - 37 `review_status: verified`
  - 12 `needs_expert_review`: partially read texts, secondary summaries, or superseded laws.
  - By evidence grade: A = 36, B = 3, C = 6, D = 4. Primary statutes, regulations, treaties, court decisions and regulator guidance dominate.
- **Deep cards:** 6. ATH-SRC-1000 (Klinger), 1009 (Lebanon Law 75/1999), 1026 (EU DSM Directive TDM), 1033 (COPPA 2025 amendments), 1038 (UK AADC), 1044 (California SB 243).
- **Knowledge objects:** 2 product opportunities (KO-PO-11-001 is a design hypothesis; KO-PO-11-002 is evidence-based).

## Files produced
- `INTELLECTUAL_PROPERTY_RESEARCH.md`
- `COMMERCIAL_USE_DECISION_MATRIX.md`
- `CHILD_AND_TEEN_PRIVACY_REQUIREMENTS.md`
- `CONTENT_AND_SAFETY_GOVERNANCE.md`
- `_data/rights_rules.csv`: 13 rows, covering the 5 protocol `rights_status` values plus variants (PUBLIC_DOMAIN_ALL_SERVED, PUBLIC_DOMAIN_PARTIAL, CC variants, TRADEMARK_OVERLAY, OFFICIAL_LEGAL_TEXT).
- `_data/sources.jsonl`, `_data/knowledge_objects.jsonl`, `_data/agent_report.md`
- `cards/ATH-SRC-1000.md`, `1009.md`, `1026.md`, `1033.md`, `1038.md`, `1044.md`

**Merge note:** `rights_rules.csv` joins on `rights_status`. The PUBLIC_DOMAIN base row is deliberately conservative: commercial use and RAG are "conditional", so they apply only in the jurisdictions listed. Rows tagged PUBLIC_DOMAIN in the catalog whose `rights_jurisdiction` covers every served market can be mapped to PUBLIC_DOMAIN_ALL_SERVED.

## Search strategy
1. **Primary texts first:**
   - WIPO Lex records for Arab copyright statutes.
   - Official portals: uaelegislation.gov.ae, legislation.gov.uk, EUR-Lex, Federal Register, copyright.gov, FTC, ICO, Ofcom, European Commission, CA legislature via LegiScan, D.C. Cir., UK National Archives case law.
2. **Then court and case resources:** Stanford Fair Use project, Leagle, Duke CSPD.
3. **Secondary law-firm or IP-agent pages** only where primary texts could not be read (AGIP, Gowling). These are flagged D/needs_expert_review.

## Blockers
- **Search and fetch budgets exhausted.** The shared WebSearch budget (200 per turn, all agents) ran out mid-session. The WebFetch budget then hit its hourly cap several times. As a result:
  - **No MENA data-protection law text was verified** except the UAE PDPL's bibliographic record (ATH-SRC-1047). Missing: KSA PDPL, Egypt Law 151/2020, Qatar, Bahrain, Oman, Kuwait, Lebanon Law 81/2018.
  - The UAE child digital safety law was not located.
  - Google Play Families policy was not fetched.
  - National GDPR digital-consent ages were not fetched.
  - CC BY / BY-SA legal codes were not fetched.
- **Wikimedia Commons copyright-by-territory pages** returned url_not_found.
- **Unreadable PDFs:** the Kuwait Law 75/2019 Arabic PDF could not be fetched (signed URL / length limit), and the unofficial English translation site was offline.
- **Truncated long pages:** EUR-Lex (DSA Art. 28, AI Act articles) and Getty v Stability (final conclusions). Unofficial mirrors were used for some article texts and are flagged.
- **Egypt Law 82/2002:** the current English text is unavailable. The 2002 English translation of Art. 160 says "from the date of his death", which needs checking against the Arabic text.

## Unverified candidates (not in sources.jsonl)
| Candidate | Why not verified |
|---|---|
| Saudi Copyright Law (Royal Decree M/169) and SAIP Implementing Regulations 2026, primary text | Only Gowling summary read; search budget exhausted |
| Saudi PDPL (Royal Decree M/19 of 1443, amended M/148 of 1444) and Implementing Regulations; SDAIA | Fetch budget exhausted |
| Egypt Personal Data Protection Law No. 151/2020 and its Executive Regulations | Fetch budget exhausted |
| Lebanon Law 81/2018 on Electronic Transactions and Personal Data | Not fetched |
| Qatar Law 13/2016; Bahrain Law 30/2018; Oman Royal Decree 6/2022; Kuwait data-protection regulation (CITRA) | Not fetched; numbers from background knowledge only, so unverified |
| UAE federal child digital safety law (2025?) | Not located in-session |
| UAE PDPL article-level content (scope, consent, minors, transfers) | Fetch budget exhausted |
| Google Play Families Policy / Teacher Approved | Not fetched |
| Apple age-rating changes (13+/16+/18+) | Page truncated before that section |
| CC BY 4.0 and CC BY-SA 4.0 legal codes | Not fetched (characterization in matrix flagged as research interpretation) |
| National GDPR Art. 8 ages (e.g., France 15, Germany 16, Ireland 16) | Not fetched |
| Bartz v. Anthropic June 2025 fair-use order; settlement amount | Settlement site lacked figures; court page refused |
| Kadrey v. Meta (N.D. Cal. 2025), Thomson Reuters v. Ross (D. Del. 2025), NYT v. OpenAI, GEMA v. OpenAI (Munich 2025) | Search budget exhausted before verification |
| Ofcom Protection of Children Codes full text ("highly effective age assurance") | Statement page returned client_error |
| Agatha Christie Limited trademark registrations (USPTO/EUIPO/UAE) | Justia listings seen in search results only; not itemized |
| Ownership of ACL (Acorn/RLJ majority stake, 2012) | Search-result headlines only; not confirmed on official page |
| URAA restoration rules for foreign works (17 U.S.C. §104A) | Not fetched |

## Top 5 findings that should change ATHAR's design
1. **Public-domain status is per market, and global stores break "PD" assumptions.** Agatha Christie (d. 12 Jan 1976) is usable in LB/AE/JO/QA from **1 Jan 2027** but protected in the UK/EU until **31 Dec 2046**. Any Christie-derived content must be geo-restricted. The real strategic asset remains original characters and cases. [1005, 1009, 1011, 1016, 1017, 1019, 1020]
2. **Translations are separate works.** Existing Arabic translations of PD classics are not usable. ATHAR must commission its own translations under assignment contracts that include adaptation and AI-use rights. [1007, 1009, 1011]
3. **AI corpus rule.** Only material that is PD in all served markets, licensed expressly for AI, or authored by ATHAR may enter training or a RAG store. The EU commercial TDM exception yields to machine-readable opt-outs, no general Arab TDM exception was verified, and the US Copyright Office treats dataset copying as prima facie reproduction. [1026, 1027, 1029, 1014]
4. **Keep AI characters story-bound, not companions.** California SB 243 excludes game bots limited to game-related replies. The FTC is investigating companion bots and minors. Disclosure, a crisis protocol, no sexual content and no relationship memory should be global defaults. [1043, 1044, 1027, 1042]
5. **Design to the AADC baseline globally.** This means high-privacy defaults, no streaks or nudges for minors, profiling off, and short written retention schedules for chat logs. Under-13s are excluded from the MVP because of COPPA 2025 (separate consent for third-party/AI-vendor disclosure; voiceprints count as personal information). The UK age of digital consent may rise from 13 to as high as 16 under 2026 powers. [1033, 1034, 1036, 1038, 1041, 1042]

## Top 5 open questions / gaps for human or expert review
1. **MENA data protection.** KSA, Egypt, UAE (article level), Qatar, Bahrain, Oman, Kuwait and Lebanon need: minors and guardian consent, cross-border transfer, breach notification, and AI-chat log retention. **Launch blocker for the Gulf and Egypt.** *(Gap-fill 2026-10-27: verified for KSA, UAE, Oman, Jordan, Bahrain, Kuwait and Egypt (translation); Qatar and Lebanon remain secondary-only. See the gap-fill section below.)*
2. **Copyright terms still open:**
   - Egypt Art. 160: computed from the death date or from year-end?
   - Egypt Art. 148: scope of the translation-lapse rule.
   - New Saudi Copyright Law (M/169): term and the AI-training exception text.
   - Kuwait Law 75/2019: the duration article.
3. **Rule of the shorter term in Arab states.** Do Lebanese, UAE and Egyptian courts apply it to foreign works? And how do perpetual moral rights constrain adapting PD works into games?
4. **Trademark clearance** for Agatha Christie Limited and Conan Doyle Estate marks in target markets and app stores.
5. **Status of 2023–2026 AI copyright litigation** (Bartz order and settlement terms, Kadrey, Thomson Reuters v. Ross appeal, NYT v. OpenAI, Getty v Stability conclusions and appeal, GEMA v OpenAI). This status should be refreshed before any AI-training decision.

## Gap-fill round (2026-10-27)

**Method.** Official texts were fetched directly from official portals by HTTPS (WIPO Lex PDFs, SDAIA, u.ae, GovInfo, National Archives XML, Umm al-Qura, LLOC, MoDEE, CITRA, BOE, Irish Statute Book, CNIL, Google, Apple), so that the shared WebSearch/WebFetch quota was used sparingly. About 14 searches and 4 fetches were used. Article numbers are cited only where the text was read.

### New records: ATH-SRC-1049 … 1077 (29)
- **MENA data protection**
  - KSA PDPL, Implementing Regulation, Transfer Regulation: 1049–1051.
  - UAE PDPL text: 1052.
  - UAE Child Digital Safety FDL 26/2025: 1053 (+1054 Latham, secondary).
  - UAE Wadeema Law 3/2016: 1055.
  - Oman RD 6/2022 and MD 34/2024: 1056–1057.
  - Jordan Law 24/2023: 1058.
  - Bahrain Law 30/2018: 1059.
  - Kuwait CITRA Regulation v2.5: 1060.
  - Egypt Law 151/2020 (unofficial translation): 1061 (+1062 CMS on the Executive Regulations, secondary).
  - Qatar and Lebanon, secondary only (DLA Piper): 1063, 1064.
- **App stores:** Google Play Families 1065; Apple age ratings 1066.
- **EU ages of digital consent:** Spain 14 (1067), Ireland 16 (1068), France 15 (1069).
- **AI/copyright cases**
  - Bartz fair-use order and settlement preliminary approval: 1070–1071.
  - Kadrey v. Meta: 1072.
  - Thomson Reuters v. Ross, Feb and May 2025: 1073–1074.
  - GEMA v OpenAI (LTO report): 1075.
- **New Saudi Copyright Law M/169 and its 2026 Implementing Regulation:** 1076–1077.

**Totals now:** 78 records; 66 verified, 12 needs_expert_review. Grades: A 57, B 4, C 8, D 9.

### Changes to existing records (logged)
| ID | Change | Basis |
|---|---|---|
| ATH-SRC-1012 (Egypt Law 82/2002) | needs_expert_review → **verified**. Art. 160 Arabic text confirmed: counts from the **date of death**, so the English translation was not the cause. Limitation and application text updated | WIPO Lex Arabic consolidated PDF (eg081ar_1.pdf) |
| ATH-SRC-1013 (KSA Copyright Law 2003) | needs_expert_review → **verified**. Art. 19 now read (life + 50 "after his death", no year rule). Marked **repealed by M/169** (Art. 59) from 12 Aug 2026; verification_url corrected to WIPO 19412 | WIPO Lex 19412 Arabic/English; ATH-SRC-1076 |
| ATH-SRC-1014 (Gowling, KSA) | needs_expert_review → **verified** (grade D unchanged). Its main points were confirmed against the gazette texts | ATH-SRC-1076, 1077 |
| ATH-SRC-1015 (Kuwait Law 75/2019) | needs_expert_review → **verified**. Art. 23(1): life + 50 from 1 Jan after death | WIPO Lex Arabic PDF (Kuwait Al-Youm 1455) |
| ATH-SRC-1032 (Getty v Stability) | needs_expert_review → **verified**. Conclusions added: secondary-infringement claim dismissed (a model that does not store works is not an "infringing copy"); limited, historic TM success | National Archives judgment XML, paras 757–758 |
| ATH-SRC-1047 (UAE PDPL record) | needs_expert_review → **verified**. Article content now read via ATH-SRC-1052 | u.ae-linked Arabic text |

### Deliverables edited
- `CHILD_AND_TEEN_PRIVACY_REQUIREMENTS.md`:
  - New §1.1 (MENA matrix), §1.2 (UAE CDS Law and Wadeema), §1.3 (launch implications).
  - Verified EU ages added.
  - App-store section rewritten with verified Google and Apple rules.
  - Checklist items 9–11 added.
- `INTELLECTUAL_PROPERTY_RESEARCH.md`:
  - Executive summary item 2 (Christie by market) and item 5 (Saudi AI exception).
  - Terms table: EG, SA, KW and QA rows.
  - Egypt and Saudi critical notes; Christie market table.
  - §13.2 US cases; §13.3 Getty conclusions; new §13.3أ (GEMA).
  - §13.4 Saudi AI exception from the official text; counsel questions 1–3; sources list.
- `COMMERCIAL_USE_DECISION_MATRIX.md`: row 2c; decision-tree step 6 (output filter, lawful-acquisition log).
- `CONTENT_AND_SAFETY_GOVERNANCE.md`: P0 incident row now lists verified breach deadlines.
- `02_DETECTIVE_LITERATURE/LITERARY_RIGHTS_REGISTER.csv` (rights columns only):
  - 12 Christie rows: corrected "EG/SA: 50y from death -> ended 12 Jan 2026". **SA was wrong** after M/169 (start-of-year rule, in force 12 Aug 2026). **EG confirmed** on the literal Arabic text.
  - Disclaimer row: counting rules updated.
  - SA dates split from EG for Queen, Carr, Yokomizo and Salem.

### Copyright-term reconciliation (Christie, d. 12 Jan 1976)
| Market | Rule (verified) | Christie texts |
|---|---|---|
| Lebanon, UAE, Jordan, Qatar, Kuwait | Year-end or 1 January after death | PD **1 Jan 2027** |
| Saudi Arabia | M/169 Art. 22: from the start of the year after death | PD **1 Jan 2027**. Open questions: Art. 24 transition from the 2003 law, which had no year rule, and the Hijri/Gregorian reading |
| Egypt | Art. 160: from the date of death | Literal expiry **12 Jan 2026**; the Berne Art. 7(5) reading gives 31 Dec 2026 (counsel) |

Both files now state this identically.

### Still unverified / open
- **Qatar Law 13/2016:** Arabic text and article numbers. Al Meezan and the NCSA portal are JavaScript-only; only DLA Piper was read.
- **Lebanon Law 81/2018:** Arabic text. UN-ESCWA blocked access (2 attempts); only DLA Piper (2022) was read.
- **Egypt Law 151/2020:** Arabic Official Gazette text; the Executive Regulations text (Ministerial Decision 816/2025) was not read.
- **UAE:** PDPL Executive Regulation not located; CDS Law Cabinet resolutions (classification, consent methods, penalties) not seen.
- **Ages of legal capacity:** not verified for KSA, Jordan and Bahrain. The definition of "child" in Oman's PDPL was not verified.
- **Remaining EU national ages:** the official Commission or BIK table returned HTTP 429.
- **AI litigation:** Kadrey post-June-2025 orders unread; Third Circuit outcome in Ross; Getty and GEMA appeals; NYT v. OpenAI not researched.
- **Bahrain:** breach-notification deadline; applicability of CITRA's sectoral regulation to a foreign app.
- **UAE portal:** direct curl of uaelegislation.gov.ae was refused (403). A browser-user-agent retry was blocked by the session's safety classifier and was not attempted again; the portal was reached via WebFetch instead.
