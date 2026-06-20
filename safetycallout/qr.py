"""Branded QR code for the SafetyCallout demo, with the shield icon knocked into
the center. High error correction keeps it scannable despite the logo."""
import qrcode
from qrcode.constants import ERROR_CORRECT_H
from PIL import Image, ImageDraw
from brand import INK, YELLOW, WHITE, shield_icon
import sys

URL = sys.argv[1] if len(sys.argv) > 1 else "https://safetycallout.com/demo"

def make_qr(url, fg=INK, bg=WHITE, box=20, border=2):
    qr = qrcode.QRCode(error_correction=ERROR_CORRECT_H, box_size=box, border=border)
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color=fg, back_color=bg).convert("RGBA")
    # center logo
    w, h = img.size
    logo_s = int(w * 0.22)
    pad = int(logo_s * 0.16)
    # white rounded backing
    back = Image.new("RGBA", (logo_s + 2*pad, logo_s + 2*pad), (0,0,0,0))
    ImageDraw.Draw(back).rounded_rectangle([0,0,back.size[0]-1,back.size[1]-1],
                                           radius=int(logo_s*0.22), fill=bg)
    icon = shield_icon(logo_s)
    back.alpha_composite(icon, (pad, pad))
    img.alpha_composite(back, ((w-back.size[0])//2, (h-back.size[1])//2))
    return img

if __name__ == "__main__":
    plain = make_qr(URL)
    plain.save("assets/qr_demo.png")
    # dark-on-card version for flyer
    print("QR ->", URL, plain.size)
