"""SafetyCallout brand foundation: palette, fonts, and reusable draw helpers."""
from PIL import Image, ImageDraw, ImageFont

# ---- Palette (Hi-vis safety) ----
INK       = (26, 26, 26)      # charcoal background
INK_2     = (34, 34, 36)      # card / elevated surface
INK_3     = (48, 48, 51)      # hairlines / inputs
YELLOW    = (255, 193, 7)     # safety yellow (primary accent)
AMBER     = (255, 159, 10)    # secondary accent
WHITE     = (255, 255, 255)
MUTED     = (165, 167, 170)   # secondary text
GREEN     = (34, 197, 94)     # success
RED       = (220, 38, 38)     # alert
LINE      = (60, 60, 64)

FONT_DIR = "/usr/share/fonts/truetype/liberation/"
DEJAVU   = "/usr/share/fonts/truetype/dejavu/"

def font(size, bold=True):
    path = FONT_DIR + ("LiberationSans-Bold.ttf" if bold else "LiberationSans-Regular.ttf")
    return ImageFont.truetype(path, size)

def sym(size):
    """DejaVu Sans for glyphs/symbols (checkmarks, arrows, etc.)."""
    return ImageFont.truetype(DEJAVU + "DejaVuSans.ttf", size)

def rounded(draw, box, radius, fill=None, outline=None, width=1):
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)

def text_center(draw, cx, y, s, fnt, fill):
    w = draw.textlength(s, font=fnt)
    draw.text((cx - w / 2, y), s, font=fnt, fill=fill)

def shield_icon(size, fg=INK, bg=YELLOW):
    """A rounded shield with a megaphone/callout mark — the SafetyCallout icon."""
    S = size * 4  # supersample
    img = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    m = S * 0.10
    # shield outline path approximated with polygon + arcs
    w = S - 2 * m
    top = m
    pts = [
        (S/2, top),
        (S - m, top + w*0.18),
        (S - m, top + w*0.52),
        (S/2, S - m),
        (m, top + w*0.52),
        (m, top + w*0.18),
    ]
    d.polygon(pts, fill=bg)
    # megaphone / callout glyph in center
    cx, cy = S/2, S*0.46
    # speech bubble
    bw, bh = w*0.46, w*0.30
    bx0, by0 = cx - bw/2, cy - bh/2
    d.rounded_rectangle([bx0, by0, bx0+bw, by0+bh], radius=bh*0.28, fill=fg)
    # bubble tail
    d.polygon([(bx0+bw*0.30, by0+bh), (bx0+bw*0.30, by0+bh+bh*0.34), (bx0+bw*0.56, by0+bh)], fill=fg)
    # exclamation in bubble
    ed = ImageDraw.Draw(img)
    bar_w = bw*0.09
    ed.rounded_rectangle([cx-bar_w/2, by0+bh*0.22, cx+bar_w/2, by0+bh*0.58], radius=bar_w/2, fill=bg)
    ed.ellipse([cx-bar_w/2, by0+bh*0.66, cx+bar_w/2, by0+bh*0.66+bar_w], fill=bg)
    return img.resize((size, size), Image.LANCZOS)

def wordmark(height=120, on_dark=True):
    """'SafetyCallout' wordmark with icon. Returns RGBA image sized to height."""
    icon_s = height
    icon = shield_icon(icon_s)
    f1 = font(int(height*0.62), bold=True)
    txt_safety = "Safety"
    txt_callout = "Callout"
    pad = int(height*0.22)
    tmp = Image.new("RGBA", (10, 10))
    td = ImageDraw.Draw(tmp)
    w_s = td.textlength(txt_safety, font=f1)
    w_c = td.textlength(txt_callout, font=f1)
    total_w = icon_s + pad + int(w_s + w_c) + int(height*0.05)
    img = Image.new("RGBA", (total_w, height), (0, 0, 0, 0))
    img.alpha_composite(icon, (0, 0))
    d = ImageDraw.Draw(img)
    ty = int(height*0.20)
    base = WHITE if on_dark else INK
    x = icon_s + pad
    d.text((x, ty), txt_safety, font=f1, fill=base)
    d.text((x + w_s, ty), txt_callout, font=f1, fill=YELLOW)
    return img

if __name__ == "__main__":
    wordmark(160).save("assets/wordmark.png")
    shield_icon(512).save("assets/icon.png")
    # light version for flyer
    wordmark(160, on_dark=False).save("assets/wordmark_dark.png")
    print("brand assets written")
