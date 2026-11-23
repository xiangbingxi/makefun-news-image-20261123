# HANDOFF — news-image-20261123

## Competition

- **Slug:** news-image-20261123
- **Title:** "Sum up 23 November's world news in one image"
- **Prize:** $100 — 1st $20, 2nd $12, 3rd $6, 4th–10th $2, 11th–50th $1.20
- **Deadline:** 2026-11-25 08:00 CST (2026-11-25T00:00:00Z)
- **Results:** 2026-12-09
- **Judge:** z-ai/glm-5.3-flash, pairwise image comparison, no ties
- **Limits:** at most 10 submissions/day, 20 total; last submission is final
- **Rules (competition.yaml + RULES.txt):** program at repo root, main.py
  (Python 3.13) or main.ts (Node 22); writes one image to
  /output/entry.png; PNG or JPEG, at most 1 MiB, at most 1024×1024 px;
  no network; program runs twice and both runs must write the same bytes.
  News = events that happened, or were first reported, on 23 November
  2026 in any time zone.
- **Kit:** kit/ in the parent workdir (competition.yaml + RULES.txt read).

## What the image contains (36 stories, 7 regions)

Front page "THE WORLD IN ONE DAY — MONDAY, 23 NOVEMBER 2026",
1024×1024, hand-drawn flat vector with PIL, no photos, no wire images.

- **3 big illustrated headlines:** COP31 collapses with no deal — written
  as a Monday follow-up ("ANTALYA — MONDAY FOLLOW-UP"; talks ended Sun
  22 Nov, Monday's wires led with the fallout); 24 dead in the Banten
  candy-factory fire (flame + factory; 23 Nov casualty update); AI
  sell-off rattles markets (falling chart).
- **10 small illustrated stories:** Dymer boy pulled alive, Merkury sunk
  off Libya, Democrats secure at least 258 House seats, Hormuz tankers
  ablaze, South Sudan 24 killed, Khartoum drones kill 5 children, Gaza
  "toxic wasteland", Belgium airports shut, Delta outage, Marquez 8th
  MotoGP title — flagged in its title as a Sun 22 Nov result.
- **Map "WHERE IT HAPPENED"** with 13 numbered red pins + **23 numbered
  briefs** (14–36): Iowa blast, Nepal PM meets Modi, Bangladesh/Hasina,
  Vietnam rare-earth plant, India power index, seized chemical ship, Iran
  MQ-9 claim, Houthi refinery claim / Hodeida, Gulf bourses, Ebola in DR
  Congo, EU Rwanda centres, France PMI, Istanbul rally, Bolsonaro in ICU,
  Hong Kong vote, Tata Steel $1.67bn, hedge funds' worst week, Wall Street
  bounce, FDA blood-pressure drug, FedEx hijack hero dies, AP Top 25,
  Russian oil exports curbed, Denmark murder-plot accusation.
- **Region bar:** Europe 9, North America 7, Asia 8, Middle East 5,
  Africa 4, South America 1, Global 2 (total 36).
- **Footer:** "HOW THIS PAGE WAS MADE — Drawn by hand with code: no
  photos, no wire images. News and follow-ups reported Mon 23 Nov 2026;
  COP31 and Marquez are Sun 22 Nov results, flagged in their items."
  + sources line (AFP, AP, Reuters, CNN, The Guardian, Le Monde, WSJ,
  Al Jazeera, Oxfam/CEOBS, One Turn, Inshorts, IANS, Times Now, Dubai
  Standard, Addis Standard, CNBC Indonesia, SCMP, Lowy Institute, WHO).

## Revision (23 Nov evening, after user review)

The first version was reviewed and the following changed:

1. **[P1] Dates:** COP31 rewritten as a 23 Nov follow-up (talks ended Sun
   22 Nov); Marquez flagged "(SUN 22 NOV)" in its title; Indonesia fire
   kept (23 Nov casualty update); footer no longer claims every story
   happened on 23 Nov.
2. **[P2] 258 seats:** AP said "at least 258". Story #6 title is now
   "DEMOCRATS SECURE AT LEAST 258 HOUSE SEATS".
3. **[P2] Layout:** the top numbers strip and the DATE CHECK box were
   deleted (both duplicated story content and crowded the thumbnail). The
   freed space went to taller headline boxes, taller story cards, a
   taller map and bigger briefs type (body 9→10, titles 10→11, big body
   11→12). The old numbers-strip overflow bug (last card ran 9 px past
   the right edge) is gone with the strip.
4. **Map:** added Japan, Indonesia (Sumatra, Java, Borneo, Sulawesi, New
   Guinea, Philippines, Taiwan), Greenland, New Zealand, Central America
   and a Turkey/Levant coast polygon; small island groups are drawn
   slightly larger than true scale so pins sit visibly on land. All land
   is clipped to the frame (lat 75 to −55) with Sutherland–Hodgman, so
   Asia's northern edge no longer spills past the top border. Base map
   and pins use the same equirectangular projection.
5. **gen_image.py output path:** was relative to the script's directory
   (would write outside the repo if the script moved to the repo root).
   Now a fixed path inside the repo (OUT_PATH env overrides). main.py
   shim untouched (pure-stdlib copy of the finished entry.png).

## File layout (~/workspace/makefun/news-image-20261123/repo/)

- `main.py` — entrypoint. Pure-stdlib copy shim: reads `entry.png`,
  verifies PNG magic + ≤1 MiB + every PNG chunk CRC through IEND, copies
  to `$MAKEFUN_OUTPUT_DIR/entry.png` (default /output), prints size +
  sha256. No rendering here (grader has no font library).
- `entry.png` — finished render (see verification).
- `tools/gen_image.py` — the dev generator (same drawing code, fixed
  OUT_PATH). Rewritten in the revision (layout, map, dates, output path).
- `NEWS.md` — all 36 stories with sources, numbers, DATE CHECK audit,
  region counts; updated for the revision (258 wording, COP31/Marquez
  dates, strip removal note).
- `HANDOFF.md` — this file.
- `prompt.txt` — the user's exact quote, one line, no trailing newline.
- `README.md`, `LICENSE` (MIT, SPDX line), `.makefun/owner.json`
  (wallet 6t8k8dD19c2zDMiZ1VNsbRDWaSNSedmQQB6A15hy3XFx).

## Verification (revision, all done in this session)

- `python3 tools/gen_image.py` → entry.png 1024×1024, 172,389 bytes.
  Viewed the image three times (full + zoomed crops of the top stories,
  the small stories, the map, and tight crops of the Tokyo and Banten
  pins). Fixes made across passes:
  1. First render: point-in-polygon check found 3 pins off land
     (Antalya, Benghazi, Gaza) — added Turkey/Levant polygon, pushed
     Africa's north coast slightly north.
  2. Ring check (land pixels in a 9–16 px ring around each pin) showed
     Tokyo and Banten mostly surrounded by sea — widened Japan and Java.
  3. Two small-story bodies truncated at 2 lines (#10 Gaza, #12 Delta)
     — shortened both to fit.
  Final view: COP31 follow-up wording correct, Marquez flagged
  "(SUN 22 NOV)", "AT LEAST 258" correct, Tokyo and Banten pins sit on
  visible land (Japan island, Java strip), no text overflow or overlap,
  headlines legible at thumbnail size.
- **Pin check (computational):** all 13 pin lon/lat points inside a
  clipped land polygon (point-in-polygon). Tokyo on Japan, Banten on
  Java, Antalya on Turkey, Gaza on the Levant coast, Benghazi on Libya.
- **Two-run determinism (main.py):** ran twice with different
  MAKEFUN_OUTPUT_DIR values (/tmp/out1, /tmp/out2), scratch dirs deleted.
  Both runs:
  - size 1024×1024, PNG, 172,389 bytes
  - sha256 `6106658e88727ec1c015fba58d1b0d972759dd494b45a0de6049d2bc69b990a6`
  - identical to each other AND to the tools/gen_image.py render.
  Byte-identical confirmed.
- **Requirements check:** 1024×1024 ≤ 1024×1024 ✓; 172,389 ≤ 1,048,576 ✓;
  PNG magic ✓; whole-image decode (PIL load) ✓; chunk CRC walk in main.py
  ✓; 36 stories, 7 regions, date Monday 23 November 2026 ✓.

## Small fix (23 Nov evening, second user review)

User approved the revision; one small fix remained:

- **Brief #17 title truncated:** "VIETNAM BREAKS GROUND ON RARE-EARTH
  PLANT" measured 316 px at DejaVuSans-Bold 11, over the 304 px briefs
  column; the briefs renderer only draws the first wrapped line, so
  "PLANT" was dropped. Title shortened to "VIETNAM STARTS RARE-EARTH
  PLANT" (232.8 px, same meaning). NEWS.md entry #17 updated to match.
- **Sweep for the same truncation:** measured all 23 brief titles (11 pt
  bold, limit 304 px) and all 23 brief bodies (10 pt regular, limit
  306 px). Only #17's title was over; the next longest titles are #30
  (285.8 px), #36 (285.6 px), #32 (281.8 px). All bodies fit. No other
  title or body needed changing.
- main.py untouched; prompt.txt untouched.

## Verification (small fix, all done in this session)

- `python3 tools/gen_image.py` → entry.png 1024×1024, 172,065 bytes.
  Viewed full image + a 2× zoom of the whole briefs block (14–36):
  #17 reads "VIETNAM STARTS RARE-EARTH PLANT" in full; every other
  brief title and body is complete on one line, no truncation.
- **Two-run determinism (main.py):** ran twice with different
  MAKEFUN_OUTPUT_DIR values (/tmp/out1, /tmp/out2), scratch dirs deleted.
  Both runs: 172,065 bytes, sha256
  `6d83278fec3b025f9acc085df3cd378c797b18316d60bc172bdef02825a953fc`,
  identical to each other AND to the tools/gen_image.py render.
- **Requirements check:** 1024×1024 ≤ 1024×1024 ✓; 172,065 ≤ 1,048,576 ✓;
  PNG magic ✓; whole-image decode (PIL load) ✓; chunk CRC walk in main.py
  ✓; 36 stories, 7 regions, date Monday 23 November 2026 ✓.

## Still to do (parent — NOT done here)

- Do NOT submit yet (per task). When ready: create the GitHub repo
  (must be created after the competition opened, 2026-11-23T00:00:00Z),
  push main.py + entry.png + NEWS.md + HANDOFF.md + prompt.txt +
  README.md + LICENSE, add .makefun/owner.json, set About, write usage,
  bundle with this session as --session, check, submit before
  2026-11-25 08:00 CST. Quota: check
  /api/competitions/news-image-20261123/quota before submitting.
- prompt.txt must stay exactly one line with no trailing newline.
