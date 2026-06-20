# SafetyCallout flyer + demo — RESUME

Marketing assets for **safetycallout.com**: a printed flyer with a QR that opens a
~30s vertical demo of a warehouse supervisor reporting an incident in the app.

QR target: **https://safetycallout.com/demo** (user hosts the final MP4 there).

---

## STATUS

**Done & committed** (no network needed — all regenerate from scripts):
- `brand.py` — official brand: orange `#F57820` on near-black `#0A0A0A`, **SC** monogram, corner glow, mono kickers.
- `icons.py` — vector UI icons (mic, doc, sparkle, pin, camera, etc.).
- `screens.py` — voice-first flow → `screens/`: `01_home`, `02_listen` (mic + live transcript), `03_review` (AI-drafted OSHA-ready report), `04_submit`, `05_confirm`.
- `qr.py` — branded QR with SC mark, decode-verified → `assets/qr_demo.png`.
- `cards.py` — video end-card → `assets/end_card.png`.

**Pending** (needs Higgsfield CDN egress — now allowlisted in a NEW session):
1. Download the 2 generated images; drop the hazard photo into `03_review`.
2. Generate + download 3 AI warehouse clips.
3. Stitch the final vertical MP4 (clips + app screens + end-card + narration).
4. Build the editable Canva flyer around the QR.

---

## FIRST STEP in the new session — verify egress

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
