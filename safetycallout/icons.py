"""Crisp monochrome vector icons drawn with PIL (supersampled), so the app UI
never depends on emoji glyphs the system font lacks."""
from PIL import Image, ImageDraw
import math

def _canvas(size):
    S = size * 4
    img = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    return img, ImageDraw.Draw(img), S

def _fin(img, size):
    return img.resize((size, size), Image.LANCZOS)

def droplet(size, color):
    img, d, S = _canvas(size); lw = S*0.09
    cx = S/2
    top = S*0.12; by = S*0.62; r = S*0.30
    d.ellipse([cx-r, by-r, cx+r, by+r], outline=color, width=int(lw))
    d.polygon([(cx, top), (cx-r*0.95, by), (cx+r*0.95, by)], fill=color)
    d.ellipse([cx-r, by-r, cx+r, by+r], fill=color)
    return _fin(img, size)

def gear(size, color):
    img, d, S = _canvas(size); cx=cy=S/2
    R=S*0.34; teeth=8
    for i in range(teeth):
        a=math.radians(i*360/teeth)
        x=cx+math.cos(a)*R; y=cy+math.sin(a)*R
        t=S*0.10
        d.rectangle([x-t,y-t,x+t,y+t], fill=color)
    d.ellipse([cx-R*0.85,cy-R*0.85,cx+R*0.85,cy+R*0.85], fill=color)
    hole=S*0.13
    d.ellipse([cx-hole,cy-hole,cx+hole,cy+hole], fill=(0,0,0,0))
    return _fin(img, size)

def barrier(size, color):
    img, d, S = _canvas(size); lw=int(S*0.07)
    # two posts
    for px in (S*0.20, S*0.80):
        d.line([(px,S*0.30),(px,S*0.84)], fill=color, width=lw)
    # striped bar
    bar=[S*0.10, S*0.30, S*0.90, S*0.50]
    d.rectangle(bar, outline=color, width=lw)
    for i in range(4):
        x0=S*0.10+i*S*0.20
        d.line([(x0,S*0.50),(x0+S*0.12,S*0.30)], fill=color, width=int(S*0.05))
    return _fin(img, size)

def camera(size, color):
    img, d, S = _canvas(size); lw=int(S*0.07)
    body=[S*0.10,S*0.30,S*0.90,S*0.80]
    d.rounded_rectangle(body, radius=S*0.10, outline=color, width=lw)
    d.rounded_rectangle([S*0.34,S*0.20,S*0.60,S*0.33], radius=S*0.04, fill=color)
    r=S*0.17
    d.ellipse([S/2-r,S*0.55-r+S*0.02,S/2+r,S*0.55+r+S*0.02], outline=color, width=lw)
    return _fin(img, size)

def pin(size, color):
    img, d, S = _canvas(size)
    cx=S/2; cy=S*0.40; r=S*0.30
    d.pieslice([cx-r,cy-r,cx+r,cy+r], 0, 360, fill=color)
    d.polygon([(cx-r*0.78,cy+r*0.55),(cx+r*0.78,cy+r*0.55),(cx,S*0.90)], fill=color)
    hr=S*0.11
    d.ellipse([cx-hr,cy-hr,cx+hr,cy+hr], fill=(0,0,0,0))
    return _fin(img, size)

def clipboard(size, color):
    img, d, S = _canvas(size); lw=int(S*0.07)
    d.rounded_rectangle([S*0.20,S*0.18,S*0.80,S*0.86], radius=S*0.08, outline=color, width=lw)
    d.rounded_rectangle([S*0.38,S*0.12,S*0.62,S*0.26], radius=S*0.04, fill=color)
    for i in range(3):
        yy=S*0.40+i*S*0.15
        d.line([(S*0.32,yy),(S*0.68,yy)], fill=color, width=int(S*0.05))
    return _fin(img, size)

def person(size, color):
    img, d, S = _canvas(size)
    hr=S*0.16
    d.ellipse([S/2-hr,S*0.18,S/2+hr,S*0.18+2*hr], fill=color)
    d.pieslice([S*0.22,S*0.52,S*0.78,S*1.05], 180, 360, fill=color)
    return _fin(img, size)

def check(size, color):
    img, d, S = _canvas(size); lw=int(S*0.12)
    d.line([(S*0.22,S*0.52),(S*0.43,S*0.72),(S*0.80,S*0.30)], fill=color, width=lw, joint="curve")
    return _fin(img, size)

def home(size, color):
    img, d, S = _canvas(size); lw=int(S*0.07)
    d.polygon([(S/2,S*0.18),(S*0.84,S*0.48),(S*0.16,S*0.48)], fill=color)
    d.rectangle([S*0.26,S*0.46,S*0.74,S*0.82], outline=color, width=lw)
    return _fin(img, size)

def warn(size, color):
    img, d, S = _canvas(size)
    pad=S*0.10
    d.polygon([(S/2,pad),(S-pad,S-pad),(pad,S-pad)], fill=color)
    bw=S*0.08
    # punch exclamation as holes
    hole=Image.new("RGBA",(S,S),(0,0,0,0)); hd=ImageDraw.Draw(hole)
    hd.rounded_rectangle([S/2-bw/2,S*0.40,S/2+bw/2,S*0.66], radius=bw/2, fill=(0,0,0,255))
    hd.ellipse([S/2-bw/2,S*0.72,S/2+bw/2,S*0.72+bw], fill=(0,0,0,255))
    img2=Image.composite(Image.new("RGBA",(S,S),(0,0,0,0)), img, hole)
    return _fin(img2, size)

def bolt(size, color):
    img, d, S = _canvas(size)
    d.polygon([(S*0.56,S*0.12),(S*0.26,S*0.56),(S*0.46,S*0.56),
               (S*0.40,S*0.88),(S*0.74,S*0.42),(S*0.52,S*0.42)], fill=color)
    return _fin(img, size)

def mic(size, color):
    img, d, S = _canvas(size); lw=int(S*0.075)
    # capsule
    cw=S*0.30
    d.rounded_rectangle([S/2-cw/2, S*0.12, S/2+cw/2, S*0.56], radius=cw/2, fill=color)
    # cradle arc
    d.arc([S*0.26, S*0.30, S*0.74, S*0.70], 20, 160, fill=color, width=lw)
    # stand
    d.line([(S/2,S*0.70),(S/2,S*0.84)], fill=color, width=lw)
    d.line([(S*0.36,S*0.86),(S*0.64,S*0.86)], fill=color, width=lw)
    return _fin(img, size)

def doc(size, color):
    img, d, S = _canvas(size); lw=int(S*0.07)
    x0,y0,x1,y1=S*0.24,S*0.14,S*0.76,S*0.86
    fold=S*0.16
    d.polygon([(x0,y0),(x1-fold,y0),(x1,y0+fold),(x1,y1),(x0,y1)], outline=color, width=lw)
    d.line([(x1-fold,y0),(x1-fold,y0+fold),(x1,y0+fold)], fill=color, width=lw)
    for i in range(3):
        yy=S*0.42+i*S*0.14
        d.line([(x0+S*0.08,yy),(x1-S*0.08,yy)], fill=color, width=int(S*0.045))
    return _fin(img, size)

def sparkle(size, color):
    img, d, S = _canvas(size)
    def star(cx,cy,r):
        d.polygon([(cx,cy-r),(cx+r*0.28,cy-r*0.28),(cx+r,cy),(cx+r*0.28,cy+r*0.28),
                   (cx,cy+r),(cx-r*0.28,cy+r*0.28),(cx-r,cy),(cx-r*0.28,cy-r*0.28)], fill=color)
    star(S*0.46,S*0.44,S*0.30); star(S*0.74,S*0.72,S*0.15)
    return _fin(img, size)

def bell(size, color):
    img, d, S = _canvas(size); lw=int(S*0.07)
    d.pieslice([S*0.24,S*0.18,S*0.76,S*0.74], 180, 360, fill=color)
    d.rectangle([S*0.24,S*0.46,S*0.76,S*0.66], fill=color)
    d.line([(S*0.18,S*0.68),(S*0.82,S*0.68)], fill=color, width=lw)
    d.ellipse([S/2-S*0.06,S*0.70,S/2+S*0.06,S*0.82], fill=color)
    return _fin(img, size)

ICONS = dict(droplet=droplet, gear=gear, barrier=barrier, camera=camera,
             pin=pin, clipboard=clipboard, person=person, check=check,
             home=home, warn=warn, bolt=bolt, mic=mic, doc=doc,
             sparkle=sparkle, bell=bell)

def paste_icon(img, name, x, y, size, color):
    ic = ICONS[name](size, color)
    img.alpha_composite(ic.convert("RGBA"), (int(x), int(y))) if img.mode=="RGBA" else img.paste(ic,(int(x),int(y)),ic)

if __name__=="__main__":
    from brand import INK, YELLOW, WHITE
    demo=Image.new("RGB",(900,140),INK)
    for i,n in enumerate(ICONS):
        paste_icon(demo, n, 20+i*100, 30, 80, YELLOW)
    demo.save("assets/_icons_demo.png"); print("icons:", list(ICONS))
