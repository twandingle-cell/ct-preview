"""Draw a stylized but credible 'phone photo' of a warehouse spill hazard,
fully local (no AI/network). Saved as screens/_hazard.jpg for the review screen."""
import random, math
from PIL import Image, ImageDraw, ImageFilter

W, H = 980, 480
random.seed(11)

img = Image.new("RGB", (W, H), (66, 68, 72))
d = ImageDraw.Draw(img)

# concrete floor — vertical gradient + speckle noise
for y in range(H):
    t = y / H
    c = int(74 - 22 * t)
    d.line([(0, y), (W, y)], fill=(c, c+2, c+5))
for _ in range(9000):
    x, y = random.randint(0, W-1), random.randint(0, H-1)
    g = random.randint(-14, 14)
    px = img.getpixel((x, y))
    img.putpixel((x, y), tuple(max(0, min(255, p+g)) for p in px))
d = ImageDraw.Draw(img)

# expansion joints (floor seams) in perspective
d.line([(W*0.0, H*0.78), (W*1.0, H*0.66)], fill=(48,50,54), width=4)
d.line([(W*0.46, H*1.0), (W*0.54, H*0.5)], fill=(48,50,54), width=4)

# metal rack uprights (left & right), orange-ish foot plates
for bx, side in [(40, 1), (W-95, -1)]:
    d.rectangle([bx, 0, bx+55, H], fill=(40, 42, 47))
    d.rectangle([bx+(0 if side>0 else 40), 0, bx+(15 if side>0 else 55), H], fill=(54,56,61))
    for hy in range(20, H, 46):
        d.ellipse([bx+22, hy, bx+34, hy+12], fill=(28,29,32))
    # orange base bracket
    d.rectangle([bx-6, H-70, bx+62, H-40], fill=(196, 92, 26))
    # a stacked pallet/box hint at top
    d.rectangle([bx-10, 0, bx+66, 70], fill=(120, 96, 64))
    d.rectangle([bx-10, 70, bx+66, 78], fill=(150, 120, 80))

# the spill — glossy dark puddle, lower-center
cx, cy = int(W*0.52), int(H*0.74)
puddle = Image.new("L", (W, H), 0)
pd = ImageDraw.Draw(puddle)
for dx, dy, rx, ry in [(0,0,180,78),(-120,-18,90,42),(150,10,80,40),(40,40,120,46),(-60,38,70,30)]:
    pd.ellipse([cx+dx-rx, cy+dy-ry, cx+dx+rx, cy+dy+ry], fill=255)
puddle = puddle.filter(ImageFilter.GaussianBlur(6))
# dark wet fill that reflects the dim ceiling (blue-grey sheen)
wet = Image.new("RGB", (W, H), (30, 34, 42))
wd = ImageDraw.Draw(wet)
for y in range(H):
    t = y / H
    wd.line([(0,y),(W,y)], fill=(int(26+30*(1-t)), int(30+32*(1-t)), int(40+34*(1-t))))
img.paste(wet, (0,0), puddle)
d = ImageDraw.Draw(img)
# specular highlights on the wet surface
hi = Image.new("L", (W, H), 0)
hd = ImageDraw.Draw(hi)
hd.ellipse([cx-150, cy-40, cx+10, cy-10], fill=120)
hd.ellipse([cx+30, cy+10, cx+150, cy+34], fill=80)
hi = hi.filter(ImageFilter.GaussianBlur(9))
white = Image.new("RGB", (W,H), (210, 216, 224))
img.paste(white, (0,0), Image.composite(hi, Image.new("L",(W,H),0), puddle))
d = ImageDraw.Draw(img)
# bright rim where puddle meets dry floor
rim = puddle.filter(ImageFilter.MaxFilter(7))
rim = Image.composite(Image.new("L",(W,H),90),
                      Image.new("L",(W,H),0),
                      Image.eval(rim, lambda v: 255 if 40 < v < 130 else 0))
img.paste(Image.new("RGB",(W,H),(150,156,164)), (0,0), rim.filter(ImageFilter.GaussianBlur(1)))
d = ImageDraw.Draw(img)

# yellow caution A-frame sign to the right of the spill
sx, sy = int(W*0.74), int(H*0.40)
d.polygon([(sx, sy), (sx-46, sy+150), (sx+46, sy+150)], fill=(240, 196, 28))
d.polygon([(sx, sy+6), (sx-38, sy+146), (sx+38, sy+146)], fill=(248, 208, 40))
# little figure-slipping glyph
d.line([(sx-12, sy+58),(sx+12, sy+86)], fill=(30,30,30), width=6)
d.ellipse([sx-4, sy+44, sx+12, sy+60], fill=(30,30,30))
d.line([(sx-22, sy+96),(sx+22, sy+96)], fill=(30,30,30), width=5)

# vignette
vig = Image.new("L", (W, H), 0)
vd = ImageDraw.Draw(vig)
vd.ellipse([-W*0.2, -H*0.2, W*1.2, H*1.2], fill=255)
vig = vig.filter(ImageFilter.GaussianBlur(120))
dark = Image.new("RGB", (W, H), (0,0,0))
img = Image.composite(img, dark, vig)

img = img.filter(ImageFilter.GaussianBlur(0.4))
img.save("screens/_hazard.jpg", quality=88)
print("hazard photo written: screens/_hazard.jpg")
