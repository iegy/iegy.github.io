# -*- coding: utf-8 -*-
"""Apply the 2026-08-27 SEO/UX audit fixes, then rebuild the static site.

This script is intentionally strict: it stops if an expected source pattern is
missing so it cannot silently damage a later, structurally different version.
"""
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]


def read(name: str) -> str:
    return (ROOT / name).read_text(encoding="utf-8")


def write(name: str, text: str) -> None:
    (ROOT / name).write_text(text, encoding="utf-8")


def replace_exact(text: str, old: str, new: str, label: str, count: int = 1) -> str:
    actual = text.count(old)
    if actual != count:
        raise RuntimeError(f"{label}: expected {count} occurrence(s), found {actual}")
    return text.replace(old, new)


# ---------------------------------------------------------------- build.py
build = read("build.py")
build = replace_exact(
    build,
    "import json, os, sys, io, re\n",
    "import json, os, sys, io, re\nfrom datetime import date\n",
    "datetime import",
)
build = replace_exact(
    build,
    '        "title": title, "desc": desc, "site": SITE, "slug": slug, "page": page,\n',
    '        "title": title, "desc": desc, "site": SITE, "slug": slug, "page": page,\n'
    '        "canonical": SITE if slug == "index.html" else SITE + slug,\n',
    "canonical render value",
)

# Render real values in the HTML from the first response; JavaScript can still animate them.
build = replace_exact(
    build,
    '<span data-count="13" data-suffix="">0</span>',
    '<span data-count="{len(PROJECTS)}" data-suffix="">{len(PROJECTS)}</span>',
    "projects counter",
)
build = replace_exact(
    build,
    '<span data-count="4" data-suffix="">0</span>',
    '<span data-count="4" data-suffix="">4</span>',
    "services counter",
)
build = replace_exact(
    build,
    '<span data-count="100" data-suffix="%">0</span>',
    '<span data-count="100" data-suffix="%">100%</span>',
    "rtl counter",
)
build = replace_exact(
    build,
    '<span data-count="1" data-suffix="">0</span>',
    '<span data-count="1" data-suffix="">1</span>',
    "reply counter",
)

# Keep the portfolio meta description in sync with the actual project list.
build = replace_exact(
    build,
    '        "سبعة مشاريع منشورة: أنظمة كاشير ومخزون، إدارة مالية سحابية، تتبع طلبات متعدد الفروع، مواقع شركات، وتطبيق أندرويد مجاني لأدوات الفيديو والصوت.",\n',
    '        f"{len(PROJECTS)} مشروعًا منشورًا: مواقع وأنظمة إدارة أعمال وتطبيقات وأدوات رقمية عربية، مع صفحات تفصيلية وروابط تجربة أو تحميل مباشرة.",\n',
    "portfolio meta description",
)

# Correct the privacy claim: submissions are transmitted through Web3Forms.
build = replace_exact(
    build,
    '<p class="form-note">بياناتك بتوصلني أنا بس، ومش بتتسجل في أي مكان تاني.</p>',
    '<p class="form-note">تُستخدم بياناتك فقط للرد على طلبك، ويتم إرسال النموذج عبر خدمة Web3Forms.</p>',
    "contact privacy note",
)

# Make form validation announcements programmatically associated with each field.
build = replace_exact(
    build,
    '<input id="name" name="name" type="text" placeholder="اسمك الكامل" autocomplete="name" required>\n'
    '        <span class="err">اكتب اسمك من فضلك.</span>',
    '<input id="name" name="name" type="text" placeholder="اسمك الكامل" autocomplete="name" required aria-describedby="name-error" aria-invalid="false">\n'
    '        <span class="err" id="name-error">اكتب اسمك من فضلك.</span>',
    "name accessibility",
)
build = replace_exact(
    build,
    '<input id="contact" name="contact" type="text" placeholder="أفضل وسيلة نتواصل بيها" required>\n'
    '        <span class="err">محتاج وسيلة أقدر أرد عليك بيها.</span>',
    '<input id="contact" name="contact" type="text" placeholder="أفضل وسيلة نتواصل بيها" required aria-describedby="contact-error" aria-invalid="false">\n'
    '        <span class="err" id="contact-error">محتاج وسيلة أقدر أرد عليك بيها.</span>',
    "contact accessibility",
)
build = replace_exact(
    build,
    '<textarea id="message" name="message" placeholder="احكيلي عن فكرتك، والمدة اللي محتاجها..." required></textarea>\n'
    '        <span class="err">اكتب سطرين على الأقل عن المشروع.</span>',
    '<textarea id="message" name="message" placeholder="احكيلي عن فكرتك، والمدة اللي محتاجها..." required aria-describedby="message-error" aria-invalid="false"></textarea>\n'
    '        <span class="err" id="message-error">اكتب سطرين على الأقل عن المشروع.</span>',
    "message accessibility",
)

# Use the clean root URL for the home page in the sitemap and add a real build lastmod.
build = replace_exact(
    build,
    "        f'  <url><loc>{SITE}{s}</loc><changefreq>monthly</changefreq>'\n",
    "        f'  <url><loc>{SITE if s==\"index.html\" else SITE+s}</loc><lastmod>{date.today().isoformat()}</lastmod><changefreq>monthly</changefreq>'\n",
    "sitemap loc and lastmod",
)
write("build.py", build)


# ---------------------------------------------------------------- template.html
template = read("template.html")
template = replace_exact(
    template,
    '<link rel="canonical" href="{{site}}{{slug}}">',
    '<link rel="canonical" href="{{canonical}}">',
    "canonical template",
)
template = replace_exact(
    template,
    '<meta property="og:url" content="{{site}}{{slug}}">',
    '<meta property="og:url" content="{{canonical}}">',
    "og:url template",
)
# Two occurrences only: logo/brand and main nav home link.
template = replace_exact(
    template,
    'href="index.html"',
    'href="/"',
    "clean home links",
    count=2,
)
write("template.html", template)


# ---------------------------------------------------------------- style.css
style = read("style.css")
style = replace_exact(
    style,
    '--accent:var(--ember-dark);--accent-bright:var(--ember);--muted:var(--sand-dark);',
    '--accent:#AC5520;--accent-bright:var(--ember);--muted:#806643;',
    "light theme contrast tokens",
)
write("style.css", style)


# ---------------------------------------------------------------- script.js
script = read("script.js")
script = replace_exact(
    script,
    'q=function(e,t){e.closest(".field").classList.toggle("invalid",t)}',
    'q=function(e,t){e.closest(".field").classList.toggle("invalid",t),e.setAttribute("aria-invalid",t?"true":"false")}',
    "aria-invalid validation state",
)
write("script.js", script)


# ---------------------------------------------------------------- rebuild and verify
subprocess.run(["python3", "-m", "py_compile", "build.py"], cwd=ROOT, check=True)
subprocess.run(["python3", "build.py"], cwd=ROOT, check=True)

index = read("index.html")
contact = read("contact.html")
sitemap = read("sitemap.xml")

checks = {
    "home canonical": '<link rel="canonical" href="https://iegy.net/">' in index,
    "home og url": '<meta property="og:url" content="https://iegy.net/">' in index,
    "real project counter": f'data-count="13" data-suffix="">13</span>' in index,
    "real RTL counter": 'data-count="100" data-suffix="%">100%</span>' in index,
    "privacy wording": "Web3Forms" in contact and "مش بتتسجل في أي مكان تاني" not in contact,
    "form aria": 'aria-describedby="name-error" aria-invalid="false"' in contact,
    "root sitemap URL": '<loc>https://iegy.net/</loc>' in sitemap,
    "sitemap lastmod": "<lastmod>" in sitemap,
    "no canonical placeholder": "{{canonical}}" not in index,
}
failed = [name for name, ok in checks.items() if not ok]
if failed:
    raise RuntimeError("Verification failed: " + ", ".join(failed))

print("Audit fixes applied and verified successfully.")
