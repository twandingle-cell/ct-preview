"""SafetyCallout brand foundation — matched to the official brand:
near-black background, vivid orange accent, 'SC' monogram, voice-first."""
from PIL import Image, ImageDraw, ImageFont

# ---- Palette (official) ----
INK       = (10, 10, 10)      # near-black background
INK_2     = (22, 22, 23)      # card / elevated surface
INK_3     = (32, 32, 34)      # inputs / wells
GLOW      = (38, 22, 12)      # dark-brown corner glow
ORANGE    = (245, 120, 32)    # primary accent  ~#F57820
ORANGE_D  = (214, 98, 22)     # pressed / deeper
WHITE     = (255, 255, 255)
MUTED     = (140, 140, 142)   # secondary text
GREEN     = (43, 191, 110)    # success
RED       = (224, 64, 48)     # alert
LINE      = (42, 42, 45)

SANS = "/usr/share/fonts/truetype/liberation/"
MONO = "/usr/share/fonts/truetype/liberation/"
DEJAVU = "/usr/share/fonts/truetype/dejavu/"

def font(size, bold=True):
    return ImageFont.truetype(SANS + ("LiberationSans-Bold.ttf" if bold else "LiberationSans-Regular.ttf"), size)

def mono(size, bold=True):
    return ImageFont.truetype(MONO + ("LiberationMono-Bold.ttf" if bold else "LiberationMono-Regular.ttf"), size)

def sym(size):
    return ImageFont.truetype(DEJAVU + "DejaVuSans.ttf", size)

def rounded(draw, box, radius, fill=None, outline=None, width=1):
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)

def text_center(draw, cx, y, s, fnt, fill):
    w = draw.textlength(s, font=fnt)
    draw.text((cx - w / 2, y), s, font=fnt, fill=fill)

def corner_glow(img, corner="tr", strength=1.0):
    """Subtle dark-brown radial glow, like the brand banner."""
    W, H = img.size
    glow = Image.new("RGB", (W, H), INK)
    gd = ImageDraw.Draw(glow)
    cx = W if "r" in corner else 0
    cy = 0 if "t" in corner else H
    maxr = int(max(W, H) * 0.9)
    for r in range(maxr, 0, -6):
        t = 1 - r / maxr
        col = tuple(int(INK[i] + (GLOW[i] - INK[i]) * (t**2) * strength) for i in range(3))
        gd.ellipse([cx-r, cy-r, cx+r, cy+r], fill=col)
    img.paste(glow, (0, 0))
    return img

def sc_mark(size):
    """Orange disc with black 'SC' monogram — the official logo mark."""
    S = size * 4
    img = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.ellipse([0, 0, S, S], fill=ORANGE)
    f = font(int(S * 0.46))
    txt = "SC"
    tw = d.textlength(txt, font=f)
    d.text((S/2 - tw/2, S*0.24), txt, font=f, fill=INK)
    return img.resize((size, size), Image.LANCZOS)

def wordmark(height=120, accent_callout=False):
    """'SafetyCallout' wordmark with SC mark. White text (brand style)."""
    icon = sc_mark(height)
    f = font(int(height * 0.60))
    s1, s2 = "Safety", "Callout"
    pad = int(height * 0.26)
    tmp = ImageDraw.Draw(Image.new("RGBA", (4, 4)))
    w1 = tmp.textlength(s1, font=f); w2 = tmp.textlength(s2, font=f)
    total_w = height + pad + int(w1 + w2)
    img = Image.new("RGBA", (total_w, height), (0, 0, 0, 0))
    img.alpha_composite(icon, (0, 0))
    d = ImageDraw.Draw(img)
    ty = int(height * 0.20)
    x = height + pad
    d.text((x, ty), s1, font=f, fill=WHITE)
    d.text((x + w1, ty), s2, font=f, fill=(ORANGE if accent_callout else WHITE))
    return img

if __name__ == "__main__":
    sc_mark(512).save("assets/icon.png")
    wordmark(160).save("assets/wordmark.png")
    wordmark(160, accent_callout=True).save("assets/wordmark_accent.png")
    card = Image.new("RGB", (1200, 360), INK)
    corner_glow(card, "tr", 1.0)
    wm = wordmark(120)
    card.paste(wm, (80, 120), wm)
    d = ImageDraw.Draw(card)
    d.text((80, 70), "// VOICE-FIRST", font=mono(34), fill=ORANGE)
    card.save("assets/_brand_check.png")
    print("brand rebuilt")
