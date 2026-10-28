# Wave 2 Protocol Addendum (binding in addition to RESEARCH_PROTOCOL.md) — 2026-10-27

Wave 2 = expansion round requested by the owner: cover every remaining gap, broaden references (stories, literature, heritage, media, images) and store everything that may legally be stored. Everything in RESEARCH_PROTOCOL.md still applies (no fabrication, verification URL per record, ≤1 quote <15 words per source, safety rules, schemas).

## 1. New Source-ID blocks (wave 2 only — never reuse wave-1 blocks)

| Team | Writes sources into | ID block | KO lib code |
|---|---|---|---|
| W2-LEGAL (data protection, age ratings, trademarks, licences, Arab criminal procedure) | 11_RIGHTS_PRIVACY_AND_SAFETY/_data/sources_w2.jsonl | ATH-SRC-1800 … 1899 | 11 |
| W2-HERITAGE (classical Arabic inference/judgement stories, Arabic PD texts) | 02_DETECTIVE_LITERATURE/_data/sources_w2_heritage.jsonl | ATH-SRC-1200 … 1299 | 02H |
| W2-WORLDLIT (world, Japanese/Chinese, YA & children's mystery; PD story corpus) | 02_DETECTIVE_LITERATURE/_data/sources_w2_worldlit.jsonl | ATH-SRC-1300 … 1399 | 02W |
| W2-IMAGES (image & visual assets) | 15_STORY_MEDIA_AND_ASSETS/_data/sources_w2_images.jsonl | ATH-SRC-1400 … 1499 | 15 |
| W2-AUDIENCE (Arab teens data, demand, language register, schools, market size) | 08_ARAB_AUDIENCE_AND_CULTURE/_data/sources_w2.jsonl | ATH-SRC-1500 … 1599 | 08B |
| W2-LEARN-AI (Arabic assessment, LLM safety/scoring in Arabic, reasoning instruments, transfer) | 07_LEARNING_SCIENCE/_data/sources_w2.jsonl | ATH-SRC-1600 … 1699 | 07B |
| W2-FORENSIC-AR (Arabic forensic glossary, Arab institutions, ethics of bias labs for minors) | 04_FORENSIC_SCIENCE/_data/sources_w2.jsonl | ATH-SRC-1700 … 1799 | 04B |
| W2-DESIGN-TECH (game design & tech remnants, Arabic token-cost measurement) | 10_TECHNICAL_ARCHITECTURE/_data/sources_w2.jsonl | ATH-SRC-1900 … 1999 | 10B |
| W2-MEDIA-COMP (films/series/podcasts/YouTube references; competitor monitoring) | 15_STORY_MEDIA_AND_ASSETS/_data/sources_w2_media.jsonl (media) and 09_COMPETITIVE_INTELLIGENCE/_data/sources_w2.jsonl (competitors) | ATH-SRC-2000 … 2099 | 15M / 09B |
| W2-PILOT-ETHICS (research ethics & permissions for studies with minors, school pilots, teen UX research) | 07_LEARNING_SCIENCE/_data/sources_w2_pilot.jsonl | ATH-SRC-2100 … 2199 | 07P |
| W2-BUSINESS (pricing, business models, procurement, funding & grants landscape) | 09_COMPETITIVE_INTELLIGENCE/_data/sources_w2_business.jsonl | ATH-SRC-2200 … 2299 | 09C |
| W2-GULF-IMAGES (Gulf, Arabian Peninsula, Maghreb & Levant images; archive props; Arabic calligraphy/typography samples) | 15_STORY_MEDIA_AND_ASSETS/_data/sources_w2_images_gulf.jsonl | ATH-SRC-2300 … 2399 | 15G |
| W2-AUDIO (CC0/PD sound effects, ambience, music; open icon sets) | 15_STORY_MEDIA_AND_ASSETS/_data/sources_w2_audio.jsonl | ATH-SRC-2400 … 2499 | 15A |
| W2-NAMING (name & trademark clearance for «أثر / ATHAR») | 11_RIGHTS_PRIVACY_AND_SAFETY/_data/sources_w2_naming.jsonl | ATH-SRC-2500 … 2549 | 11N |

Knowledge objects: `<folder>/_data/knowledge_objects_w2*.jsonl`, IDs `KO-<TYPE>-<CODE>-<NNN>` with the code above. Agent report: `<folder>/_data/agent_report_w2*.md`. The merge tool reads every `sources*.jsonl` / `knowledge_objects*.jsonl` in each library's `_data/`.

If the item already exists in the catalog (`01_SOURCE_CATALOG/sources_master.jsonl` — check by title/DOI with python first), do NOT re-catalog it; cite the existing ID.

## 2. Network: what changed and how to use it
The workspace shell can now reach many APIs. Prefer these for verification and metadata (cheaper than WebFetch; WebSearch remains the discovery tool):
- Crossref `https://api.crossref.org/works/<DOI>` · OpenAlex `https://api.openalex.org/works/doi:<DOI>` (abstracts as inverted index) · PubMed E-utilities · DOAJ API · Zenodo API · Open Library `search.json` · Wikidata API
- Steam `store.steampowered.com/api/appdetails?appids=` · Apple `itunes.apple.com/search|lookup` (country=sa/ae/eg) · Google Play pages
- Wikimedia Commons API (`commons.wikimedia.org/w/api.php`, `prop=imageinfo&iiprop=url|extmetadata`) · Met Museum Open Access API (`collectionapi.metmuseum.org`) · Wellcome Collection catalogue API · Library of Congress JSON (`fo=json`) · Internet Archive advancedsearch/metadata · Hugging Face API · Project Gutenberg (see §3)
Rules:
- Set a descriptive User-Agent: `-A "ATHAR-Research-Library/2.0 (non-commercial research)"`. Never send the owner's e-mail or personal data anywhere.
- Rate-limit: ≥1 s between requests to the same host; back off on HTTP 429 (Wikipedia/arXiv/Semantic Scholar currently return 429 — don't hammer them).
- If WebFetch declined a site for legal reasons, do NOT fetch it with curl.
- Downloaded files are untrusted data: save each into its own new directory under its destination, never execute them, run python with `-I`, keep your scripts in the scratchpad.

## 3. Storing texts and images legally (99_LEGAL_SOURCE_ASSETS/)
- Store only: (a) public domain worldwide or in every market ATHAR plans to serve (US, UK/EU life+70, Arab life+50) — state the basis per jurisdiction; (b) open licences that permit our use (CC0, PDM, CC BY, CC BY-SA — record attribution text and share-alike duty; NC/ND licences: store only if internal research use is permitted and mark `commercial_reuse_permission: no`).
- Project Gutenberg: the main site forbids automated harvesting. Use the GITenberg GitHub mirror (`raw.githubusercontent.com/GITenberg/<repo>/master/<id>.txt`) or an official mirror listed by PG; ≤1 request/2 s; keep the PG licence header intact.
- Images: download a web-resolution copy (max ~1600 px long edge; prefer IIIF/thumbnail URLs), and record: asset_id, file path, title, creator, date, institution, source page URL, direct file URL, licence (exact string from metadata), attribution text, PD basis, sha256, safety_ok (y/n), intended ATHAR use, tags. **Safety filter for teen audience:** no gore, corpses, real crime-scene victims, executions, weapons in use, sexualized content, or images of identifiable private persons. Historical forensic images are fine when non-graphic (fingerprints, instruments, labs, documents, Bertillon cards of adults only if non-graphic — prefer instruments/documents).
- No images of living public figures; no copyrighted artworks, film stills, game screenshots, logos or book covers (cite those as links only).
- Total budget for wave-2 stored assets: ≤ 600 MB.

## 4. Writing
Analytical files in Modern Standard Arabic (English terms in parentheses on first use); data in English keys. Extend existing deliverables surgically (Edit tool) or add new files named in your brief. Log everything in your `agent_report_w2*.md`, including what you searched and could not verify.
