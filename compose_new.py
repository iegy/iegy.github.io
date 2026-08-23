# -*- coding: utf-8 -*-
"""
أغلفة المشاريع الجديدة — ذِكري (٣ شاشات موبايل) وقاهر الطريق (شاشتين ويب).

نفس أسلوب compose.py بالظبط: إطار جهاز داكن على خلفية متدرجة بألوان
مشتقة من هوية كل مشروع. حط اللقطات الخام في screenshots/ وشغّل:

    python3 compose_new.py
"""
from PIL import Image, ImageDraw, ImageFilter
import os

UP, OUT = "screenshots", "."
W, H = 2400, 1500
BEZEL, RADIUS = 14, 34

# slug: (تدرّج, [(ملف, قص من فوق, قص من تحت)], نوع الترتيب)
JOBS = {
    # ذِكري: تلات شاشات موبايل — داكنة في النص وفاتحتين على الجناحين
    "dhikri": (("#f0ead9", "#b9a260"), [
        ("dhikri-home.jpg",   96, 30),   # الرئيسية (داكن)
        ("dhikri-adhkar.jpg", 96, 30),   # الأذكار (فاتح)
        ("dhikri-prayer.jpg", 96, 30),   # المواقيت (داكن)
    ], "phones3"),

    # قاهر الطريق: شاشتين ويب — الهيرو العربي والشهادات الإنجليزي
    "qaher": (("#e6e9ef", "#8f9bb0"), [
        ("qaher-hero.png",  0, 0),
        ("qaher-certs.png", 0, 0),
    ], "web2"),

    # Omega Care: شاشتين ويب — لقطات متصفح كاملة، بنقص شريط كروم فوق وشريط المهام تحت
    "omegacare": (("#1c1147", "#6c3fa8"), [
        ("omegacare-hero.png", 128, 42),
        ("omegacare-lab.png",  128, 42),
    ], "web2"),

    # الحمد للفحم: شاشتين ويب — هوية داكنة فحمية بلمسة ذهبية
    "alhamd": (("#14100c", "#caa15a"), [
        ("alhamd-hero.png", 128, 42),
        ("alhamd-map.png",  128, 42),
    ], "web2"),

    # Kallista: شاشتين ويب — هوية فاتحة كريمية بلمسة ذهبية هادئة
    "kallista": (("#eef0e6", "#8e9b7a"), [
        ("kallista-hero.png",    128, 42),
        ("kallista-gallery.png", 128, 42),
    ], "web2"),

    # رِفق: شاشة موبايل واحدة — تدرّج تركوازي دافئ يطابق هوية التطبيق
    "rifq": (("#f3ede0", "#4a9e94"), [
        ("rifq-home.jpg", 0, 0),
    ], "phone1"),
}


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
        [blur * 1.5, blur * 1.5, blur * 1.5 + size[0], blur * 1.5 + size[1]], r, fill=(24, 20, 14, alpha))
    return s.filter(ImageFilter.GaussianBlur(blur))


def place(canvas, img, x, y, alpha):
    sh = shadow(img.size, RADIUS, alpha=alpha)
    canvas.alpha_composite(sh, (x - (sh.width - img.width) // 2,
                                y - (sh.height - img.height) // 2 + 36))
    canvas.alpha_composite(img, (x, y))


for slug, (colors, shots, layout) in JOBS.items():
    src = []
    for fname, top, bot in shots:
        p = os.path.join(UP, fname)
        if not os.path.exists(p):
            print("!! ناقص:", fname)
            continue
        im = Image.open(p).convert("RGB")
        src.append(im.crop((0, top, im.width, im.height - bot)))
    if not src:
        continue

    canvas = gradient((W, H), *colors).convert("RGBA")
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(glow).ellipse([-460, -560, 1180, 700], fill=(255, 255, 255, 66))
    canvas = Image.alpha_composite(canvas, glow.filter(ImageFilter.GaussianBlur(190)))

    if layout == "phones3" and len(src) >= 3:
        hs = [1120, 1276, 1120]                       # الأوسط أكبر وقدّام
        devs = [device(src[1], hs[0]), device(src[0], hs[1]), device(src[2], hs[2])]
        gap = 46
        total = sum(d.width for d in devs) + gap * 2
        x = (W - total) // 2
        order = [(0, 96), (1, 132), (2, 96)]          # (index, قوة الظل)
        # الجناحين الأول عشان الأوسط يفضل فوقهم
        for i in (0, 2):
            xi = x + sum(devs[j].width + gap for j in range(i))
            place(canvas, devs[i], xi, (H - hs[i]) // 2 + 32, 96)
        xi = x + devs[0].width + gap
        place(canvas, devs[1], xi, (H - hs[1]) // 2, 132)

    elif layout == "web2" and len(src) >= 2:
        # لقطات الويب عرضية — الارتفاع بيتحسب عشان الاتنين يدخلوا في الكانفس
        gap, avail = 50, W - 300
        ar0, ar1 = src[0].width / src[0].height, src[1].width / src[1].height
        h_front = int((avail - gap) / (ar0 + ar1 * 0.89))
        h_front = min(h_front, H - 220)
        h_back = int(h_front * 0.89)
        back = device(src[1], h_back)
        front = device(src[0], h_front)
        total = back.width + front.width + gap
        x0 = (W - total) // 2
        place(canvas, back, x0, (H - h_back) // 2 + 30, 96)
        place(canvas, front, x0 + back.width + gap, (H - h_front) // 2, 128)

    else:
        h = 1290
        d = device(src[0], h)
        place(canvas, d, (W - d.width) // 2, (H - h) // 2, 130)

    rgb = canvas.convert("RGB")
    rgb.resize((1600, 1000), Image.LANCZOS).save(f"{OUT}/cover-{slug}.webp", "WEBP", quality=88, method=6)
    rgb.resize((880, 550), Image.LANCZOS).save(f"{OUT}/thumb-{slug}.webp", "WEBP", quality=84, method=6)
    print("✓", slug, len(src), "لقطة ·",
          os.path.getsize(f"{OUT}/cover-{slug}.webp") // 1024, "KB")
