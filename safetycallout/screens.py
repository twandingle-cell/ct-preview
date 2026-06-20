"""SafetyCallout app screens, rendered full-frame 1080x1920 for the demo video."""
from PIL import Image, ImageDraw
from brand import (font, sym, rounded, text_center, wordmark, shield_icon,
                   INK, INK_2, INK_3, YELLOW, AMBER, WHITE, MUTED, GREEN, RED, LINE)
from icons import paste_icon

W, H = 1080, 1920

def base():
    img = Image.new("RGB", (W, H), INK)
    d = ImageDraw.Draw(img)
    return img, d

def status_bar(d, dark_text=False):
    c = INK if dark_text else WHITE
    d.text((60, 44), "9:41", font=font(34), fill=c)
    # signal / wifi / battery (simple glyphs)
    d.text((W-210, 40), "●●●", font=sym(30), fill=c)
    rounded(d, [W-150, 46, W-95, 78], 7, outline=c, width=3)
    d.rectangle([W-92, 54, W-86, 70], fill=c)
    d.rounded_rectangle([W-145, 51, W-110, 73], 4, fill=c)

def app_header(img, d, title=None, back=False):
    y = 118
    if back:
        d.text((56, y+6), "‹", font=font(72), fill=WHITE)
    wm = wordmark(58)
    img.paste(wm, (W//2 - wm.width//2, y+14), wm)
    d.line([(0, y+96), (W, y+96)], fill=LINE, width=2)

def pill(d, x, y, txt, fg, bg, fnt=None):
    fnt = fnt or font(30)
    tw = d.textlength(txt, font=fnt)
    rounded(d, [x, y, x+tw+44, y+52], 26, fill=bg)
    d.text((x+22, y+10), txt, font=fnt, fill=fg)
    return x+tw+44

# ---------------------------------------------------------------- HOME
def screen_home(tap=False):
    img, d = base()
    status_bar(d)
    app_header(img, d)
    y = 280
    d.text((60, y), "Good morning, Marcus", font=font(40), fill=WHITE)
    d.text((60, y+58), "Shift A · North Distribution Center", font=font(30, bold=False), fill=MUTED)

    # primary CTA
    by0 = y+150
    btn = [60, by0, W-60, by0+170]
    rounded(d, btn, 28, fill=YELLOW)
    if tap:
        rounded(d, btn, 28, fill=AMBER)
    paste_icon(img, "warn", 104, by0+42, 86, INK)
    d.text((220, by0+34), "Report an Incident", font=font(50), fill=INK)
    d.text((220, by0+100), "Takes about 30 seconds", font=font(30, bold=False), fill=(60,55,20))

    # secondary tiles
    ty = by0+220
    for i,(t,sub) in enumerate([("Near Miss","Quick log"),("My Reports","8 this month")]):
        tx0 = 60 + i*( (W-120)//2 + 20 )
        tw = (W-120-20)//2
        rounded(d, [tx0, ty, tx0+tw, ty+150], 24, fill=INK_2)
        d.text((tx0+30, ty+30), t, font=font(34), fill=WHITE)
        d.text((tx0+30, ty+82), sub, font=font(28, bold=False), fill=MUTED)

    # recent
    ry = ty+200
    d.text((60, ry), "Recent activity", font=font(34), fill=WHITE)
    items = [("Spill cleaned — Aisle C","Resolved", GREEN),
             ("Forklift inspection due","Open", AMBER)]
    for i,(t,s,col) in enumerate(items):
        cy = ry+60 + i*120
        rounded(d, [60, cy, W-60, cy+100], 20, fill=INK_2)
        d.text((90, cy+30), t, font=font(32, bold=False), fill=WHITE)
        pill(d, W-260, cy+24, s, INK, col, font(26))
    nav(img, d, 0)
    return img

# ---------------------------------------------------------------- TYPE
TYPES = [
    ("warn",    "Slip, Trip & Fall",     "Wet floor, obstruction, uneven surface"),
    ("droplet", "Spill / Leak",          "Liquid, chemical, oil"),
    ("gear",    "Equipment / Machinery", "Forklift, conveyor, damage"),
    ("bolt",    "Fire / Electrical",     "Sparks, exposed wiring, heat"),
    ("barrier", "Blocked Exit / Access", "Aisle, fire door, egress"),
]
def screen_type(selected=0, tap=False):
    img, d = base()
    status_bar(d)
    app_header(img, d, back=True)
    d.text((60, 270), "What happened?", font=font(48), fill=WHITE)
    d.text((60, 336), "Select the type of hazard", font=font(30, bold=False), fill=MUTED)
    y = 420
    for i,(ic,t,sub) in enumerate(TYPES):
        cy = y + i*180
        sel = (i==selected)
        box = [60, cy, W-60, cy+150]
        if sel:
            rounded(d, box, 24, fill=INK_2, outline=YELLOW, width=5)
        else:
            rounded(d, box, 24, fill=INK_2)
        paste_icon(img, ic, 92, cy+43, 64, YELLOW if sel else WHITE)
        d.text((200, cy+34), t, font=font(38), fill=WHITE)
        d.text((200, cy+90), sub, font=font(27, bold=False), fill=MUTED)
        if sel:
            d.ellipse([W-150, cy+50, W-100, cy+100], fill=YELLOW)
            paste_icon(img, "check", W-141, cy+54, 42, INK)
    return img

# ---------------------------------------------------------------- DETAILS
def screen_details(photo=None, filled=True, tap=False):
    img, d = base()
    status_bar(d)
    app_header(img, d, back=True)
    d.text((60, 250), "Slip, Trip & Fall", font=font(44), fill=WHITE)
    pill(d, 60, 322, "Step 2 of 3", YELLOW, INK_2, font(26))

    # photo field
    py = 410
    d.text((60, py), "Photo evidence", font=font(32), fill=WHITE)
    pbox = [60, py+50, W-60, py+50+520]
    rounded(d, pbox, 24, fill=INK_2)
    if photo is not None and filled:
        ph = photo.resize((W-124, 516))
        m = Image.new("L", ph.size, 0)
        ImageDraw.Draw(m).rounded_rectangle([0,0,ph.size[0],ph.size[1]], 22, fill=255)
        img.paste(ph, (62, py+52), m)
        # tag
        rounded(d, [90, py+50+440, 372, py+50+500], 18, fill=(0,0,0))
        paste_icon(img, "camera", 112, py+50+452, 38, WHITE)
        d.text((164, py+50+452), "Photo added", font=font(28), fill=WHITE)
    else:
        paste_icon(img, "camera", W//2-150, py+250, 56, MUTED)
        d.text((W//2-80, py+258), "Add photo", font=font(40), fill=MUTED)

    # location field
    ly = py+50+560
    d.text((60, ly), "Location", font=font(32), fill=WHITE)
    rounded(d, [60, ly+50, W-60, ly+140], 20, fill=INK_2, outline=YELLOW if tap else LINE, width=3 if tap else 2)
    paste_icon(img, "pin", 96, ly+72, 46, YELLOW)
    loc = "Aisle B · Rack 12" if filled else "Tap to set location…"
    d.text((164, ly+80), loc, font=font(36, bold=not False), fill=WHITE if filled else MUTED)

    # severity
    sy = ly+190
    d.text((60, sy), "Severity", font=font(32), fill=WHITE)
    labels=[("Low",INK_3),("Medium",AMBER),("High",RED)]
    x=60
    for i,(t,col) in enumerate(labels):
        sel = (i==1 and filled)
        tw=d.textlength(t,font=font(32))
        bw=tw+70
        rounded(d,[x,sy+50,x+bw,sy+120],22, fill=col if sel else INK_2, outline=col, width=3)
        d.text((x+35,sy+66),t,font=font(32),fill=INK if sel else WHITE)
        x+=bw+24
    return img

# ---------------------------------------------------------------- SUBMIT
def screen_submit(pressed=False):
    img = screen_details(photo=_PHOTO, filled=True)
    d = ImageDraw.Draw(img)
    # bottom submit bar
    d.rectangle([0, H-200, W, H], fill=INK)
    d.line([(0,H-200),(W,H-200)], fill=LINE, width=2)
    btn=[60, H-160, W-60, H-40]
    rounded(d, btn, 28, fill=AMBER if pressed else YELLOW)
    text_center(d, W//2, H-128, "Submit Report", font(46), INK)
    return img

# ---------------------------------------------------------------- CONFIRM
def screen_confirm():
    img, d = base()
    status_bar(d)
    # green wash top
    cy=620
    d.ellipse([W//2-150, cy-150, W//2+150, cy+150], fill=GREEN)
    d.text((W//2-78, cy-110), "✓", font=sym(170), fill=WHITE)
    text_center(d, W//2, cy+200, "Incident reported", font(64), WHITE)
    text_center(d, W//2, cy+290, "Your safety team has been", font(38, bold=False), MUTED)
    text_center(d, W//2, cy+340, "notified in real time.", font(38, bold=False), MUTED)

    # ticket card
    ky=cy+440
    rounded(d, [120, ky, W-120, ky+260], 28, fill=INK_2)
    d.text((170, ky+40), "Report ID", font=font(30, bold=False), fill=MUTED)
    d.text((170, ky+80), "SC-4827", font=font(52), fill=YELLOW)
    d.line([(170,ky+170),(W-170,ky+170)], fill=LINE, width=2)
    paste_icon(img, "pin", 170, ky+188, 40, YELLOW)
    d.text((224, ky+190), "Aisle B · Rack 12", font=font(32, bold=False), fill=WHITE)
    pill(d, W-360, ky+186, "Notified", INK, GREEN, font(28))

    btn=[60, H-160, W-60, H-40]
    rounded(d, btn, 28, fill=YELLOW)
    text_center(d, W//2, H-128, "Done", font(46), INK)
    return img

# ---------------------------------------------------------------- bottom nav
def nav(img, d, active=0):
    d.rectangle([0, H-150, W, H], fill=INK_2)
    d.line([(0,H-150),(W,H-150)], fill=LINE, width=2)
    items=[("home","Home"),("clipboard","Reports"),("warn","Report"),("person","Me")]
    n=len(items)
    for i,(ic,t) in enumerate(items):
        cx=W/n*(i+0.5)
        col=YELLOW if i==active else MUTED
        paste_icon(img, ic, cx-23, H-138, 46, col)
        text_center(d, cx, H-78, t, font(24, bold=False), col)

_PHOTO=None
def load_photo(path):
    global _PHOTO
    _PHOTO=Image.open(path).convert("RGB")

if __name__=="__main__":
    import os
    os.makedirs("screens", exist_ok=True)
    # placeholder hazard photo until AI photo is ready
    ph=Image.new("RGB",(800,520),(70,72,75))
    pd=ImageDraw.Draw(ph)
    pd.ellipse([250,300,560,470], fill=(120,125,135))
    ph.save("screens/_placeholder_hazard.jpg")
    load_photo("screens/_placeholder_hazard.jpg")
    screen_home().save("screens/01_home.png")
    screen_home(tap=True).save("screens/01_home_tap.png")
    screen_type(selected=0).save("screens/02_type.png")
    screen_details(photo=_PHOTO, filled=True).save("screens/03_details.png")
    screen_submit().save("screens/04_submit.png")
    screen_submit(pressed=True).save("screens/04_submit_tap.png")
    screen_confirm().save("screens/05_confirm.png")
    print("screens written")
