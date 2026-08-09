# SafetyCallout — Cowork Handoff

Continuation doc for this project. Hand this to a Cowork/Claude session to pick up where we left off.

- **Repo:** `twandingle-cell/ct-preview`
- **Working branch:** `claude/lucid-hamilton-1ex9st`
- **Owner:** twan.dingle@gmail.com
- **Date:** 2026-08-09

> ⚠️ Note: the repo root `index.html` is a *different* project ("ChainLogic AI — Control Tower" preview). All SafetyCallout work lives under `safetycallout/`. The public site **safetycallout.com is hosted elsewhere** (host/registrar not yet identified — see open items).

---

## 1. What's done & committed

| Deliverable | Location |
|---|---|
| Demo video (25.5s, 9:16, audio) | `safetycallout/video/safetycallout_demo.mp4` |
| Print-ready flyer (PNG + PDF) | `safetycallout/assets/flyer.png` · `flyer.pdf` |
| Editable Canva flyer | https://www.canva.com/d/mDiU0L_PRieswrb |
| Drop-in scan-to-watch demo page | `safetycallout/demo/` (index.html + mp4 + poster) |
| App screens (rebranded) | `safetycallout/screens/*.png` |
| Build scripts | `safetycallout/*.py` (build_video, make_flyer, screens, brand, qr, …) |
| Prior resume notes | `safetycallout/RESUME.md` |

**Go-live step still pending:** upload the `demo/` folder to `safetycallout.com/demo` so the flyer's QR opens the branded page.

---

## 2. AI footage (Higgsfield) — assets generated

All generated server-side in Higgsfield. **This container cannot download from the Higgsfield CDN** (`d8j0ntlcm91z4.cloudfront.net` is not in the sandbox allowlist — returns 403). Downloading/compositing the clips into the polished cut requires a **new session in an egress-enabled environment**. The user's browser CAN open these URLs.

### Character / stills
- Supervisor character image — job `22babfe7-742b-49e1-8e55-a558ecbb714d`
- Real app voice-screen imported into Higgsfield — media `9a63a292-2ebb-46f5-9c46-782e156aab2b` (from `safetycallout/screens/02_listen.png`)
- Composite stills (supervisor holding phone showing the **real** app UI), `nano_banana_pro`:
  - **A (chosen)** — job `6b7986c4-d6c6-4abc-9839-98c3b8b5e0c6`
  - B — job `57a4f99c-6bfd-4cb6-8a43-f21e32a39c98`

### Video clips (seedance_2_0, 9:16, 1080p, audio)
- Supervisor notices spill → raises phone → reports → nods — **10s**:
  - Variant A — job `950e1e46-ebc3-4607-abc0-89da233fb2e8`
    `https://d8j0ntlcm91z4.cloudfront.net/user_369o6rhJ3A6NBvc4YEC5fcBZIEs/hf_20260620_131414_950e1e46-ebc3-4607-abc0-89da233fb2e8.mp4`
  - Variant B — job `ba23419c-4bbd-40bf-8361-524ba67ef4bf`
    `https://d8j0ntlcm91z4.cloudfront.net/user_369o6rhJ3A6NBvc4YEC5fcBZIEs/hf_20260620_131414_ba23419c-4bbd-40bf-8361-524ba67ef4bf.mp4`
- **App-on-phone clip** (animated from composite A, real UI visible) — **8s**, job `441adba6-063e-4514-b952-70c4e8aca003`
  `https://d8j0ntlcm91z4.cloudfront.net/user_369o6rhJ3A6NBvc4YEC5fcBZIEs/hf_20260620_134322_441adba6-063e-4514-b952-70c4e8aca003.mp4`

### Feedback / status
- First two clips (950e1e46 / ba23419c): user felt they **didn't clearly show the app**.
- Fix applied: composited the **real app screen onto the phone** (via `media_import_url` of the GitHub raw PNG → `nano_banana_pro`), then animated → clip `441adba6`. **Awaiting user verdict** on whether the app now reads clearly.
- To surface a clip to the user in chat: Higgsfield `job_display` with the job id (renders inline).

### Next options for the video
1. If `441adba6` looks good → use as hero clip; host at `/demo`, or fold into the full cut.
2. If UI warps on motion → re-animate with near-zero motion (locked phone, slow push-in, mouth-only).
3. Full polished cut = AI footage **intercut with legible app screens + branded end-card + QR** → needs egress (new session) to download clips and run `build_video.py` stitching.

---

## 3. IN PROGRESS — Google Search Console (indexing)

User wants **safetycallout.com** added to Google Search Console. Chosen method: **DNS TXT (Domain property)** — host-independent.

### Steps given to user
1. Search Console → **Add property** → **Domain** → enter `safetycallout.com` → copy the `google-site-verification=…` TXT value.
2. At registrar DNS, add: **Type** `TXT`, **Name/Host** `@`, **Value** = the full string, **TTL** default. (Add only — don't delete existing records. Keep it permanently.)
3. Click **Verify** (allow a few min–hours for propagation).
4. After verifying: generate **`sitemap.xml` + `robots.txt`** and submit the sitemap in Search Console.

### Open items blocking completion
- **Which registrar** hosts the domain (Cloudflare / GoDaddy / Namecheap / Squarespace Domains / …) → to give exact click-path.
- **Where safetycallout.com is actually hosted** (host/repo) → needed to generate + place `sitemap.xml` and `robots.txt`.
- Whether the user has generated the verification token yet.

---

## 4. Environment gotchas
- Sandbox network policy is fixed at container boot. Higgsfield CDN egress is **blocked in this session**; enabling it requires a **fresh session**.
- GitHub access is scoped to `twandingle-cell/ct-preview` only.
- Higgsfield MCP tools available: `generate_image`, `generate_video`, `media_import_url`, `job_display`, `show_generations`, `balance`, etc.

## 5. Suggested next actions (priority order)
1. Get user's verdict on clip `441adba6`; iterate or lock it.
2. Get registrar + host for safetycallout.com → finish Search Console verification + ship sitemap/robots.
3. Host `demo/` at `safetycallout.com/demo` to activate the flyer QR.
4. (Optional) New egress-enabled session → download AI clips → stitch full polished cut via `build_video.py`.
