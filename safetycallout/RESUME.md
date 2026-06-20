# SafetyCallout flyer + demo — RESUME

Marketing assets for **safetycallout.com**: a printed flyer with a QR that opens a
~30s vertical demo of a warehouse supervisor reporting an incident in the app.

QR target: **https://safetycallout.com/demo** (user hosts the final MP4 there).

---

## ✅ DELIVERED (local version — shipped, committed & pushed)

- **Demo video** `video/safetycallout_demo.mp4` — 25.5s, 9:16, on-brand, ambient audio.
  Hook → one-tap → speak (live waveform + transcript) → AI OSHA-ready report →
  submit → confirmed → QR end-card. Built fully locally by `build_video.py`.
- **Print-ready flyer** `assets/flyer.png` + `assets/flyer.pdf` (US Letter) — `make_flyer.py`.
  Scannable QR (decode-verified), phone mockup, voice-first messaging.
- **Editable Canva flyer** — design id `DAHNHCLWILI`
  - Edit: https://www.canva.com/d/mDiU0L_PRieswrb
  - View: https://www.canva.com/d/f3gvRcHyDC3AtO7
  - (QR Canva asset id `MAHNHN6KCms`; cleaned of AI-template junk, headline + DEMO CTA fixed.)
- **Embed page** `demo/` (index.html + safetycallout_demo.mp4 + poster.jpg) — drop the
  folder at safetycallout.com/demo so the QR opens a branded scan→watch page.
- **Brand system** `brand.py` (orange #F57820 / near-black, SC monogram), `icons.py`,
  `screens.py` (voice-first), `qr.py`, `cards.py`, `make_hazard.py`.

### To regenerate everything
`python3 brand.py icons.py screens.py make_hazard.py cards.py qr.py make_flyer.py`
then `python3 build_video.py` (ffmpeg via `imageio-ffmpeg`).

---

## OPTIONAL UPGRADE — AI-footage cut (needs Higgsfield CDN egress in a NEW session)

The current video is fully local (stylized, no photoreal person). To swap in real
AI warehouse footage, start a new session in the egress-enabled environment and
follow the pipeline below.

### Verify egress first


```bash
cd safetycallout && curl -sS -L -o clips/char.png -w "%{http_code}\n" \
 "https://d8j0ntlcm91z4.cloudfront.net/user_369o6rhJ3A6NBvc4YEC5fcBZIEs/hf_20260620_012840_22babfe7-742b-49e1-8e55-a558ecbb714d.png"
```
HTTP 200 + a real PNG = good. 403 "not in allowlist" = egress still not applied (need Full or Custom incl. these hosts, in the environment this session booted with).

Then rebuild deterministic assets: `python3 brand.py screens.py qr.py cards.py` (run each).

---

## Higgsfield assets already generated (account: Plus, ~754 credits at start)

Find via `show_generations(type="image")`. Job IDs + direct CDN URLs:

- **Supervisor character** (9:16) — `22babfe7-742b-49e1-8e55-a558ecbb714d`
  `https://d8j0ntlcm91z4.cloudfront.net/user_369o6rhJ3A6NBvc4YEC5fcBZIEs/hf_20260620_012840_22babfe7-742b-49e1-8e55-a558ecbb714d.png`
- **Hazard photo / spill** (16:9, for app `03_review`) — `3b53e15b-dd59-4432-9800-231b5f9b0396`
  `https://d8j0ntlcm91z4.cloudfront.net/user_369o6rhJ3A6NBvc4YEC5fcBZIEs/hf_20260620_012840_3b53e15b-dd59-4432-9800-231b5f9b0396.png`

Download both into `clips/`. Re-render review screen with the real photo:
`screens.load_photo("clips/hazard.png")` then `screen_review(photo=_PHOTO,...)`.

---

## Video plan — 9:16, ~30s, stitched with ffmpeg (imageio-ffmpeg)

Model: **seedance_2_0** (consistent identity), `aspect_ratio:"9:16"`, `generate_audio:false`,
`duration:5`. Pass the supervisor image as reference: `medias:[{value:"<char job id>", role:"image"}]`.
Cost ≈ 22.5 credits/clip.

| # | Source | ~sec | Content |
|---|--------|------|---------|
| 1 | clip A (AI) | 5 | Supervisor in hi-vis notices a spill by the racking, looks concerned |
| 2 | clip B (AI) | 5 | Pulls out phone, taps, starts speaking into it (voice report) |
| 3 | `01_home` → `02_listen` | 6 | App: tap "Report an Incident" → mic + live transcript |
| 4 | `03_review` | 5 | App: AI-drafted OSHA-ready report (real hazard photo) |
| 5 | `04_submit` → `05_confirm` | 4 | App: Submit → "team notified, PDF ready" |
| 6 | clip C (AI) | 3 | Supervisor nods, satisfied, back to work |
| 7 | `end_card` | 4 | // VOICE-FIRST · OSHA-ready in 60s · scan QR |

Add captions/VO (optional TTS via Higgsfield generate_audio / list_voices) and light music.
Download every clip to `clips/` before stitching (CDN egress required). Export `video/safetycallout_demo.mp4`.

Deliver MP4 to user → they host it at safetycallout.com/demo. Also build `demo/index.html`
embed page (poster = `end_card.png`) for a polished scan→watch experience.

---

## Canva flyer (editable)

Canva MCP can't read local files. Use the pushed QR via raw GitHub URL with
`upload-asset-from-url`:
`https://raw.githubusercontent.com/twandingle-cell/ct-preview/claude/lucid-hamilton-1ex9st/safetycallout/assets/qr_demo.png`
(same pattern for `end_card.png` / a chosen video poster frame).

Flyer copy: headline **"Call it out. Report it right."**, sub **"Voice-first incident
reporting — OSHA-ready reports in 60 seconds."**, big QR + **"Scan to watch the 30-second demo."**
Brand: near-black bg, orange `#F57820`, SC monogram, white text, mono accents.
Export print-ready PDF + PNG.
