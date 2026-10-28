# Agent report — W2-IMAGES (image & visual assets) — 2026-10-27

## Counts
- Images stored: **400** (102.6 MB; plus 32 contact sheets, 3.9 MB) — PUBLIC_DOMAIN_VERIFIED: 336, OPEN_LICENSE: 64. Long edge ≤1600 px; re-encoded JPEG q85 without embedded metadata; SHA-256 per file in the register.
- Sources cataloged: **14** (ATH-SRC-1400 … ATH-SRC-1413); deep cards: 0 (not required by brief); knowledge objects: 3 (KO-CM-15-001/002, KO-PO-15-001).
- Link-only copyrighted visual references: 14 (COPYRIGHTED_VISUAL_REFERENCES.csv).
- Removed after review (safety filter, off-topic, licence re-check, curation to the 250–400 target): 74 images (+2 ID renumberings); pre-download skips: 359.

### Images by collection
| folder | tier | images |
|---|---|---|
| met_islamic_art | PD | 121 |
| loc_matson_american_colony | PD | 78 |
| met_19c_photographs | PD | 33 |
| loc_photochrom | PD | 23 |
| met_science_instruments | PD | 22 |
| wellcome_labs_instruments | OPEN/PD | 17 |
| commons_levant_heritage | OPEN/PD | 14 |
| commons_iraq_egypt_maghreb | OPEN | 14 |
| wellcome_fingerprints_galton_faulds | OPEN/PD | 10 |
| commons_gulf_heritage | OPEN/PD | 10 |
| ia_fbi_science_of_fingerprints | PD | 9 |
| wellcome_bertillon_identification | OPEN/PD | 8 |
| wellcome_arabic_science_manuscripts | OPEN/PD | 8 |
| wellcome_documents_ciphers | PD | 7 |
| met_prints_drawings | PD | 6 |
| ia_henry_classification_1900 | PD | 5 |
| loc_abdul_hamid_ii | PD | 5 |
| commons_maps | PD | 4 |
| commons_science_manuscripts | OPEN/PD | 2 |
| commons_documents_archive | OPEN/PD | 2 |
| commons_forensic_lab_visuals | OPEN | 2 |

### Images by exact licence string (register `license` field)
| licence | images |
|---|---|
| Met Open Access — isPublicDomain: true (CC0 1.0 Universal) | 182 |
| No known restrictions on publication. | 106 |
| Public Domain Mark | 26 |
| Attribution 4.0 International (CC BY 4.0) | 24 |
| CC BY-SA 4.0 | 18 |
| CC BY-SA 3.0 | 12 |
| Public domain — work of the U.S. Government (17 U.S.C. §105); IA metadata: no licence stated | 9 |
| Public domain | 8 |
| CC BY 2.0 | 6 |
| Public domain (IA possible-copyright-status: NOT_IN_COPYRIGHT) | 5 |
| CC BY 3.0 | 2 |
| CC BY-SA 2.0 | 1 |
| CC BY 4.0 | 1 |

## Files produced
- `15_STORY_MEDIA_AND_ASSETS/IMAGE_ASSET_REGISTER.csv`
- `15_STORY_MEDIA_AND_ASSETS/VISUAL_REFERENCE_GUIDE.md`
- `15_STORY_MEDIA_AND_ASSETS/COPYRIGHTED_VISUAL_REFERENCES.csv`
- `15_STORY_MEDIA_AND_ASSETS/_data/sources_w2_images.jsonl`
- `15_STORY_MEDIA_AND_ASSETS/_data/knowledge_objects_w2_images.jsonl`
- `15_STORY_MEDIA_AND_ASSETS/_data/agent_report_w2_images.md`
- Images: `99_LEGAL_SOURCE_ASSETS/PUBLIC_DOMAIN_VERIFIED/images/<collection>/IMG-NNNN_*.jpg` and `99_LEGAL_SOURCE_ASSETS/OPEN_LICENSE/images/<collection>/IMG-NNNN_*.jpg`; one `_contact_sheet*.jpg` per collection folder (32 sheets).
- Note: a collection whose items carry different licences is split across both tiers under the same folder name (e.g., `wellcome_*`: PDM items in PUBLIC_DOMAIN_VERIFIED, CC BY items in OPEN_LICENSE).
- Scripts (scratchpad, not part of library): net.py, reg.py, met_harvest.py, loc_harvest.py, wellcome_*.py, commons_harvest.py, ia_store.py, contact.py, remove.py.
- Overlap note: ATH-SRC-1406 (CC legal codes + PDM + attribution practice) overlaps W2-LEGAL's ATH-SRC-1839 (CC BY-SA 4.0 legal code) and wave-1 ATH-SRC-1025 (CC BY-NC 4.0); linked via `supports` for the merge step.

## Method (short)
1. Rights first: verified each collection's rights page (Met Open Access policy; LoC P&P rights CSV behind guides.loc.gov; Wellcome copyright-images page; CC legal codes/TASL; 17 U.S.C. §105 on LII) and recorded each as an ATH-SRC record.
2. Item-level gate: Met `isPublicDomain=true`; LoC item `rights_advisory` must contain 'No known restrictions'; Wellcome per-image licence ∈ {pdm, cc-0, cc-by} (NC/ND excluded); Commons `LicenseShortName` ∈ {Public domain, CC0, PDM, CC BY x, CC BY-SA x}, no `Restrictions`, and a PD-* template required for 'Public domain'; Internet Archive only US-government works or NOT_IN_COPYRIGHT pre-1931 books by authors dead >70 years.
3. Photographs: Met photos limited to works made ≤1925 and photographers who died ≤1955 when known; Matson items limited to dated ≤1936 or ranges ending ≤1946 (corporate/anonymous studio work), post-1930 items tagged `rights_review:post1930`.
4. Safety: word-boundary keyword filter (EN/FR; weapons, war, death, gore, nudity, alcohol, religious figures/sacred texts, portraits/'types', minors, police/criminals, rulers) before download; then contact-sheet visual review of every collection (sheets opened and inspected) with removals logged below.
5. Politeness: UA 'ATHAR-Research-Library/2.0 (non-commercial research)'; ≥1.2 s per host (Commons API 4–7 s); Retry-After honoured. 1925 requests logged, 118 HTTP 429 responses (almost all from Wikimedia).

## Interpretations made autonomously (owner away)
- 'One source record per collection/institution/licence page and per key image set' → 14 records: 4 institutions/collections (Met, LoC×3), Wellcome, Commons, CC licences, 2 key books (FBI 1957, Henry 1900), LoC rights dataset, 1 candidate (Cleveland), 1 cataloged-not-stored dataset (NIST SD 302), 2 link-only game references needed by COPYRIGHTED_VISUAL_REFERENCES.csv.
- Matson collection treated as PD/no-known-restrictions worldwide for items made by 1946, because LoC records a 2003 dedication of rights to the American public and the works are corporate/anonymous studio photographs (70/50-year anonymous terms). Residual risk flagged per item.
- US-government works (FBI manual) stored under PUBLIC_DOMAIN_VERIFIED with an explicit 'outside US not formally established' caveat.
- Religious-sensitivity rule applied conservatively: no Qur'an manuscripts, mosque lamps, prophets, saints/angels, divine-hand iconography; mosques appear only as parts of city views; manuscripts that open with the basmala kept but flagged in the guide.
- Bertillon: stored instruction plates, measurement drawings, ear/iris charts and book pages only; the album's mugshot plates of real arrested persons were excluded (dignity + teen-safety), although openly licensed.
- Off-topic items returned by broad API queries (European furniture, Moscow/Rome/Delhi views, North-American street photochroms) removed to keep the library on-brief.

## Removals after visual review (logged)
| asset_id | title | reason |
|---|---|---|
| IMG-0091 | "Figure for Use at Drinking Parties", Folio from a Book of the Knowled | cultural-sensitivity: content/title references wine or drinking parties (AGE_APPROPRIATE_CONTENT_POLICY §4) |
| IMG-0100 | "Men Treading Grapes", Folio from a Materia Medica of Dioscorides | cultural-sensitivity: content/title references wine or drinking parties (AGE_APPROPRIATE_CONTENT_POLICY §4) |
| IMG-0006 | Button or Bead | visual review: off-topic for ATHAR settings/props (non-Arab European/Indian subject or furniture/dress item) |
| IMG-0016 | Hair Ornament, One of a Pair | visual review: off-topic for ATHAR settings/props (non-Arab European/Indian subject or furniture/dress item) |
| IMG-0043 | Vest | visual review: off-topic for ATHAR settings/props (non-Arab European/Indian subject or furniture/dress item) |
| IMG-0187 | Temple of Wingless Victory, Lately Restored | visual review: off-topic for ATHAR settings/props (non-Arab European/Indian subject or furniture/dress item) |
| IMG-0188 | Moscow, Domes of Churches in the Kremlin | visual review: off-topic for ATHAR settings/props (non-Arab European/Indian subject or furniture/dress item) |
| IMG-0189 | [Basilica of Maxentius and Constantine, Rome] | visual review: off-topic for ATHAR settings/props (non-Arab European/Indian subject or furniture/dress item) |
| IMG-0196 | [Mosque at Sultaniye, [same as 46] ] | visual review: off-topic for ATHAR settings/props (non-Arab European/Indian subject or furniture/dress item) |
| IMG-0197 | [Jama Masjid Mosque, Delhi] | visual review: off-topic for ATHAR settings/props (non-Arab European/Indian subject or furniture/dress item) |
| IMG-0198 | [Simla Bazaar] | visual review: off-topic for ATHAR settings/props (non-Arab European/Indian subject or furniture/dress item) |
| IMG-0201 | Fountain, Savanah, Georgia | visual review: off-topic for ATHAR settings/props (non-Arab European/Indian subject or furniture/dress item) |
| IMG-0202 | [Fountain at Versailles] | visual review: off-topic for ATHAR settings/props (non-Arab European/Indian subject or furniture/dress item) |
| IMG-0203 | Nîmes, Fontaine | visual review: off-topic for ATHAR settings/props (non-Arab European/Indian subject or furniture/dress item) |
| IMG-0224 | A Great Green Bush Cricket (Tettigorica viridissima Linneaeus), A Clio | visual review: off-topic for ATHAR settings/props (non-Arab European/Indian subject or furniture/dress item) |
| IMG-0232 | Irish cars (Study of two carts in a landscape) | visual review: off-topic for ATHAR settings/props (non-Arab European/Indian subject or furniture/dress item) |
| IMG-0236 | Piece | visual review: off-topic for ATHAR settings/props (non-Arab European/Indian subject or furniture/dress item) |
| IMG-0237 | Shawl | visual review: off-topic for ATHAR settings/props (non-Arab European/Indian subject or furniture/dress item) |
| IMG-0238 | Nécessaire | visual review: off-topic for ATHAR settings/props (non-Arab European/Indian subject or furniture/dress item) |
| IMG-0239 | Nécessaire | visual review: off-topic for ATHAR settings/props (non-Arab European/Indian subject or furniture/dress item) |
| IMG-0253 | Cabinet | visual review: off-topic for ATHAR settings/props (non-Arab European/Indian subject or furniture/dress item) |
| IMG-0257 | The Louis XV Room | visual review: off-topic for ATHAR settings/props (non-Arab European/Indian subject or furniture/dress item) |
| IMG-0260 | Table | visual review: off-topic for ATHAR settings/props (non-Arab European/Indian subject or furniture/dress item) |
| IMG-0261 | Side table (one of a pair) | visual review: off-topic for ATHAR settings/props (non-Arab European/Indian subject or furniture/dress item) |
| IMG-0262 | Chocolate pot | visual review: off-topic for ATHAR settings/props (non-Arab European/Indian subject or furniture/dress item) |
| IMG-0133 | Mirror | visual review: safety/cultural filter — religious-figure imagery (saints/monks) or astrological figurative mirror (policy §4/§6; skip ambigu |
| IMG-0212 | S. Jean Damascène (St. John of Damascus), May 6th, from "Les Images De | visual review: safety/cultural filter — religious-figure imagery (saints/monks) or astrological figurative mirror (policy §4/§6; skip ambigu |
| IMG-0214 | Two Monks Looking up at a Dragon in a Tower | visual review: safety/cultural filter — religious-figure imagery (saints/monks) or astrological figurative mirror (policy §4/§6; skip ambigu |
| IMG-0215 | S. Damase, pape (St. Damasus, Pope), December 11th, from "Les Images D | visual review: safety/cultural filter — religious-figure imagery (saints/monks) or astrological figurative mirror (policy §4/§6; skip ambigu |
| IMG-0174 | Femme turque en toilette de ville | visual review: safety/cultural filter — satirical caricature / orientalist 'type' portrait (non-stereotyping rule §5) |
| IMG-0209 | Theologie à la Turque and a Peep of the Coptic Mayor at Cairo, precede | visual review: safety/cultural filter — satirical caricature / orientalist 'type' portrait (non-stereotyping rule §5) |
| IMG-0229 | The World, Cage of Fools | visual review: safety/cultural filter — satirical caricature / orientalist 'type' portrait (non-stereotyping rule §5) |
| IMG-0179 | Jérusalem, Sarcophage judaïque | visual review: safety filter — armed guards / animal violence (bullfight) / funerary object |
| IMG-0208 | Arnaut Guardhouse in Cairo | visual review: safety filter — armed guards / animal violence (bullfight) / funerary object |
| IMG-0233 | The agility and audacity of Juanito Apiñani in [the ring] at Madrid, p | visual review: safety filter — armed guards / animal violence (bullfight) / funerary object |
| IMG-0160 | Saîs coureurs au Caire | visual review: orientalist 'type' photograph of costumed servants (non-stereotyping rule §5) |
| IMG-0323 | Matson photographing in Petra, 1934 | visual review: portrait framing a private person by religious/ethnic identity, or identifiable photographer portrait — off-topic and sensiti |
| IMG-0335 | [Ashkenazim [i.e., Ashkenazi] Jew in his home (scribe) | visual review: portrait framing a private person by religious/ethnic identity, or identifiable photographer portrait — off-topic and sensiti |
| IMG-0337 | [Askenazim [i.e., Ashkenazi] Jew in his home (scribe)] | visual review: portrait framing a private person by religious/ethnic identity, or identifiable photographer portrait — off-topic and sensiti |
| IMG-0340 | MSS [i.e., manuscript] | visual review: religious-figure iconography in manuscript / religious pilgrimage site (policy §6; skip ambiguous) |
| IMG-0345 | Ancient MSS [i.e., manuscript] | visual review: religious-figure iconography in manuscript / religious pilgrimage site (policy §6; skip ambiguous) |
| IMG-0354 | Jacob's Well | visual review: religious-figure iconography in manuscript / religious pilgrimage site (policy §6; skip ambiguous) |
| IMG-0221 | Frontispiece: mythological figures weigh astronomical theories, from " | visual review: religious/devotional iconography (divine hand, cherubs, prayer scene) or Death automaton on cathedral clock — ambiguous for 1 |
| IMG-0222 | Astronomical Clock in the Cathedral in Strasbourg | visual review: religious/devotional iconography (divine hand, cherubs, prayer scene) or Death automaton on cathedral clock — ambiguous for 1 |
| IMG-0226 | The Alchemist's Laboratory from Heinrich Khunrath, Amphiteatrum sapien | visual review: religious/devotional iconography (divine hand, cherubs, prayer scene) or Death automaton on cathedral clock — ambiguous for 1 |
| IMG-0220 | Trade Card for G.F. Cruchley, Map Seller and Publisher | visual review: off-topic (19th-c. British trade card) |
| IMG-0378 | [Warships, Algiers, Algeria] | visual review: military subject (warships) — weapons/military excluded by teen safety filter |
| IMG-0379 | [Warship, Algiers, Algeria] | visual review: military subject (warships) — weapons/military excluded by teen safety filter |
| IMG-0377 | [Cathedral, Algiers, Algeria] | visual review: off-topic (North American street views / colonial-era cathedral with contested religious history) |
| IMG-0387 | Wisconsin Street, Milwaukee | visual review: off-topic (North American street views / colonial-era cathedral with contested religious history) |
| IMG-0388 | Champlain Street, Quebec | visual review: off-topic (North American street views / colonial-era cathedral with contested religious history) |
| IMG-0393 | [Students, high school, Damascus] | visual review: posed portrait of identifiable minors (schoolboys) — skip ambiguous |
| IMG-0446 | View for Minarets of Bab Zuwayla, Cairo 04.jpg | licence re-check: true licence 'Public domain' not accepted (no PD template or restricted) |
| IMG-0463 | Houghton GC5 R4947 572i - Opticæ thesavrvs.jpg | visual review: safety filter — frontispiece depicts burning mirrors setting warships on fire (weapon in use) and a nude figure |
| IMG-0467 | Stamp of Brazil - 1970 - Colnect 213991 - Inauguration of the historic | visual review: off-topic search hits (20th-c. Brazil/Peru stamps with a military portrait; 1973 US Navy ship document) |
| IMG-0468 | Stamp of Peru - 1970 - Colnect 387008 - Historical Peru - Tourist Attr | visual review: off-topic search hits (20th-c. Brazil/Peru stamps with a military portrait; 1973 US Navy ship document) |
| IMG-0473 | Ranger (CVA-61) - March 1973 - DPLA - 09361650553c3c2896be33e4213e2404 | visual review: off-topic search hits (20th-c. Brazil/Peru stamps with a military portrait; 1973 US Navy ship document) |
| IMG-0469 | 1915 Ottoman Documents-4.png | metadata review: document concerns 1915 deportations (Armenian Genocide) — real atrocity / contested political history, banned by content po |
| IMG-0102 | Identification anthropométrique : instructions signalétiques / par Alp | curation to brief target (≤400): near-duplicate of a retained image (same view/print/spread) |
| IMG-0155 | Le Kaire, Mosquée Nâcéryeh | curation to brief target (≤400): near-duplicate of a retained image (same view/print/spread) |
| IMG-0278 | Beirut, etc. General view of Beirut | curation to brief target (≤400): near-duplicate of a retained image (same view/print/spread) |
| IMG-0298 | Hama (Hamath). Double water-wheel | curation to brief target (≤400): near-duplicate of a retained image (same view/print/spread) |
| IMG-0318 | Jaffa | curation to brief target (≤400): near-duplicate of a retained image (same view/print/spread) |
| IMG-0363 | [Egypt. Cairo. On the Nile shore near Boulac, with Dahableh making sai | curation to brief target (≤400): near-duplicate of a retained image (same view/print/spread) |
| IMG-0437 | Mustansiriya Madrasah5.jpg | curation to brief target (≤400): near-duplicate of a retained image (same view/print/spread) |
| IMG-0449 | Al Attarine Madrasa Fez el Bali Fez Morocco - panoramio (2).jpg | curation to brief target (≤400): near-duplicate of a retained image (same view/print/spread) |
| IMG-0175 | Baalbek | curation to brief target (≤400): low legibility (very dark daguerreotype) or uncertain identification ('Tripoli?') |
| IMG-0205 | Monsieur Itier's Cange Under Sail on the Nile | curation to brief target (≤400): low legibility (very dark daguerreotype) or uncertain identification ('Tripoli?') |
| IMG-0286 | Tripoli? | curation to brief target (≤400): low legibility (very dark daguerreotype) or uncertain identification ('Tripoli?') |
| IMG-0180 | Jérusalem, Côté Est de Jérusalem | curation to brief target (≤400): off-brief subject (map of Greece; insect studies) or low-value contested-geography landscape |
| IMG-0181 | Jérusalem, Côté Sud de Jérusalem | curation to brief target (≤400): off-brief subject (map of Greece; insect studies) or low-value contested-geography landscape |
| IMG-0182 | Jérusalem, Côté Nord de Jérusalem | curation to brief target (≤400): off-brief subject (map of Greece; insect studies) or low-value contested-geography landscape |
| IMG-0219 | Map of Greece, from "Speculum Romanae Magnificentiae" | curation to brief target (≤400): off-brief subject (map of Greece; insect studies) or low-value contested-geography landscape |
| IMG-0225 | Studies of a Blue Beetle and Insects | curation to brief target (≤400): off-brief subject (map of Greece; insect studies) or low-value contested-geography landscape |

## Pre-download skips (counts)
| source | reason | count |
|---|---|---|
| commons | filter | 155 |
| loc | matson_date_gt_1936_or_unknown | 59 |
| met | filter | 53 |
| loc | filter | 38 |
| commons | pd_without_template | 20 |
| commons | licence | 16 |
| commons | http_429 | 5 |
| loc | rights_not_clear | 5 |
| pipeline | decode_failed | 3 |
| pipeline | duplicate_hash | 2 |
| commons | http_0 | 2 |
| met | http_429 | 1 |

## Data-quality incident (found and fixed)
- The Commons harvester's metadata accessor was a late-bound closure, so for some files the licence/author/date of the *last* search hit was written to the register; separately, extmetadata from generator=search sometimes disagreed with the file-page licence template. Fix: every Commons row was re-fetched individually (imageinfo + templates with continuation), licence/creator/date/attribution rewritten, tier folder corrected (2 files moved to PUBLIC_DOMAIN_VERIFIED: PD-Lebanon engraving, PD-self photo; 3 moved to OPEN_LICENSE), 1 file removed (claimed 'Public domain' without a PD template). Harvester patched (bound closure + template-consistency gate) before the final Commons batches. Non-Commons sources were unaffected (per-object metadata).
- Second-pass sensitivity scan on full Commons descriptions/categories and LoC notes (not just titles): removed a 1915 Ottoman telegram concerning Armenian deportations (title alone looked like a neutral 'Ottoman document'); tagged 35 Jerusalem/Jaffa/Galilee items `sensitivity:contested_geography` (catalogue labels such as 'Holy Land (i.e. Israel)'); remaining hits were benign (minarets in city views, a Christian family courtyard, mis-captioned 'tomb').

## Blockers
- Wikimedia Commons API and upload.wikimedia.org repeatedly returned HTTP 429 (Retry-After 14–60 s) even at 4–7 s spacing; worked around with longer spacing and standard thumbnail sizes (960/500 px) from thumb.wikimedia.org, which made Commons the slowest source and limited its share.
- Commons policy pages (Licensing, Reusing content) not retrievable via WebFetch (url_not_found); Licensing intro read via the MediaWiki parse API.
- LoC collection 'rights-and-access' HTML pages blocked by a JS challenge (403); rights statements taken from the LoC P&P rights CSV (`guides.loc.gov/ld.php?content_id=76336558`) and item JSON `rights_advisory`.
- Met `/public/collection/v1/search` retired 2026-10-01 (HTTP 410); migrated to `/v1.1/search`.
- Qatar Digital Library site returned 403 to automated requests — no QDL images stored (rights are item-specific anyway, ATH-SRC-0733).
- Smithsonian Open Access and Gallica terms pages not retrievable by WebFetch (client_error) — not used.
- 3 LoC downloads were truncated (decode failed) and skipped.

## Unverified candidates (not cataloged)
- Smithsonian Open Access (CC0) — terms page could not be fetched this session.
- Gallica/BnF images (e.g., al-Idrisi BnF Arabe 2221 is on Commons as PD) — Gallica reuse terms (commercial reuse fee) not fetched; not used directly.
- Netflix official title pages for Paranormal/Whispers — only Wikipedia/catalog entries used (ATH-SRC-0737/0739).
- House of Hikmah gameplay/visual claims beyond Steam basics and Arab News report.

## Top 5 findings that should change ATHAR's design
1. A zero-licence-cost historic visual base for the Levant/Egypt/Maghreb exists and is now stored (Met CC0 + LoC Matson/Photochrom), enough for the 'old paper / brass' half of the identity — but almost all of it is seen through European/American lenses; captions must be rewritten in an Arab, source-critical voice.
2. The Gulf is the visual gap: no usable historic open images for Kuwait/Bahrain/Qatar/UAE in LoC; Commons gives modern CC BY/BY-SA photos with share-alike and possible freedom-of-panorama limits. 'al-Marsa' needs original art or an archive partnership (QDL, national archives).
3. Attribution can be a learning mechanic: a per-prop 'source card' generated from the register teaches provenance (KO-CM-15-001) and simultaneously satisfies CC BY/LoC credit requests.
4. Historic forensic imagery is usable for explanation (Galton/Faulds/Henry/FBI diagrams, Bertillon procedure) but real biometric datasets (NIST SD 302) and mugshot plates are not; ATHAR must synthesise fingerprints and faces.
5. Object props with readable dates (dinars/dirhams with AH dates, coin weights, seals, sundials, watches) support a dating mechanic (KO-CM-15-002) across many archetypes (ARC-09, ARC-04, ARC-11, ARC-23).

## Top 5 open questions / gaps for human or expert review
1. Legal: status of US-government works and of the Matson 2003 dedication outside the US (EU/UK/Arab states) for commercial use.
2. Legal: can ATHAR accept CC BY-SA for in-product art (share-alike on derivatives) — currently quarantined to 'reference only / display as-is'.
3. Legal: freedom of panorama for modern buildings in UAE/Qatar/KSA photos from Commons.
4. Cultural: human sensitivity review of manuscripts with the basmala and of city views where mosques are visible, before any use in a case.
5. Coverage: Gulf/Hejaz/Oman historic imagery and authentic Arabic administrative documents (telegrams, court registers, merchant ledgers) — next wave should pursue QDL partnership, Cleveland CC0 (ATH-SRC-1410), and commissioned art.
