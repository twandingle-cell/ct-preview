"""Build the local SafetyCallout demo (9:16, ~28s) entirely from app screens +
brand cards. No network: animates tap pulses, voice waveform, progressive
transcript, captions; cross-dissolves; encodes with bundled ffmpeg + ambient bed."""
import os, math, random, shutil, subprocess
from PIL import Image, ImageDraw
import imageio_ffmpeg
from brand import INK, ORANGE, WHITE, MUTED, font, mono, text_center
import screens, cards

W, H, FPS = 1080, 1920, 24
FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()
FRAMES = "video/frames"
DISSOLVE = 6  # frames of cross-dissolve at scene starts

screens.load_photo("screens/_hazard.jpg" if os.path.exists("screens/_hazard.jpg")
                   else "screens/_placeholder_hazard.jpg")

# ---------- overlays ----------
def caption(img, text, alpha, cy):
    if not text or alpha <= 0: return
    d = ImageDraw.Draw(img, "RGBA")
    f = font(40)
    tw = d.textlength(text, font=f)
    pad_x, pad_y = 44, 26
    bx0 = W/2 - tw/2 - pad_x - 34
    box = [bx0, cy - 34, W/2 + tw/2 + pad_x, cy + 34]
    a = int(220 * alpha)
    d.rounded_rectangle(box, radius=40, fill=(8, 8, 8, a))
    # orange leading dot
    d.ellipse([bx0 + 26, cy - 12, bx0 + 50, cy + 12], fill=(ORANGE[0], ORANGE[1], ORANGE[2], int(255*alpha)))
    d.text((bx0 + 34 + 44, cy - 26), text, font=f, fill=(255, 255, 255, int(255*alpha)))

def tap_pulse(img, x, y, t, period=0.85):
    d = ImageDraw.Draw(img, "RGBA")
    phase = (t % period) / period
    r = int(40 + phase * 120)
    a = int(180 * (1 - phase))
    d.ellipse([x-r, y-r, x+r, y+r], outline=(ORANGE[0], ORANGE[1], ORANGE[2], a), width=10)
    # solid finger dot
    d.ellipse([x-34, y-34, x+34, y+34], fill=(255, 255, 255, 70))

# ---------- scenes ----------
def build_scenes():
    home = screens.screen_home()
    review = screens.screen_review(photo=screens._PHOTO)
    submit = screens.screen_review(photo=screens._PHOTO, submit=True)
    confirm = screens.screen_confirm()
    hook = cards.hook_card()
    end = cards.end_card()

    scenes = []
    scenes.append(dict(kind="static", base=hook, dur=2.4))
    scenes.append(dict(kind="static", base=home, dur=3.0,
                       cap="One tap. Then just talk.", cap_y=1560,
                       tap=(W//2, 520)))
    scenes.append(dict(kind="listen", dur=5.4,
                       cap="Describe it out loud — AI is listening.", cap_y=1780))
    scenes.append(dict(kind="static", base=review, dur=5.0,
                       cap="AI writes the OSHA-ready report.", cap_y=1700))
    scenes.append(dict(kind="static", base=submit, dur=2.2,
                       tap=(W//2, H-100)))
    scenes.append(dict(kind="static", base=confirm, dur=3.0))
    scenes.append(dict(kind="static", base=end, dur=4.6))
    return scenes

def listen_frame(t):
    random.seed(int(t * FPS) + 1)
    level = 0.45 + 0.55 * abs(math.sin(t * 5.0))
    n = min(3, int(t / 1.5) + 1) if t > 0.4 else 0
    rec = min(9, int(t / 5.4 * 9) + 1)
    return screens.screen_listen(level=level, transcript=True, transcript_n=n, rec=rec)

def render_frame(scene, t, dur):
    if scene["kind"] == "listen":
        img = listen_frame(t).convert("RGB")
    else:
        img = scene["base"].copy()
    if scene.get("tap"):
        x, y = scene["tap"]; tap_pulse(img, x, y, t)
    if scene.get("cap"):
        a = min(1.0, t / 0.35) * min(1.0, (dur - t) / 0.35 + 1)
        caption(img, scene["cap"], min(1.0, a), scene["cap_y"])
    return img

# ---------- render all frames ----------
def main():
    shutil.rmtree(FRAMES, ignore_errors=True); os.makedirs(FRAMES, exist_ok=True)
    scenes = build_scenes()
    idx = 0; prev_last = None
    for s in scenes:
        nf = int(s["dur"] * FPS)
        last = None
        for f in range(nf):
            t = f / FPS
            frame = render_frame(s, t, s["dur"])
            if prev_last is not None and f < DISSOLVE:
                frame = Image.blend(prev_last, frame, (f + 1) / (DISSOLVE + 1))
            frame.save(f"{FRAMES}/f{idx:05d}.png"); idx += 1
            last = frame
        prev_last = last
    total = idx
    print(f"{total} frames ({total/FPS:.1f}s)")

    silent = "video/_silent.mp4"
    subprocess.run([FFMPEG, "-y", "-framerate", str(FPS), "-i", f"{FRAMES}/f%05d.png",
                    "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18",
                    "-movflags", "+faststart", silent], check=True,
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    dur = total / FPS
    # ambient pad: detuned chord (A2/C3/E3), tremolo, lowpass, fades
    pad = ("sine=frequency=110:sample_rate=44100,volume=0.10[a];"
           "sine=frequency=164.81:sample_rate=44100,volume=0.07[b];"
           "sine=frequency=220:sample_rate=44100,volume=0.05[c];"
           "[a][b]amix=inputs=2[ab];[ab][c]amix=inputs=2,"
           "tremolo=f=4:d=0.3,lowpass=f=700,"
           f"afade=t=in:st=0:d=0.8,afade=t=out:st={dur-1.0:.2f}:d=1.0[out]")
    final = "video/safetycallout_demo.mp4"
    subprocess.run([FFMPEG, "-y", "-i", silent,
                    "-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo",
                    "-filter_complex", pad, "-map", "0:v", "-map", "[out]",
                    "-t", f"{dur:.2f}", "-c:v", "copy", "-c:a", "aac", "-b:a", "128k",
                    "-shortest", final], check=True,
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    os.remove(silent)
    sz = os.path.getsize(final) / 1e6
    print(f"wrote {final}  ({sz:.1f} MB, {dur:.1f}s)")

if __name__ == "__main__":
    main()
