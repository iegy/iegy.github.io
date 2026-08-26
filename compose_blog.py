# -*- coding: utf-8 -*-
"""
أغلفة مقالات المدونة — نفس أسلوب compose_new.py (خلفية متدرجة + توهج)،
لكن بدل مكيت الجهاز، أيقونة تجريدية كبيرة داخل لوحة زجاجية دائرية،
برسم SVG بخط رفيع بنفس هوية أيقونات الموقع في build.py.

يعتمد على cairosvg لتحويل الأيقونة لـ PNG بدقة عالية قبل تركيبها.
شغّله بعد أي إضافة/تعديل في posts.py:

    python3 compose_blog.py
"""
from PIL import Image, ImageDraw, ImageFilter
import cairosvg, io, os
from posts import POSTS

OUT = "."
W, H = 2400, 1500

# نفس عائلة ألوان الموقع (مستخرجة من تدرّجات الروبوت في template.html)
GRADIENTS = {
    "cream": ("#F5EEE1", "#DCCDB4"),
    "sage":  ("#A4AC8C", "#7E8869"),
    "tan":   ("#D3B389", "#A9855C"),
    "ember": ("#F0913F", "#D06B23"),
}
# لون الأيقونة نفسها — فاتحة على الغامق، غامقة على الفاتح
ICON_COLOR = {"cream": "#8A7554", "sage": "#F5F3EA", "tan": "#3E2E1C", "ember": "#3B1E0E"}
PANEL_COLOR = {"cream": (255, 255, 255, 92), "sage": (255, 255, 255, 60),
               "tan": (255, 255, 255, 70), "ember": (255, 255, 255, 66)}

# نفس مفردات الأيقونات الخطية المستخدمة في build.py (ICON dict) + إضافات لموضوعات المدونة
import math

def _gear(cx=12, cy=12, r_out=8.4, r_in=6, teeth=8, tooth_len=2.1):
    pts_out, pts_in = [], []
    for i in range(teeth * 2):
        ang = math.pi * 2 * i / (teeth * 2)
        r = r_out + (tooth_len if i % 2 == 0 else 0)
        pts_out.append((cx + r * math.cos(ang), cy + r * math.sin(ang)))
    d = "M" + " L".join(f"{x:.2f} {y:.2f}" for x, y in pts_out) + " Z"
    return f'<path d="{d}"/><circle cx="{cx}" cy="{cy}" r="2.6"/>'

ICONS = {
 "web": '<path d="M3 12h18M12 3a15 15 0 0 1 0 18a15 15 0 0 1 0-18z"/><circle cx="12" cy="12" r="9"/>',
 "gear": _gear(),
 "bolt": '<path d="M13 2 4.5 13.5H11l-1 8.5 8.5-11.5H12l1-8.5z"/>',
 "shield": '<path d="M12 2.5 20 6v6c0 5-3.4 8.4-8 9.5C7.4 20.4 4 17 4 12V6l8-3.5z"/>',
 "pulse": '<path d="M2.5 12h4.2l2-6 3.8 12 2-6h6.8"/>',
 "sparkle": '<path d="M12 3l1.9 5.6L19.5 10l-5.6 1.9L12 17.5l-1.9-5.6L4.5 10l5.6-1.9z"/>'
            '<path d="M19 15.5l.8 2.2 2.2.8-2.2.8-.8 2.2-.8-2.2-2.2-.8 2.2-.8z"/>',
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


def shadow(size, r, blur=50, alpha=90):
    s = Image.new("RGBA", (size[0] + blur * 3, size[1] + blur * 3), (0, 0, 0, 0))
    ImageDraw.Draw(s).ellipse(
        [blur * 1.5 - 30, blur * 1.5 - 10, blur * 1.5 + size[0] + 30, blur * 1.5 + size[1] + 10],
        fill=(24, 20, 14, alpha))
    return s.filter(ImageFilter.GaussianBlur(blur))


def icon_png(name, color, px):
    svg = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" '
           'fill="none" stroke="%s" stroke-width="1.15" stroke-linecap="round" '
           'stroke-linejoin="round">%s</svg>') % (color, ICONS[name])
    png = cairosvg.svg2png(bytestring=svg.encode(), output_width=px, output_height=px)
    return Image.open(io.BytesIO(png)).convert("RGBA")


for p in POSTS:
    slug, grad, icon = p["slug"], p["grad"], p["icon"]
    c1, c2 = GRADIENTS[grad]

    canvas = gradient((W, H), c1, c2).convert("RGBA")
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(glow).ellipse([-460, -560, 1180, 700], fill=(255, 255, 255, 60))
    canvas = Image.alpha_composite(canvas, glow.filter(ImageFilter.GaussianBlur(190)))

    # لوحة دائرية زجاجية في المنتصف
    panel_d = 760
    sh = shadow((panel_d, panel_d), panel_d // 2, alpha=100)
    canvas.alpha_composite(sh, ((W - sh.width) // 2, (H - sh.height) // 2 + 26))

    panel = Image.new("RGBA", (panel_d, panel_d), (0, 0, 0, 0))
    ImageDraw.Draw(panel).ellipse([0, 0, panel_d, panel_d], fill=PANEL_COLOR[grad])
    px, py = (W - panel_d) // 2, (H - panel_d) // 2
    canvas.alpha_composite(panel, (px, py))
    # حافة رفيعة على اللوحة
    ring = Image.new("RGBA", (panel_d, panel_d), (0, 0, 0, 0))
    ImageDraw.Draw(ring).ellipse([2, 2, panel_d - 3, panel_d - 3], outline=(255, 255, 255, 130), width=3)
    canvas.alpha_composite(ring, (px, py))

    ic = icon_png(icon, ICON_COLOR[grad], 360)
    canvas.alpha_composite(ic, ((W - ic.width) // 2, (H - ic.height) // 2))

    rgb = canvas.convert("RGB")
    rgb.resize((1600, 1000), Image.LANCZOS).save(f"{OUT}/cover-{slug}.webp", "WEBP", quality=88, method=6)
    rgb.resize((880, 550), Image.LANCZOS).save(f"{OUT}/thumb-{slug}.webp", "WEBP", quality=84, method=6)
    print("✓", slug, "·", os.path.getsize(f"{OUT}/cover-{slug}.webp") // 1024, "KB")
