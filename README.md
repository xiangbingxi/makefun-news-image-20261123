# news-image-20261123 — The World in One Day

One image summing up the world's news of **Monday, 23 November 2026**:
36 stories across 7 regions, the day's 6 biggest numbers, 3 illustrated
headlines, 10 more illustrated stories, a world map with 13 numbered pins,
a region bar, a DATE CHECK box for look-alike events from other days, and
a sources line. Drawn by hand with code (PIL flat vector style) — no
photos, no wire images.

## Files

- `main.py` — the entrypoint. Pure standard library: copies `entry.png`
  to `$MAKEFUN_OUTPUT_DIR/entry.png` (default `/output`), after verifying
  the PNG magic, the 1 MiB limit, and every PNG chunk's CRC through IEND.
  It does **no rendering** (the grader has no font library).
- `entry.png` — the finished image, 1024×1024 PNG.
- `tools/gen_image.py` — the development generator that draws `entry.png`
  with PIL + system DejaVu fonts.
- `NEWS.md` — all 36 stories with outlets, dates, region counts, and the
  DATE CHECK list.
- `HANDOFF.md` — method and verification results.
- `prompt.txt` — the build prompt, verbatim.
- `LICENSE` — MIT.

## Run

```sh
python3 tools/gen_image.py        # redraw entry.png (development only)
MAKEFUN_OUTPUT_DIR=out python3 main.py   # what the grader runs
```

## Verification

- 1024×1024 PNG, under 1 MiB, PNG magic correct, whole image decodes.
- `main.py` run twice into different output dirs produces byte-identical
  `entry.png` (same sha256), identical to the `tools/gen_image.py` render.
- 36 stories, 7 regions, date Monday 23 November 2026.
