# Agent report — W2-AUDIO (sound effects, ambience, music, UI icons) — 2026-10-27

## Counts
- **Audio assets stored: 165** (78.8 MB of audio; IDs AUD-0001…AUD-0165), all in `AUDIO_ASSET_REGISTER.csv` with exact licence string, attribution text, PD basis, SHA-256 (re-verified), duration, format, bytes, intended use, tags (including `loudjump`) and safety flag.
  - PUBLIC_DOMAIN_VERIFIED/audio (CC0): **108** files, 27 MB. Kenney 67 [ATH-SRC-2400], OpenGameArt CC0 30 [ATH-SRC-2402], Musopen Chopin 11 [ATH-SRC-2410].
  - OPEN_LICENSE/audio: **57** files, 50 MB. radio aporee field recordings: 52 Public Domain Mark 1.0 + 4 CC BY 3.0 [ATH-SRC-2401]; 1 legacy CC public-domain Morse sample [ATH-SRC-2403].
  - Not stored: anything NC, ND or BY-SA.
- **Icon sets stored: 6** (232 SVG + 6 licence files, 1.0 MB): Material Symbols (Google repo commit 10ecc14), Lucide 1.62.0, Phosphor core 2.1.1, Tabler 3.49.0, Heroicons 2.2.0, Fluent UI System Icons 1.1.344. All SVGs were scanned for script/event handlers/external hrefs (0 found).
- **Total wave-2 storage by this team: ≈79 MB** (budget ≤150 MB).
- **Sources cataloged: 31** (ATH-SRC-2400–2403, 2410–2416, 2420–2427, 2430–2441). Deep cards: 0 (not required by brief). **Knowledge objects: 5** (KO-CM-15A-001…003, KO-PO-15A-001, KO-LA-15A-001).

### Audio by collection
| folder | tier | files | licence |
|---|---|---|---|
| kenney_interface_sounds | PD | 26 | CC0 |
| kenney_rpg_audio | PD | 21 | CC0 |
| kenney_impact_sounds | PD | 15 | CC0 |
| kenney_ui_audio | PD | 5 | CC0 |
| oga_book_flips / oga_keyboard / oga_paper / oga_misc_cc0 / oga_interface_beeps | PD | 6 / 5 / 6 / 7 / 6 | CC0 (per OGA page) |
| musopen_chopin_cc0 | PD | 11 | CC0 1.0 |
| ia_aporee_maghreb (Tunis, Fes, Meknes, Marrakech, Tangier, Laassilat, Tissardmine) | OPEN | 18 | PDM 17, CC BY 1 |
| ia_aporee_gulf (Sharjah, Dubai, Liwa, Bahrain) | OPEN | 12 | PDM |
| ia_aporee_foley_rooms (typewriter, library, print shop, clocks, keys, phone tone, server room, café) | OPEN | 15 | PDM 13, CC BY 2 |
| ia_aporee_weather_water (rain, thunder, storm, wind, harbour, moored boat) | OPEN | 6 | PDM 5, CC BY 1 |
| ia_aporee_egypt_sudan / ia_aporee_levant | OPEN | 3 / 2 | PDM |
| ia_misc_open (Morse) | OPEN | 1 | legacy CC PD |

## Files produced
- `15_STORY_MEDIA_AND_ASSETS/SOUND_DESIGN_GUIDE.md` (Arabic): evidence, layers, age rules, accessibility, cultural cautions, attribution, sound palette per setting, RTL icon rules, pipeline, open questions.
- `15_STORY_MEDIA_AND_ASSETS/AUDIO_ASSET_REGISTER.csv` (165 rows).
- `15_STORY_MEDIA_AND_ASSETS/ICON_AND_UI_ASSET_REGISTER.csv` (6 rows; adds `licence_obligations`, `verification_url` and `catalog_source_id` to the requested columns).
- `15_STORY_MEDIA_AND_ASSETS/_data/sources_w2_audio.jsonl` (31), `_data/knowledge_objects_w2_audio.jsonl` (5), and this report.
- Assets: `99_LEGAL_SOURCE_ASSETS/PUBLIC_DOMAIN_VERIFIED/audio/<collection>/`, `99_LEGAL_SOURCE_ASSETS/OPEN_LICENSE/audio/<collection>/` and `99_LEGAL_SOURCE_ASSETS/OPEN_LICENSE/icons/<set>/`. Each audio collection folder has `License.txt` (Kenney, bundled), `LICENSE_NOTE.txt` (OGA, IA, Musopen) or the bundled CC0 legal code (AntumDeluge clock).
- Scripts are in the scratchpad (`…/scratchpad/w2audio/`) and are not part of the library: net.py, store.py, loud.py, ia_import.py, kenney_import.py, oga_import*.py, music_import.py, icons_dl.py, build_sources.py, build_kos.py.

## Method and interpretations (owner away; recorded here)
1. **Tier mapping.** CC0 assets went to PUBLIC_DOMAIN_VERIFIED, following the images team's practice (Met CC0 → PD). Public Domain Mark items went to **OPEN_LICENSE**, not PD: PDM on a 2004–2025 field recording is a label set by the recordist, not a term-expired work and not a CC0 waiver. The register states this in `pd_basis`.
2. **Excerpts, not full files, for field recordings.** Long recordings (2–15 min, up to 380 MB lossless) were cut to 45–90 s and re-encoded to Ogg Vorbis q3. The window was chosen automatically as the one with the lowest "loudness jump" (EBU R128 momentary max minus median), to avoid startling peaks. Excerpt times are in each `attribution_text`. Short SFX were copied as-is (Kenney OGG) or re-encoded at q5.
3. **Religious-audio filter.** Items whose title or description matched prayer/adhan/mosque/Qur'an/church/Sufi/dhikr terms were excluded: most at candidate selection (adhan and prayer items in Fes, Manama, Essaouira, Tunis were never queued) and 1 automatically at import (a Fes 'musicians' item whose description mentioned the call to prayer). **Nothing was auditioned by ear.** Distant adhan, incidental speech or shop radios may still be present: human listening is mandatory before production (all safety flags say so).
4. **Music.** The only music stored is CC0 Musopen Chopin (composer d.1849; recording CC0 per the Internet Archive item uploaded by Musopen's own account; Libre Arts 2013 corroborates the CC0 promise). Plus one diegetic field recording of an oud and darbouka street duo (PDM). **Early Arabic recordings (LoC National Jukebox, 1916–1925) were cataloged but NOT stored**: they are US PD under the Music Modernization Act, but the songwriters are unidentified, status outside the US is unknown, and all are vocal songs. This follows the brief's "skip if unclear".
5. **Material Symbols.** The npm package @material-symbols/svg-400 is a third-party repackaging, so it was deleted after download and replaced with SVGs from Google's own repository, pinned to the commit.
6. **Freesound** was not fetched at all: robots.txt disallows ClaudeBot site-wide and downloads need OAuth2. **BBC Sound Effects** is catalog-only (RemArc non-commercial; the licence page was blocked to our fetcher).

## Search strategy
Internet Archive advancedsearch (simple title queries per Arab city and per SFX keyword; wildcard licence filters returned backend errors) plus the metadata API per item. Kenney official asset pages. OpenGameArt pages found via WebSearch (robots disallows /search/), fetched with a 10 s crawl delay. LoC JSON API (National Jukebox). NASA images API. npm registry and jsDelivr for icon versions; raw.githubusercontent.com for upstream licences. Crossref and OpenAlex for research DOIs and abstracts. WebFetch for W3C, Xbox, GAG, Material v1, Wikimedia Codex, LoC blog, Cambridge (Mayer), Engadget.

## Blockers
- **Wikimedia Commons returned HTTP 429 for almost the whole session** (API and file pages; shared egress with other wave-2 teams). One partial search ran ("WWS …" historical machine sounds: typewriters, teleprinters, rotary dialling, ship engine telegraph), but licence metadata could never be fetched. **No Commons audio stored.** This is the main open item.
- musopen.org returned 403 to curl; marineband.marines.mil returned 403 to curl (WebFetch worked); BBC licence page blocked; GitHub API blocked (raw files OK); psycnet (APA) robots-disallowed.
- Internet Archive search intermittently returned "BACKEND_ERROR" on complex queries.

## Unverified candidates (not cataloged as sources)
- Wikimedia Commons "WWS" series (e.g., File:WWS Typewriter.ogg, WWS Teleprintertyping.ogg, WWS Dial-operatedtelephone.ogg, WWS ShipSodekengineordertelegraph.ogg) and "File:Turning a page.ogg": titles seen in search results, but licence pages could not be read (429).
- Internet Archive "office-sound-effects" (CC0 label set by an anonymous uploader, but the description says the files came from mixkit/pixabay/soundbible, whose own licences are not CC0). **Rejected as laundering risk.** "turkish-instrumental-music" (CC0 label, contents from pixabay): rejected for the same reason.
- Alexander Maloof's death year (needed for the PD status of his 1913 compositions): not found in verified sources.
- Material Design m2/m3 bidirectionality pages need JavaScript; only the m1 page was read.

## Top 5 findings that should change ATHAR's design
1. **Invest in sound effects before music.** Sound on/off affected every self-reported experience dimension, while music alone had no main effect [ATH-SRC-2433]. Background music disturbs reading [ATH-SRC-2431], so evidence screens should be music-free, with music only in transitions, epilogues and short pre-deduction bridges [ATH-SRC-2432].
2. **Every sound clue needs a visual twin** (transcript or caption), captions available before the first sound, four independent volume channels, and a mono toggle [ATH-SRC-2435] [ATH-SRC-2437] [ATH-SRC-2436].
3. **Religious audio is a release-level risk**: LittleBigPlanet was recalled and delayed worldwide over Qur'anic phrases in a background track [ATH-SRC-2441]. Every ambience file from an Arab city needs human audition for distant adhan.
4. **Music-optional onboarding** (a neutral choice, with full SFX parity) addresses contested attitudes to music [ATH-SRC-2439] at low cost (KO-PO-15A-001).
5. **Authentic Arab soundscapes exist under open terms** (Tunis, Fes, Marrakech souqs and crafts quarters; Bahrain and Sharjah harbours and fish auctions; Liwa wind). The world-building can sound real without orientalist "mystery" clichés. Gaps remain: Saudi, Kuwaiti, Omani, Iraqi and Levantine streets.

## Top 5 open questions / gaps for human or expert review
1. **Legal:** Is a recordist-applied Public Domain Mark (52 files) sufficient for commercial use in KSA, UAE, Lebanon and Egypt? Do street performers' related rights matter (AUD-0134)? Consider contacting the recordists (Chris Weaver, J.-F. Cavro, Frank Schulte) for explicit CC0.
2. **Legal:** Phonogram related-rights terms in Arab markets, which decide whether the 1916–1925 Arabic recordings could ever be used outside the US.
3. **Audition:** All 56 radio aporee excerpts and the 11 "caution" files need human listening (adhan, speech, radio music, startle peaks). 33 files peak at 0 dBFS and need normalising.
4. **Commons retry:** Re-run the Commons audio survey when rate limits clear (WWS historical machine sounds, telegraph, rotary phone, "Sounds of …" categories). Owner may register a Freesound API key for CC0-only pulls.
5. **Commissioned score:** A short Arab-instrument palette (oud/qanun/ney "aha" phrase, case-solved motif, music-free alternative) to replace the placeholder Chopin, plus focus-group testing of the music-off onboarding question.
