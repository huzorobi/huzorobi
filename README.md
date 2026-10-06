# HuzoSecurity LinkedIn posters

Image files used for scheduled HuzoSecurity LinkedIn posts. Not part of the profile README.

## Instagram Reels

From 7 October 2026 Instagram gets an animated Reel each day instead of the static card.

- `reels/make_reels.py` builds the Reels from the approved cards (`python3 reels/make_reels.py . out/ 10 11 ...`).
- `reels/cards.json` holds the tag, stat and headline for each card; body, steps and source come from the captions.
- `instagram/reels/` holds the finished MP4s, `instagram/reels.json` the daily schedule the poster reads.
- `instagram/schedule.json` now only lists the image posts that already went out (days 1 to 9).
