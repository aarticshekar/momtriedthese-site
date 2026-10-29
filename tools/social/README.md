# MTT social factory

All renderers run from the repo root with `ROOT=$PWD`. Product images come from `images/out/<slug>.jpg` (brand-site images only, never Amazon). Fonts come from `site/static/fonts/`.

- Pins: add entries to `tools/pins/pins.json` (status "queued"), then run `node tools/pins/pin.js`. Images land in `site/static/pins/`; commit them on the factory branch so the raw GitHub URL works. The daily Pinterest task publishes 3 queued pins.
- Reels: `node tools/social/reel.js <spec.json> <outdir>`. Spec format: see `specs/reels-2026-11-a.json`. Formula: hook, 5 products about 2s each with name and reason, then the CTA plus an on-screen #ad. Exports silent (add a trending sound in the app).
- Carousels: `node tools/social/carousel.js <posts.json> <outdir>`. Full-page design. Spec format: see `specs/carousels-season.json`.

Rules: the note rule (reasons only, no sales or popularity talk), vegetarian, no em dashes, no invented use, never the child's name or age, #ad plus the Associates line on product posts.
