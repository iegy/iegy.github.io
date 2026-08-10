# -*- coding: utf-8 -*-
"""
غلاف مشروع Easy Mo — لقطة الجهاز + اللوجو جنبها.

مختلف عن compose.py لأن ده تطبيق موبايل له لوجو، فالغلاف بيعرض
الاتنين مع بعض بدل جهازين. شغّله بعد ما تحط الملفات في screenshots/:
    screenshots/easymo-shot.jpg   لقطة التطبيق
    screenshots/easymo-logo.png   اللوجو (خلفية بيضا — بتتشال أوتوماتيك)
"""
from PIL import Image, ImageDraw, ImageFilter
import os

UP, OUT = "screenshots", "."
W, H = 2400, 1500
BEZEL, RADIUS = 14, 34
C1, C2 = "#e4f0ef", "#a9c9c6"          # تدرّج هادي مشتق من تركواز التطبيق
STATUS_BAR = 74                         # شريط الحالة اللي بيتقص من فوق


def hexrgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def gradient(size, c1, c2):
    w, h = size
    small = Image.new("RGB", (w // 8, h // 8))
    px, a, b = small.load(), hexrgb(c1), hexrgb(c2)
    sw, sh = small.size
    for y in range(sh):
        for x in range(sw):
            t = x / sw * .55 + y / sh * .45
            px[x, y] = tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))
    return small.resize((w, h), Image.BICUBIC)


def rounded(img, r):
    mask = Image.new("L", img.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, img.size[0] - 1, img.size[1] - 1], r, fill=255)
    out = img.convert("RGBA")
    out.putalpha(mask)
    return out


def device(shot, target_h):
    scr_h = target_h - BEZEL * 2
    scr_w = int(shot.width * scr_h / shot.height)
    screen = rounded(shot.resize((scr_w, scr_h), Image.LANCZOS), RADIUS - 5)
    frame = Image.new("RGBA", (scr_w + BEZEL * 2, target_h), (0, 0, 0, 0))
    frame.paste(rounded(Image.new("RGB", frame.size, (28, 25, 22)), RADIUS), (0, 0))
    frame.paste(screen, (BEZEL, BEZEL), screen)
    return frame


def shadow(size, r, blur=46, alpha=118):
    s = Image.new("RGBA", (size[0] + blur * 3, size[1] + blur * 3), (0, 0, 0, 0))
    ImageDraw.Draw(s).rounded_rectangle(
        [blur * 1.5, blur * 1.5, blur * 1.5 + size[0], blur * 1.5 + size[1]], r, fill=(20, 30, 30, alpha))
    return s.filter(ImageFilter.GaussianBlur(blur))


def dewhite(img, tol=26):
    """
    يشيل خلفية اللوجو البيضا ويخليها شفافة.

    مهم: بيمشي من الحواف لجوّه (flood fill) مش «امسح كل أبيض» —
    عشان المقص نفسه أبيض، ولو مسحنا كل الأبيض هيتخرم.
    """
    img = img.convert("RGB")
    # ٢٥٥ = خلفية فاتحة · ٠ = عناصر اللوجو
    mask = img.convert("L").point(lambda v: 255 if v > 205 else 0)
    ImageDraw.floodfill(mask, (0, 0), 128, thresh=tol)      # من الركن لجوّه
    alpha = mask.point(lambda v: 0 if v == 128 else 255)
    out = img.convert("RGBA")
    out.putalpha(alpha)
    return out.crop(out.getbbox())


shot_p = os.path.join(UP, "easymo-shot.jpg")
logo_p = os.path.join(UP, "easymo-logo.png")
assert os.path.exists(shot_p) and os.path.exists(logo_p), "الملفات مش موجودة في screenshots/"

shot = Image.open(shot_p).convert("RGB")
shot = shot.crop((0, STATUS_BAR, shot.width, shot.height))

canvas = gradient((W, H), C1, C2).convert("RGBA")
glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
ImageDraw.Draw(glow).ellipse([-460, -560, 1180, 700], fill=(255, 255, 255, 70))
canvas = Image.alpha_composite(canvas, glow.filter(ImageFilter.GaussianBlur(190)))

# الجهاز على اليمين (اتجاه القراءة العربي بيبدأ من اليمين)
dh = 1290
dev = device(shot, dh)
dx, dy = W - dev.width - 210, (H - dh) // 2
sh = shadow(dev.size, RADIUS, alpha=126)
canvas.alpha_composite(sh, (dx - (sh.width - dev.width) // 2, dy - (sh.height - dev.height) // 2 + 38))
canvas.alpha_composite(dev, (dx, dy))

# اللوجو على الشمال
logo = dewhite(Image.open(logo_p))
lw = 720
logo = logo.resize((lw, int(logo.height * lw / logo.width)), Image.LANCZOS)
lx = (dx - lw) // 2
ly = (H - logo.height) // 2
canvas.alpha_composite(logo, (max(120, lx), ly))

rgb = canvas.convert("RGB")
rgb.resize((1600, 1000), Image.LANCZOS).save(f"{OUT}/cover-easymo.webp", "WEBP", quality=88, method=6)
rgb.resize((880, 550), Image.LANCZOS).save(f"{OUT}/thumb-easymo.webp", "WEBP", quality=84, method=6)
print("✓ easymo —", os.path.getsize(f"{OUT}/cover-easymo.webp") // 1024, "KB cover,",
      os.path.getsize(f"{OUT}/thumb-easymo.webp") // 1024, "KB thumb")
