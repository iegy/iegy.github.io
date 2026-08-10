# -*- coding: utf-8 -*-
"""
يبني نسخة النشر المضغوطة.

الفكرة: تفضل تعدّل في الملفات المقروءة (style.css / script.js / knowledge.js)،
والسكربت ده بيطلّع منها نسخة مضغوطة للنشر مع ترويسة حقوق الملكية.

الاستخدام:
    python3 build.py            # يبني الصفحات
    python3 minify.py           # يضغط CSS و JS
    python3 minify.py --restore # يرجّع النسخ المقروءة

يحتاج مرة واحدة:
    npm i -g terser clean-css-cli
"""
import os, shutil, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, '_readable')          # نسخة احتياطية من الملفات المقروءة
JS = ['script.js', 'knowledge.js']
CSS = ['style.css']

BANNER = ('/*! محمد حسين — Mohammed Hussein | © 2026 جميع الحقوق محفوظة\n'
          ' *  https://iegy.github.io · egyup@outlook.com\n'
          ' *  الكود ده ملكية خاصة — ممنوع النسخ أو إعادة الاستخدام بدون إذن كتابي.\n'
          ' *  Proprietary. Do not copy or reuse without written permission.\n'
          ' */\n')


def kb(p):
    return os.path.getsize(p) / 1024


def backup():
    os.makedirs(SRC, exist_ok=True)
    for f in JS + CSS:
        dst = os.path.join(SRC, f)
        if not os.path.exists(dst):
            shutil.copy2(os.path.join(HERE, f), dst)


def restore():
    if not os.path.isdir(SRC):
        print('مفيش نسخة مقروءة محفوظة.')
        return
    for f in JS + CSS:
        s = os.path.join(SRC, f)
        if os.path.exists(s):
            shutil.copy2(s, os.path.join(HERE, f))
            print('↩', f)
    print('\nرجّعت النسخ المقروءة. عدّل زي ما انت عايز وبعدين شغّل minify.py تاني.')


def run(cmd):
    r = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(r.stderr.strip()[:200])


def minify():
    backup()
    before = after = 0
    for f in JS:
        src, out = os.path.join(SRC, f), os.path.join(HERE, f)
        b = kb(src)
        run(f'terser "{src}" -c -m --format comments=false -o "{out}"')
        body = open(out, encoding='utf-8').read()
        open(out, 'w', encoding='utf-8').write(BANNER + body)
        a = kb(out); before += b; after += a
        print(f'  {f:16s} {b:6.1f} → {a:6.1f} KB')

    for f in CSS:
        src, out = os.path.join(SRC, f), os.path.join(HERE, f)
        b = kb(src)
        run(f'cleancss -O2 "{src}" -o "{out}"')
        body = open(out, encoding='utf-8').read()
        open(out, 'w', encoding='utf-8').write(BANNER + body)
        a = kb(out); before += b; after += a
        print(f'  {f:16s} {b:6.1f} → {a:6.1f} KB')

    print(f'\n  المجموع        {before:6.1f} → {after:6.1f} KB  '
          f'(توفير {100 - after / before * 100:.0f}%)')
    print('\n  النسخ المقروءة محفوظة في _readable/ — متمسحهاش.')


if __name__ == '__main__':
    if '--restore' in sys.argv:
        restore()
    else:
        try:
            minify()
        except Exception as e:
            print('فشل الضغط:', e)
            print('\nثبّت الأدوات الأول:  npm i -g terser clean-css-cli')
