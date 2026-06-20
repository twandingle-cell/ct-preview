"""Branded marketing cards: the video end-card and a flyer hero panel.
Both reuse the official brand (near-black + orange, SC monogram, voice-first)."""
from PIL import Image, ImageDraw
from brand import (font, mono, rounded, text_center, wordmark, sc_mark, corner_glow,
                   INK, INK_2, ORANGE, WHITE, MUTED, LINE)

def end_card(W=1080, H=1920, qr_path="assets/qr_demo.png"):
    img = Image.new("RGB", (W, H), INK)
    corner_glow(img, "tr", 1.0)
    d = ImageDraw.Draw(img)

    # kicker
    text_center(d, W/2, 360, "// VOICE-FIRST", mono(40), ORANGE)
    # wordmark
    wm = wordmark(118)
    img.paste(wm, (W//2 - wm.width//2, 430), wm)

    # value prop
    text_center(d, W/2, 640, "OSHA-ready reports", font(74), WHITE)
    text_center(d, W/2, 730, "in 60 seconds.", font(74), ORANGE)
    d.line([(W/2-70, 850),(W/2+70, 850)], fill=ORANGE, width=6)
    text_center(d, W/2, 900, "CALL IT OUT.   REPORT IT RIGHT.", mono(34), MUTED)

    # QR card
    qr = Image.open(qr_path).convert("RGBA")
    qs = 520
    qr = qr.resize((qs, qs))
    card_pad = 46
    cx0 = W//2 - (qs+2*card_pad)//2
    cy0 = 1070
    rounded(d, [cx0, cy0, cx0+qs+2*card_pad, cy0+qs+2*card_pad], 40, fill=WHITE)
    img.paste(qr, (cx0+card_pad, cy0+card_pad), qr)

    text_center(d, W/2, cy0+qs+2*card_pad+50, "Scan to watch the 30-second demo", font(38), WHITE)
    text_center(d, W/2, cy0+qs+2*card_pad+110, "safetycallout.com", mono(36), ORANGE)
    return img

if __name__ == "__main__":
    end_card().save("assets/end_card.png")
    print("end card written")
