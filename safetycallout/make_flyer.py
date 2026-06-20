"""Print-ready SafetyCallout flyer (US Letter portrait, ~200dpi) with the
scannable QR, phone mockup, and brand voice-first messaging. Outputs PNG + PDF."""
from PIL import Image, ImageDraw, ImageFilter
from brand import (font, mono, rounded, text_center, wordmark, sc_mark, corner_glow,
                   INK, INK_2, ORANGE, WHITE, MUTED, GREEN, LINE)
from icons import paste_icon

W, H = 1700, 2200
M = 120

img = Image.new("RGB", (W, H), INK)
corner_glow(img, "tr", 1.0)
d = ImageDraw.Draw(img)

# ---- header ----
d.text((M, M-10), "// VOICE-FIRST INCIDENT REPORTING", font=mono(34), fill=ORANGE)
wm = wordmark(96)
img.paste(wm, (M, M+44), wm)

# ---- hero headline ----
d.text((M, 360), "Call it out.", font=font(150), fill=WHITE)
d.text((M, 520), "Report it right.", font=font(150), fill=ORANGE)
d.text((M, 720), "Voice-first hazard reporting for warehouse", font=font(44, bold=False), fill=MUTED)
d.text((M, 778), "& distribution teams — no typing, no paperwork.", font=font(44, bold=False), fill=MUTED)

# ---- middle band: features (left) + phone (right) ----
feats = [
    ("mic",     "Just speak",           "Describe the hazard out loud, hands-free."),
    ("sparkle", "AI does the writing",  "It drafts a complete, OSHA-ready report."),
    ("bell",    "Team notified instantly","Submit and the safety team knows in seconds."),
]
fy = 920
for ic, t, s in feats:
    rounded(d, [M-30, fy-30, M+760, fy+150], 26, fill=INK_2)
    d.ellipse([M, fy, M+96, fy+96], fill=INK)
    paste_icon(img, ic, M+24, fy+24, 48, ORANGE)
    d.text((M+140, fy+6), t, font=font(48), fill=WHITE)
    d.text((M+140, fy+70), s, font=font(34, bold=False), fill=MUTED)
    fy += 220

# phone mockup (listen screen) on the right
phone = Image.open("screens/02_listen.png").convert("RGB")
pw = 440
ph = int(pw * phone.height / phone.width)
phone = phone.resize((pw, ph))
mask = Image.new("L", (pw, ph), 0)
ImageDraw.Draw(mask).rounded_rectangle([0, 0, pw, ph], 54, fill=255)
px, py = W - M - pw, 905
# shadow
shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
ImageDraw.Draw(shadow).rounded_rectangle([px-14, py+10, px+pw+14, py+ph+22], 64, fill=(0, 0, 0, 150))
img.paste(Image.alpha_composite(img.convert("RGBA"), shadow.filter(ImageFilter.GaussianBlur(22))).convert("RGB"), (0, 0))
d = ImageDraw.Draw(img)
# bezel + screen
rounded(d, [px-12, py-12, px+pw+12, py+ph+12], 62, fill=(0, 0, 0), outline=(50, 50, 54), width=3)
img.paste(phone, (px, py), mask)
d = ImageDraw.Draw(img)

# ---- QR call-to-action card ----
qy0 = 1620
rounded(d, [M-30, qy0, W-M+30, qy0+430], 36, fill=INK_2, outline=ORANGE, width=4)
qr = Image.open("assets/qr_demo.png").convert("RGBA")
qs = 360
qr = qr.resize((qs, qs))
rounded(d, [M+10, qy0+35, M+10+qs+40, qy0+35+qs+40], 28, fill=WHITE)
img.paste(qr, (M+30, qy0+55), qr)
tx = M + qs + 110
d.text((tx, qy0+70), "Scan to watch the", font=font(64), fill=WHITE)
d.text((tx, qy0+150), "30-second demo", font=font(64), fill=ORANGE)
d.text((tx, qy0+260), "See a supervisor report a hazard,", font=font(38, bold=False), fill=MUTED)
d.text((tx, qy0+312), "hands-free, in real time.", font=font(38, bold=False), fill=MUTED)

# ---- footer ----
d.line([(M, H-150), (W-M, H-150)], fill=LINE, width=2)
d.text((M, H-118), "OSHA-ready reports in 60 seconds.", font=font(40), fill=WHITE)
url = "safetycallout.com"; uf = mono(38)
uw = d.textlength(url, font=uf)
d.text((W - M - uw, H-116), url, font=uf, fill=ORANGE)
sm = sc_mark(52); img.paste(sm, (int(W - M - uw - 72), H-124), sm)

img.save("assets/flyer.png")
img.convert("RGB").save("assets/flyer.pdf", "PDF", resolution=200.0)
print("flyer written: assets/flyer.png + assets/flyer.pdf", img.size)
