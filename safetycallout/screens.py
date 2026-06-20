"""SafetyCallout app screens (1080x1920) — voice-first incident reporting flow.
Speak -> AI drafts an OSHA-ready report -> submit -> team notified."""
import math
from PIL import Image, ImageDraw
from brand import (font, mono, sym, rounded, text_center, wordmark, sc_mark,
                   INK, INK_2, INK_3, ORANGE, ORANGE_D, WHITE, MUTED, GREEN, RED, LINE)
from icons import paste_icon

W, H = 1080, 1920

def base():
    img = Image.new("RGB", (W, H), INK)
    return img, ImageDraw.Draw(img)

def status_bar(d):
    d.text((60, 44), "9:41", font=font(34), fill=WHITE)
    d.text((W-210, 40), "●●●", font=sym(30), fill=WHITE)
    d.rounded_rectangle([W-150, 46, W-95, 78], 7, outline=WHITE, width=3)
    d.rectangle([W-92, 54, W-86, 70], fill=WHITE)
    d.rounded_rectangle([W-145, 51, W-110, 73], 4, fill=WHITE)

def app_header(img, d, back=False):
    y = 116
    if back:
        d.text((54, y+2), "‹", font=font(74), fill=WHITE)
    wm = wordmark(54)
    img.paste(wm, (W//2 - wm.width//2, y+14), wm)
    d.line([(0, y+96), (W, y+96)], fill=LINE, width=2)

def pill(d, x, y, txt, fg, bg, fnt=None):
    fnt = fnt or font(28)
    tw = d.textlength(txt, font=fnt)
    rounded(d, [x, y, x+tw+44, y+50], 25, fill=bg)
    d.text((x+22, y+9), txt, font=fnt, fill=fg)
    return x+tw+44

def nav(img, d, active=0):
    d.rectangle([0, H-150, W, H], fill=INK_2)
    d.line([(0,H-150),(W,H-150)], fill=LINE, width=2)
    items=[("home","Home"),("clipboard","Reports"),("mic","Report"),("person","Me")]
    n=len(items)
    for i,(ic,t) in enumerate(items):
        cx=W/n*(i+0.5)
        col=ORANGE if i==active else MUTED
        paste_icon(img, ic, cx-23, H-138, 46, col)
        text_center(d, cx, H-78, t, font(24, bold=False), col)

# ---------------------------------------------------------------- HOME
def screen_home(tap=False):
    img, d = base()
    status_bar(d); app_header(img, d)
    y = 270
    d.text((60, y), "Good morning, Marcus", font=font(42), fill=WHITE)
    d.text((60, y+58), "Shift A · North Distribution Center", font=font(30, bold=False), fill=MUTED)

    by0 = y+150
    btn = [60, by0, W-60, by0+200]
    rounded(d, btn, 30, fill=ORANGE_D if tap else ORANGE)
    # mic circle
    d.ellipse([108, by0+50, 108+100, by0+150], fill=INK)
    paste_icon(img, "mic", 130, by0+70, 56, ORANGE)
    d.text((250, by0+52), "Report an Incident", font=font(50), fill=INK)
    d.text((250, by0+120), "Tap and speak — done in 60 sec", font=font(30, bold=False), fill=(40,26,10))

    ty = by0+250
    for i,(ic,t,sub) in enumerate([("bolt","Near Miss","Quick voice log"),("doc","My Reports","8 this month")]):
        tw = (W-120-20)//2
        tx0 = 60 + i*(tw+20)
        rounded(d, [tx0, ty, tx0+tw, ty+160], 24, fill=INK_2)
        paste_icon(img, ic, tx0+30, ty+30, 44, ORANGE)
        d.text((tx0+30, ty+92), t, font=font(32), fill=WHITE)

    ry = ty+210
    d.text((60, ry), "Recent activity", font=font(34), fill=WHITE)
    items=[("Spill cleaned — Aisle C","Resolved",GREEN),
           ("Forklift inspection due","Open",ORANGE)]
    for i,(t,s,col) in enumerate(items):
        cy=ry+60+i*120
        rounded(d, [60, cy, W-60, cy+100], 20, fill=INK_2)
        d.text((90, cy+30), t, font=font(31, bold=False), fill=WHITE)
        pill(d, W-260, cy+25, s, INK, col, font(26))
    nav(img, d, 0)
    return img

# ---------------------------------------------------------------- LISTEN (voice)
def waveform(d, cx, cy, level=1.0, n=27, spread=560, color=ORANGE):
    import random
    random.seed(7)
    for i in range(n):
        t = i/(n-1)
        x = cx - spread/2 + t*spread
        env = math.sin(t*math.pi)           # tall in middle
        h = (18 + env*150*level) * (0.5+random.random())
        h = max(10, min(h, 190))
        d.rounded_rectangle([x-7, cy-h/2, x+7, cy+h/2], radius=7, fill=color)

def screen_listen(level=1.0, transcript=True):
    img, d = base()
    status_bar(d); app_header(img, d, back=True)
    d.text((60, 250), "Describe what happened", font=font(46), fill=WHITE)
    d.text((60, 318), "Speak naturally — SafetyCallout listens", font=font(30, bold=False), fill=MUTED)

    # waveform
    waveform(d, W//2, 560, level=level)

    # big mic button with glow rings
    cx, cy, r = W//2, 940, 150
    for rr,alpha in [(r+70,18),(r+36,30)]:
        ring=Image.new("RGBA",(W,H),(0,0,0,0))
        ImageDraw.Draw(ring).ellipse([cx-rr,cy-rr,cx+rr,cy+rr], fill=(ORANGE[0],ORANGE[1],ORANGE[2],alpha))
        img.paste(Image.alpha_composite(img.convert("RGBA"),ring).convert("RGB"),(0,0))
        d=ImageDraw.Draw(img)
    d.ellipse([cx-r, cy-r, cx+r, cy+r], fill=ORANGE)
    paste_icon(img, "mic", cx-58, cy-66, 116, INK)
    # timer
    pill(d, cx-95, cy+r+40, "● REC  0:09", WHITE, INK_2, mono(32))

    if transcript:
        ty=cy+r+150
        rounded(d, [60, ty, W-60, ty+260], 24, fill=INK_2)
        paste_icon(img, "sparkle", 90, ty+30, 40, ORANGE)
        d.text((150, ty+34), "Live transcript", font=mono(28), fill=ORANGE)
        quote=['"There’s a liquid spill by the racking',
               'in Aisle B, Rack 12 — someone could',
               'slip. Medium severity, taping it off now."']
        for i,l in enumerate(quote):
            d.text((90, ty+96+i*50), l, font=font(31, bold=False), fill=WHITE)
    return img

# ---------------------------------------------------------------- AI REVIEW
def screen_review(photo=None, submit=False, pressed=False):
    img, d = base()
    status_bar(d); app_header(img, d, back=True)
    paste_icon(img, "sparkle", 60, 238, 44, ORANGE)
    d.text((120, 244), "AI-drafted from your voice note", font=mono(30), fill=ORANGE)
    d.text((60, 308), "Slip, Trip & Fall", font=font(50), fill=WHITE)
    pill(d, 60, 384, "OSHA-ready", INK, ORANGE, font(28))
    pill(d, 290, 384, "Auto-filled", WHITE, INK_2, font(28))

    # photo
    py=470
    pbox=[60, py, W-60, py+470]
    rounded(d, pbox, 24, fill=INK_2)
    if photo is not None:
        ph=photo.resize((W-124, 466))
        m=Image.new("L", ph.size, 0)
        ImageDraw.Draw(m).rounded_rectangle([0,0,ph.size[0],ph.size[1]],22,fill=255)
        img.paste(ph,(62,py+2),m)
        rounded(d,[90,py+390,372,py+448],18,fill=(0,0,0))
        paste_icon(img,"camera",112,py+400,38,WHITE)
        d.text((164,py+400),"Photo attached",font=font(28),fill=WHITE)
    else:
        paste_icon(img,"camera",W//2-150,py+200,56,MUTED)
        d.text((W//2-80,py+208),"Add photo",font=font(40),fill=MUTED)

    # fields
    fy=py+510
    def field(label, value, icon, y):
        d.text((60, y), label, font=font(28, bold=False), fill=MUTED)
        rounded(d, [60, y+44, W-60, y+128], 18, fill=INK_2)
        paste_icon(img, icon, 92, y+62, 44, ORANGE)
        d.text((160, y+66), value, font=font(34), fill=WHITE)
    field("Location", "Aisle B · Rack 12", "pin", fy)
    # severity row
    sy=fy+170
    d.text((60, sy), "Severity", font=font(28, bold=False), fill=MUTED)
    x=60
    for i,(t,col) in enumerate([("Low",INK_3),("Medium",ORANGE),("High",RED)]):
        sel=(i==1)
        tw=d.textlength(t,font=font(32)); bw=tw+70
        rounded(d,[x,sy+44,x+bw,sy+116],22, fill=col if sel else INK_2, outline=col, width=3)
        d.text((x+35,sy+60),t,font=font(32),fill=INK if sel else WHITE)
        x+=bw+22

    if submit:
        d.rectangle([0,H-200,W,H], fill=INK)
        d.line([(0,H-200),(W,H-200)], fill=LINE, width=2)
        btn=[60,H-160,W-60,H-40]
        rounded(d, btn, 28, fill=ORANGE_D if pressed else ORANGE)
        text_center(d, W//2, H-130, "Submit OSHA Report", font(44), INK)
    return img

# ---------------------------------------------------------------- CONFIRM
def screen_confirm():
    img, d = base()
    status_bar(d)
    cy=560
    d.ellipse([W//2-150, cy-150, W//2+150, cy+150], fill=GREEN)
    paste_icon(img, "check", W//2-95, cy-95, 190, WHITE)
    text_center(d, W//2, cy+200, "Incident reported", font(62), WHITE)
    text_center(d, W//2, cy+286, "Safety team notified in real time.", font(34, bold=False), MUTED)

    ky=cy+390
    rounded(d, [110, ky, W-110, ky+360], 28, fill=INK_2)
    d.text((160, ky+38), "Report ID", font=font(28, bold=False), fill=MUTED)
    d.text((160, ky+76), "SC-4827", font=font(50), fill=ORANGE)
    d.line([(160,ky+162),(W-160,ky+162)], fill=LINE, width=2)
    paste_icon(img, "pin", 160, ky+182, 40, ORANGE)
    d.text((214, ky+184), "Aisle B · Rack 12", font=font(32, bold=False), fill=WHITE)
    paste_icon(img, "doc", 160, ky+258, 44, ORANGE)
    d.text((220, ky+264), "OSHA-ready PDF generated", font=font(31, bold=False), fill=WHITE)
    pill(d, W-360, ky+262, "Ready", INK, GREEN, font(26))

    btn=[60,H-160,W-60,H-40]
    rounded(d, btn, 28, fill=ORANGE)
    text_center(d, W//2, H-130, "Done", font(44), INK)
    return img

_PHOTO=None
def load_photo(path):
    global _PHOTO
    _PHOTO=Image.open(path).convert("RGB")

if __name__=="__main__":
    import os
    os.makedirs("screens", exist_ok=True)
    ph=Image.new("RGB",(900,470),(60,62,66))
    pd=ImageDraw.Draw(ph); pd.ellipse([300,250,620,430],fill=(110,115,125))
    ph.save("screens/_placeholder_hazard.jpg"); load_photo("screens/_placeholder_hazard.jpg")
    screen_home().save("screens/01_home.png")
    screen_home(tap=True).save("screens/01_home_tap.png")
    screen_listen(level=1.0).save("screens/02_listen.png")
    screen_listen(level=0.4).save("screens/02_listen_low.png")
    screen_review(photo=_PHOTO).save("screens/03_review.png")
    screen_review(photo=_PHOTO, submit=True).save("screens/04_submit.png")
    screen_review(photo=_PHOTO, submit=True, pressed=True).save("screens/04_submit_tap.png")
    screen_confirm().save("screens/05_confirm.png")
    print("screens written")
