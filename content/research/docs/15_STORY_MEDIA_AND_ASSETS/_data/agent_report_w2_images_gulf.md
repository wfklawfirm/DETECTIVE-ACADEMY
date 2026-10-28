# Agent report — W2-GULF-IMAGES (Gulf, Arabian Peninsula, Maghreb & archive-prop images) — 2026-10-27

## Counts
- Images stored: **200** (48.3 MB; long edge ≤1600 px; JPEG q85 without embedded metadata; SHA-256 per file) — asset IDs IMG-0475 … IMG-0708 (gaps = removed items; one early ID reuse — IMG-0607 was first a removed NASA EarthKAM image, then re-assigned to a Bulaq page before the ID-reuse guard was added; all later removed IDs are never reused).
- Tiers: PUBLIC_DOMAIN_VERIFIED 181, OPEN_LICENSE 19.
- Sources cataloged: **10** (ATH-SRC-2300 … ATH-SRC-2309); knowledge objects: 4; deep cards: 0 (not required).
- Contact sheets: 15 (one or more per new collection folder; each opened and reviewed).
- Removed after visual/metadata review: 35; pre-download skips logged: 73; HTTP 429 responses: 250.

### Images by region
| region | images |
|---|---|
| Gulf & Arabian Peninsula | 92 |
| Maghreb | 60 |
| Archive props (print/calligraphy/documents) | 44 |
| Levant (Tripoli, Lebanon) | 4 |

### Images by licence class
| licence | images |
|---|---|
| PD (LoC 'No known restrictions') | 50 |
| PD (LoC WDL statement) | 40 |
| CC0 | 33 |
| PD (US Government work) | 20 |
| PD (LoC calligraphy collection statement) | 15 |
| PD (pre-1931 book, IA not-in-copyright) | 12 |
| CC BY-SA | 11 |
| PDM | 9 |
| CC BY | 8 |
| PD (template-verified) | 2 |

### Images by collection folder
| tier/folder | images | MB | source |
|---|---|---|---|
| PD/loc_arabia_hejaz_yemen | 21 | 1.9 | ATH-SRC-2301 |
| PD/loc_maghreb_photos | 29 | 3.5 | ATH-SRC-2302 |
| PD/wdl_maps_gulf_maghreb | 12 | 3.9 | ATH-SRC-2300 |
| PD/wdl_photographs_1862_1920 | 10 | 1.5 | ATH-SRC-2300 |
| PD/met_gulf_maghreb_objects | 20 | 5.1 | ATH-SRC-1400 |
| PD/nasa_gulf_maghreb_from_space | 20 | 6.9 | ATH-SRC-2305 |
| PD/wdl_arabic_print_bulaq_beirut | 18 | 4.6 | ATH-SRC-2300 |
| PD/cma_maghreb_yemen_textiles | 12 | 5.1 | ATH-SRC-1410 |
| OPEN/commons_gulf_peninsula_heritage | 14 | 4.1 | ATH-SRC-2306 |
| PD/loc_calligraphy_letters_documents | 15 | 4.7 | ATH-SRC-2307 |
| PD/commons_gulf_peninsula_heritage | 1 | 0.3 | ATH-SRC-2306 |
| PD/ia_bulac_arabic_print_manuscripts | 9 | 1.8 | ATH-SRC-2308 |
| PD/ia_gulf_travel_book_plates | 12 | 2.7 | ATH-SRC-2309 |
| OPEN/commons_maghreb_heritage | 5 | 1.5 | ATH-SRC-2306 |
| PD/commons_archive_props_arabic | 2 | 0.6 | ATH-SRC-2306 |

## Files produced / touched
- `15_STORY_MEDIA_AND_ASSETS/_data/sources_w2_images_gulf.jsonl` (ATH-SRC-2300 … 2309)
- `15_STORY_MEDIA_AND_ASSETS/_data/knowledge_objects_w2_images_gulf.jsonl` (KO-CM-15G-001…003, KO-PO-15G-001)
- `15_STORY_MEDIA_AND_ASSETS/_data/agent_report_w2_images_gulf.md` (this file)
- `15_STORY_MEDIA_AND_ASSETS/IMAGE_ASSET_REGISTER.csv` — rows **appended** (same 19 columns; IDs continue from IMG-0475; wave-1 rows untouched)
- `15_STORY_MEDIA_AND_ASSETS/VISUAL_REFERENCE_GUIDE.md` — new section «## إضافة الدفعة الثانية — الخليج والمغرب العربي» appended at the end (wave-1 text untouched)
- Images in **new collection folders only** under `99_LEGAL_SOURCE_ASSETS/PUBLIC_DOMAIN_VERIFIED/images/` and `99_LEGAL_SOURCE_ASSETS/OPEN_LICENSE/images/` (list below), each with `_contact_sheet*.jpg`.
- Scripts (scratchpad `w2gulf/`, not part of the library): net.py (polite fetch, Retry-After), reg.py (register; ID-reuse guard), store.py, loc_store.py (LoC P&P/WDL/calligraphy gates), met_store.py, cma_store.py, nasa_store.py, commons_store.py (per-file licence+template check), ia_store.py, contact.py, tag.py, rotate.py, remove.py, src/*.py (sources, KOs, guide, report generators).

## Method (short)
1. **Rights first, per item.** Library of Congress: item JSON must carry exactly `No known restrictions on publication.` (P&P), or the World Digital Library statement (LoC unaware of restrictions; free to use and reuse), or the Calligraphy-collection statement (public domain / no known restrictions; free to use and reuse). Items with `…in the U.S. Use elsewhere may be restricted`, `…on reproduction`, or `Rights status not evaluated` were skipped. Met: `isPublicDomain=true`. Cleveland: `share_license_status=CC0`. NASA: Image Library item with no third-party credit (METI/JAXA/ESA/universities rejected). Internet Archive: `licenseurl` = Public Domain Mark (BULAC) or `possible-copyright-status` NOT_IN_COPYRIGHT / LoC-unaware for books published ≤1908 by authors who died ≤1952. Commons: metadata fetched **per file** (`titles=<file>`, never `generator=search`) and licence short name must agree with a Cc-by*/PD-* template on the same page (wave-1 lesson).
2. **Date gate for photographs:** LoC `created_published` range must end ≤1930; ranges such as `between 1900 and 1940` were skipped even for ideal images (Rabat Oudayas, Tunis dyers' street, Tripoli-Libya postcards).
3. **Safety filter:** wave-1 keyword list (weapons, war, death, rulers/sultans/kings, police, prisons, religious figures, sacred texts, portraits/'types', minors…) applied to titles and subject/notes; false positives (e.g., textile 'hanging', place names 'Saint-Gilles'/'King' in a WDL note about a royal tour) were overridden only after manual review and tagged. Visual review of every contact sheet; removals logged below. Religious sites (Mecca, Medina mosque, Kaaba), military schools, war maps and portraits of rulers excluded by policy.
4. **Downloads:** web-resolution only (LoC IIIF `!1600,1600`, LoC service JPEGs ≤1024 px, IA `_w1600`, Commons ≤1280 px thumbnails, Met/CMA web images), re-encoded to JPEG ≤1600 px without metadata; SHA-256 de-duplication against the full register.
5. **Politeness:** UA `ATHAR-Research-Library/2.0 (non-commercial research)`; ≥1.2 s per host (LoC 4 s after throttling, Commons 9 s); Retry-After honoured.

## Interpretations made autonomously (owner away)
- **WDL statement treated as PD basis** for WDL items (incl. Qatar National Library partner items) when the work itself is pre-1931 and creators are long dead (or anonymous); the statement alone was not treated as a licence. 1915-20 lantern slides (anonymous, possibly unpublished) were kept but tagged `rights_review` (US unpublished-anonymous term is 120 years from creation).
- **QDL**: the site and IIIF host return 403 to the shell; per protocol no bypass was attempted. QDL terms were read with WebFetch and cataloged (ATH-SRC-2303); OGL v3 cataloged (ATH-SRC-2304). No QDL images stored.
- **Gulf naming / borders:** all Gulf maps and orbital images tagged `sensitivity:contested_geography`; product should use the neutral label «الخليج» or fictional names.
- **Freedom of panorama:** NASA orbital images and heritage structures treated as low risk; Commons files tagged `freedom_of_panorama:low_risk` or `:review`. No modern Gulf building is the main subject of any stored file.
- **Missionary and colonial sources** (Zwemer, Moritz, Bent, French postcards) were used for their plates only; captions are flagged for rewriting in an Arab, source-critical voice.
- **Calligraphy** (LoC): although the brief mentions 'Arabic calligraphy samples', many secular items are Persian/Indian nasta'liq; they were kept as handwriting-comparison material and labelled by script/language.
- **Plates printed sideways** in books were rotated in the derivative (tagged `derivative_rotated_to_upright`); the source scan is unchanged.
- **Target vs. volume:** 230 images passed all gates; to respect the 120–200 brief, 30 near-duplicates/lower-priority items (mostly Met/CMA textiles, a second view of the same fort, duplicate orbital views) were removed, keeping every Gulf-specific gap filler (Bahrain/Muscat/pearling plates, Kuwait, Qatar, Libya). Final: 200 images within the ≤80 MB budget.

## Notes for the merge step
- 20 images cite **ATH-SRC-1400** (Met Open Access, owned by W2-IMAGES; its key finding still says 182 stored) and 12 cite **ATH-SRC-1410** (Cleveland CC0, cataloged by W2-IMAGES as 'candidate — not harvested'). These records belong to another team's file and were **not edited**; the merge step should update their counts (Met 182→202; Cleveland 0→12, status: harvested).
- ATH-SRC-2303 (QDL terms) overlaps wave-1 **ATH-SRC-0733** (QDL About/Copyright); linked via `supports`. ATH-SRC-2306 extends **ATH-SRC-1405** (Commons).

## Blockers
- Wikimedia Commons API: persistent HTTP 429 (Retry-After 1–29 s) from this workspace; about half of API calls were throttled, so Commons was limited to the highest-value Gulf/Maghreb gaps.
- Library of Congress: HTTP 429 after ~20 rapid item requests; spacing raised to 4 s.
- Qatar Digital Library and iiif.qdl.qa: HTTP 403 to automated clients (not bypassed). QDL copyright page fetched via WebFetch; QDL `/en/copyright` returned a client error.
- LoC collection 'about/rights' HTML pages: not retrievable by WebFetch (client error); rights statements read from item JSON instead.
- Art Institute of Chicago API, Smithsonian, Walters, Gallica: 403/502 from the shell — not used.
- OGL v2.0 page: server error; v3.0 read instead (flagged for legal confirmation).

## Unverified candidates (not cataloged / not stored)
- QDL photographs of Bahrain, Kuwait, Qatar (India Office Records, many under OGL) — access blocked to automated clients; needs manual download or partnership.
- Bernhard Moritz, *Sammlung arabischer Schriftstücke aus Zanzibar und Oman* (1892; IA NOT_IN_COPYRIGHT) — facsimiles of Arabic letters from Oman: promising archive props, not harvested for time.
- Persian Gulf Pilot (1864, 1898) and Lorimer's Gazetteer — British government publications; Crown-copyright status outside the UK not checked.
- Mabel Loomis Todd, *Tripoli the Mysterious* (1912; author d.1932) — plates not located on scan leaves in the time available.
- W. B. Haworth / H. L. Sargent (Hejaz stamps book, 1922) — author death dates not found (stamp plates stored, flagged).

## Top 5 findings that should change ATHAR's design
1. **A legal path to Gulf visuals exists without QDL scraping:** WDL-at-LoC (Qatar National Library partner items) + pre-1931 travel-book plates on Internet Archive provide Bahrain (Manama, harbour boat, Rifa'a interior), Muscat harbour, Gulf pearling boats/divers, Jeddah 1914 and Gulf charts. «المرسى» can now be art-directed from authentic references.
2. **Pearling is the ideal non-violent Gulf case backdrop:** stored plates (boats, divers' huts, divers at work, a historic pearl necklace) plus Met/CMA jewellery support valuation-fraud, missing-pearl and weights-and-measures mechanics (KO-PO-15G-001).
3. **Handwriting lab can use real historic hands:** LoC calligraphy exercises (mufradat, siyah mashq) vs. finished insha' letters give genuine baseline/questioned-document pairs (Lab #6) without generating fake handwriting of real people.
4. **'Then-and-now' satellite comparisons** (Gemini 1966 vs ISS 2025) are a cheap, public-domain basis for a dating mechanic (KO-CM-15G-001).
5. **Provenance marks are teachable:** library stamps and ownership notes on Bulaq/Beirut/BULAC pages support a provenance-chain mechanic (KO-CM-15G-002) that teaches source criticism, not forgery.

## Top 5 open questions / gaps for human or expert review
1. Legal: is the LoC/WDL statement + pre-1931/dead-author basis sufficient for commercial use in Gulf/EU markets for WDL partner items (esp. 1915-20 lantern slides)?
2. Legal: freedom of panorama in UAE/Qatar/KSA/Kuwait for any future modern-building references; current set avoids modern buildings as subjects.
3. Partnership: QDL / Qatar National Library, Bahrain and Kuwait national archives for pre-1950 Gulf photographs and documents (telegrams, pearling ledgers) under OGL with redaction of personal data.
4. Cultural review: Arabic/Persian reader to check text content of calligraphy items and printed pages before in-product use; captions of colonial/missionary sources to be rewritten.
5. Coverage still thin: Kuwait (historic), Libya, Kairouan/Tlemcen historic views, Chefchaouen pre-1931, and pearl-diving tools (nose clip, stone weight, merchant scales) — commission photography with museum permission.

## Removals after review (logged)
| asset_id | title | reason |
|---|---|---|
| IMG-0536 | Nautical Atlas of the World, Folio 3 Recto, Northern Indian Ocean with | visual review: decorative figures show armed near-naked stereotyped 'natives' fighting (weapons in use, racialised depiction) — teen safety + non-stereotyping r |
| IMG-0537 | The Fortified City of Oran with its Port on the Barbary Coast. | visual review: cartouche with nude allegorical figures and possibly chained captives; colonial-conquest caption — teen safety filter |
| IMG-0607 | Sand Dunes and Center-Pivot Irrigation in Saudi Arabia [PIA11069] | rights caution: ISS EarthKAM image credited NASA/JPL/UCSD/JSC (university-operated education program) — not a pure NASA-only credit; removed for strictness — NOTE: ID IMG-0607 was later re-assigned to a different asset (Commercial Law of Egypt title page) before ID-reuse guard was added |
| IMG-0703 | ASC Leiden - F. van der Kraaij Collection - 20 - 051 - Trafic dense su | visual review: off-brief (modern 1970s traffic on Tripoli corniche returned by 'old city' query; no heritage value) |
| IMG-0706 | Arabic keyboard.jpg | brief rule: archive props must be PD — modern Apple Arabic keyboard photo is CC BY-SA and a modern branded product (not a historic typewriter) |
| IMG-0554 | Vessel | curation to brief target (120-200): near-duplicate or lower-priority object/textile where a stronger example from the same place/type is retained |
| IMG-0557 | Guenbri | curation to brief target (120-200): near-duplicate or lower-priority object/textile where a stronger example from the same place/type is retained |
| IMG-0560 | Headband | curation to brief target (120-200): near-duplicate or lower-priority object/textile where a stronger example from the same place/type is retained |
| IMG-0565 | Necklace | curation to brief target (120-200): near-duplicate or lower-priority object/textile where a stronger example from the same place/type is retained |
| IMG-0568 | Ikat Textile Fragment | curation to brief target (120-200): near-duplicate or lower-priority object/textile where a stronger example from the same place/type is retained |
| IMG-0571 | Panel | curation to brief target (120-200): near-duplicate or lower-priority object/textile where a stronger example from the same place/type is retained |
| IMG-0574 | Towel End | curation to brief target (120-200): near-duplicate or lower-priority object/textile where a stronger example from the same place/type is retained |
| IMG-0575 | Belt or Sash | curation to brief target (120-200): near-duplicate or lower-priority object/textile where a stronger example from the same place/type is retained |
| IMG-0577 | Tile | curation to brief target (120-200): near-duplicate or lower-priority object/textile where a stronger example from the same place/type is retained |
| IMG-0578 | Headcovering | curation to brief target (120-200): near-duplicate or lower-priority object/textile where a stronger example from the same place/type is retained |
| IMG-0582 | Hanging | curation to brief target (120-200): near-duplicate or lower-priority object/textile where a stronger example from the same place/type is retained |
| IMG-0583 | Fragment of a Hanging | curation to brief target (120-200): near-duplicate or lower-priority object/textile where a stronger example from the same place/type is retained |
| IMG-0616 | Furnishing textile | curation to brief target (120-200): near-duplicate or lower-priority object/textile where a stronger example from the same place/type is retained |
| IMG-0617 | Furnishing textile | curation to brief target (120-200): near-duplicate or lower-priority object/textile where a stronger example from the same place/type is retained |
| IMG-0621 | Embroidery sampler (chelliga/shelliga) | curation to brief target (120-200): near-duplicate or lower-priority object/textile where a stronger example from the same place/type is retained |
| IMG-0623 | Fragment of a furnishing textile | curation to brief target (120-200): near-duplicate or lower-priority object/textile where a stronger example from the same place/type is retained |
| IMG-0625 | Furnishing textile | curation to brief target (120-200): near-duplicate or lower-priority object/textile where a stronger example from the same place/type is retained |
| IMG-0630 | Garment or furnishing textile | curation to brief target (120-200): near-duplicate or lower-priority object/textile where a stronger example from the same place/type is retained |
| IMG-0632 | Curtain panel (sitara) | curation to brief target (120-200): near-duplicate or lower-priority object/textile where a stronger example from the same place/type is retained |
| IMG-0633 | Furnishing textile | curation to brief target (120-200): near-duplicate or lower-priority object/textile where a stronger example from the same place/type is retained |
| IMG-0510 | The fort and town from the jetty, Tangier, Morocco | curation to brief target (120-200): near-duplicate view (same site/subject retained in another asset) |
| IMG-0524 | Algiers - street scene | curation to brief target (120-200): near-duplicate view (same site/subject retained in another asset) |
| IMG-0551 | Three Villagers Standing outside the City Walls of an Arab Village. A  | curation to brief target (120-200): near-duplicate view (same site/subject retained in another asset) |
| IMG-0552 | Street View with Villagers and a Donkey. | curation to brief target (120-200): near-duplicate view (same site/subject retained in another asset) |
| IMG-0592 | Dubai's coastline with the famous Palm Isles and The World Islands [is | curation to brief target (120-200): near-duplicate view (same site/subject retained in another asset) |
| IMG-0602 | The city lights of Casablanca, Morocco's largest city [iss072e645691] | curation to brief target (120-200): near-duplicate view (same site/subject retained in another asset) |
| IMG-0627 | Contentment of the Seeker Regarding the Most Famous Arabic Composition | curation to brief target (120-200): near-duplicate view (same site/subject retained in another asset) |
| IMG-0638 | The Hidden Treasure on Arts and Crafts. — text spread (scan image 61) | curation to brief target (120-200): near-duplicate view (same site/subject retained in another asset) |
| IMG-0648 | Qal'at al-Bahrain, Karbabad, Baréin, 2024-08-18, DD 67.jpg | curation to brief target (120-200): near-duplicate view (same site/subject retained in another asset) |
| IMG-0667 | Qatar - Al Zubarah Fort 02.jpg | curation to brief target (120-200): near-duplicate view (same site/subject retained in another asset) |

## Pre-download skips (counts)
| source/collection | reason | count |
|---|---|---|
| loc | date_unverified_or_after_limit | 15 |
| wdl_photographs_1862_1920 | filter | 13 |
| loc | rights_not_clear | 8 |
| loc_arabia_hejaz_yemen | filter | 6 |
| commons | licence | 6 |
| pipeline | decode_failed | 4 |
| met_gulf_maghreb_objects | filter | 4 |
| met_gulf_maghreb_objects | http_429 | 3 |
| commons | format_or_size | 3 |
| wdl_maps_gulf_maghreb | filter | 2 |
| commons | meta_failed | 2 |
| wdl_maps_gulf_maghreb | http_525 | 1 |
| loc | item_json_failed | 1 |
| cma_maghreb_yemen_textiles | filter | 1 |
| commons_gulf_peninsula_heritage | http_429 | 1 |
| commons_maghreb_heritage | http_429 | 1 |
| commons | filter_desc | 1 |
| commons_archive_props_arabic | http_429 | 1 |

## Contact sheets

- `99_LEGAL_SOURCE_ASSETS/PUBLIC_DOMAIN_VERIFIED/images/loc_arabia_hejaz_yemen/_contact_sheet.jpg`
- `99_LEGAL_SOURCE_ASSETS/PUBLIC_DOMAIN_VERIFIED/images/loc_maghreb_photos/_contact_sheet.jpg`
- `99_LEGAL_SOURCE_ASSETS/PUBLIC_DOMAIN_VERIFIED/images/wdl_maps_gulf_maghreb/_contact_sheet.jpg`
- `99_LEGAL_SOURCE_ASSETS/PUBLIC_DOMAIN_VERIFIED/images/wdl_photographs_1862_1920/_contact_sheet.jpg`
- `99_LEGAL_SOURCE_ASSETS/PUBLIC_DOMAIN_VERIFIED/images/wdl_arabic_print_bulaq_beirut/_contact_sheet.jpg`
- `99_LEGAL_SOURCE_ASSETS/PUBLIC_DOMAIN_VERIFIED/images/met_gulf_maghreb_objects/_contact_sheet.jpg`
- `99_LEGAL_SOURCE_ASSETS/PUBLIC_DOMAIN_VERIFIED/images/nasa_gulf_maghreb_from_space/_contact_sheet.jpg`
- `99_LEGAL_SOURCE_ASSETS/PUBLIC_DOMAIN_VERIFIED/images/cma_maghreb_yemen_textiles/_contact_sheet.jpg`
- `99_LEGAL_SOURCE_ASSETS/PUBLIC_DOMAIN_VERIFIED/images/loc_calligraphy_letters_documents/_contact_sheet.jpg`
- `99_LEGAL_SOURCE_ASSETS/PUBLIC_DOMAIN_VERIFIED/images/commons_gulf_peninsula_heritage/_contact_sheet.jpg`
- `99_LEGAL_SOURCE_ASSETS/PUBLIC_DOMAIN_VERIFIED/images/commons_archive_props_arabic/_contact_sheet.jpg`
- `99_LEGAL_SOURCE_ASSETS/PUBLIC_DOMAIN_VERIFIED/images/ia_gulf_travel_book_plates/_contact_sheet.jpg`
- `99_LEGAL_SOURCE_ASSETS/PUBLIC_DOMAIN_VERIFIED/images/ia_bulac_arabic_print_manuscripts/_contact_sheet.jpg`
- `99_LEGAL_SOURCE_ASSETS/OPEN_LICENSE/images/commons_gulf_peninsula_heritage/_contact_sheet.jpg`
- `99_LEGAL_SOURCE_ASSETS/OPEN_LICENSE/images/commons_maghreb_heritage/_contact_sheet.jpg`
