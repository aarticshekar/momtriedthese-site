# MTT content factory (branch: factory)

Hostinger deploys `main` only. This branch holds the generators and each week's scripts.

## Tools
- `tools/video.js <videos.json> <outdir>`: 1080x1920 silent kinetic-type mp4s + covers. Needs playwright (preinstalled) and ffmpeg.
- `tools/images.js <images.json> <outdir>`: Instagram slides (1080x1350) to `<outdir>/instagram/<id>/NN.jpg` + caption.txt, pins (1000x1500) to `<outdir>/pins/<id>.jpg`.
- See `weeks/w1/` for the exact JSON shapes. Scene classes: `dark`, `sun` (CTA). Elements: `.k` kicker, h1/h2 with `<em>` accent, p, `.num`, `.card`, `.tag` (On my list / Bought by us), `.tag.r` (Researched pick). Add `in` class to animate in.

## Weekly recipe
1. Research: Amazon autocomplete for the season, Pinterest trends, what is on the site (`main` branch, sitemap.xml). Check `weeks/` so nothing repeats.
2. Write `weeks/wN/videos.json` (3 Reels, 12-20s, 5-8 scenes, hook in first scene, sun CTA last) and `weeks/wN/images.json` (2 carousels, 2 thought posts, 14 pins). Rotate hook formulas from HOOKS.md. Follow VOICE.md.
3. Render to `out/`. Look at every cover jpg before shipping.
4. On `main`: copy outputs to `social/wN/` (mp4, covers, slides, pins, one `<id>.txt` caption each, and an index.html listing them). Commit and push (auto-deploys). Commit `weeks/wN/` on `factory`.
5. Do NOT post anywhere. Send Aarti the link momtriedthese.com/social/wN/ for approval.
