# -*- coding: utf-8 -*-
"""محتوى صفحة «جسر» (iegy.net/jisr). build.py بيستدعي page() ويحط النتيجة جوه قالب الموقع."""
import os

HERE = os.path.dirname(os.path.abspath(__file__))

# (التصنيف, أيقونة, العنوان, الشرح)
FEATS = [
 ("send", "📦", "أي نوع وأي حجم", "ملفات وصور وفيديو وتطبيقات ومستندات — ومفيش سقف 4 جيجا: الملف الواحد بيعدّي مهما كبر."),
 ("send", "🗂️", "مجلدات بهيكلها", "اختار مجلد فيه آلاف الملفات وهيوصل بنفس ترتيبه، كسلة واحدة تتبعت مرة واحدة."),
 ("send", "🔁", "مبيبدأش من الأول", "الاتصال قطع؟ الموبايل اتقفل؟ التطبيق اتقفل؟ النقل يكمّل من آخر بايت وصل، لوحده."),
 ("send", "⏱️", "سرعة ووقت متبقي", "تشوف السرعة والباقي لحظة بلحظة، وتوقف مؤقت أو تلغي أو تكمّل وقت ما تحب."),
 ("send", "📡", "أكتر من جهاز مرة واحدة", "ابعت نفس الحاجة لكذا موبايل في نفس الوقت على نفس الشبكة من غير ما تكرر."),
 ("send", "🖼️", "الجودة بإيدك", "صغّر الصور قبل الإرسال لو عايز توفر حجم (اختياري)، والفيديو بيتبعت بأصله دايمًا."),
 ("sec", "🔐", "تشفير من طرف لطرف", "ECDH P-256 ومفتاح جلسة جديد لكل عملية، وكل إطار مشفّر AES-256-GCM. مفيش سيرفر في النص."),
 ("sec", "🔥", "تأكد إنه جهازك", "امسح رمز QR أو قارن أربع رموز تعبيرية على الشاشتين — لو اتطابقت، مفيش حد وسطكم."),
 ("sec", "✅", "أجهزة موثوقة", "كل جهاز له مفتاح هوية في Android Keystore. الموثوق بيستقبل منه تلقائي، والمنتحل بيتّرفض."),
 ("sec", "🧬", "بصمة لكل ملف", "SHA-256 بيتحسب ويتقارن في الآخر، فلو بايت واحد اتغيّر هتعرف."),
 ("any", "🌐", "غرفة لأي متصفح", "آيفون؟ لابتوب؟ تلفزيون؟ افتح غرفة، والباقي يدخل بمسح QR وPIN من غير ما يثبّت حاجة."),
 ("any", "📂", "مجلد مشترك للقراءة فقط", "شارك مجلد وخلي الناس تتصفحه وتحمّل منه ملف ملف أو ZIP، ومن غير ما يعدلوا فيه."),
 ("any", "🖥️", "تطبيق ويندوز صغير", "لو بتنقل كتير للكمبيوتر: برنامج من غير تثبيت بيظهر في قايمة الأجهزة القريبة، وبيستقبل بنفس التشفير والاستكمال والاتصالات المتوازية."),
 ("any", "📋", "حافظة مشتركة", "انسخ نص على موبايلك والصقه على اللابتوب (وبالعكس) جوه الغرفة، لحظيًا."),
 ("any", "💬", "نصوص وروابط سريعة", "ابعت لينك أو رقم أو كلمة سر من غير ما تعمل ملف، ويتفتح بضغطة."),
 ("any", "👥", "غرف وأعضاء", "تتحكم فيمن يدخل: موافقة يدوية، طرد، وقف الرفع أو التحميل، ومدة تنتهي لوحدها."),
 ("phone", "📱", "موبايل جديد في خطوات", "جهات الاتصال والصور والفيديو والتطبيقات تنتقل للموبايل الجديد من غير كابلات ولا سحابة."),
 ("phone", "💾", "نسخ احتياطي بين جهازين", "نسخة محلية على موبايل تاني، والجهاز التاني بيتخطى اللي عنده — كرره براحتك."),
 ("tidy", "🧾", "سجل بكل حاجة", "اللي اتبعت واللي اتستقبل، ولمين، وامتى، ونجح ولا لأ — وتعيد الإرسال من السجل."),
 ("tidy", "🌗", "عربي وإنجليزي، فاتح وداكن", "الواجهة كلها بتتحوّل بحرية، من اليمين لليسار وبالعكس."),
 ("tidy", "🔄", "تحديث من جوه التطبيق", "بيتشيك على إصدار جديد ويتحقق من بصمته قبل ما يتثبّت."),
 ("tidy", "🛡️", "متوافق مع حصن", "جسر وحصن بيتكلموا نفس اللغة، فتبعت من واحد للتاني عادي. وحصن متصفح بيحجب الإعلانات: iegy.net/H"),
]

CATS = [("all", "الكل"), ("send", "النقل"), ("sec", "الأمان"), ("any", "أي جهاز"), ("phone", "موبايل جديد"), ("tidy", "التنظيم")]

FAQ = [
 ("محتاج إنترنت؟", "لا. جسر بيشتغل على نفس الواي فاي، أو بيعمل شبكة واي فاي خاصة بين الجهازين من غير راوتر ولا باقة. الإنترنت محتاجه بس وقت التحميل أو التحديث."),
 ("في تطبيق للويندوز؟", "أيوه، تطبيق صغير من غير تثبيت: فكّ الـ ZIP وشغّل Jisr.exe، وسمح للـ Firewall على الشبكات الخاصة أول مرة. بتلاقيه في «الأجهزة القريبة» على الموبايل أو بتمسح الرمز اللي فيه، والملفات بتتحفظ في Downloads\\Jisr."),
 ("أبعت لآيفون أو كمبيوتر؟", "أيوه، من «غرفة مشاركة»: بتفتح صفحة مؤقتة على موبايلك والطرف التاني بيدخلها من أي متصفح من غير ما يثبّت حاجة. التطبيق نفسه أندرويد."),
 ("فيه حد أقصى لحجم الملف؟", "لأ. الملفات الأكبر من 4 جيجا ماشية، والمجلدات الكبيرة كمان. بس لازم مكان فاضي على الجهاز المستقبل، والتطبيق بيتشيك على ده قبل ما يبدأ."),
 ("لو النت أو الاتصال قطع في النص؟", "النقل بيكمّل من آخر بايت وصل، لوحده أو بضغطة، وحتى لو قفلت التطبيق. ده من أساس التصميم، مش ميزة إضافية."),
 ("آمن ولا لأ؟", "كل جلسة مشفّرة من طرف لطرف، وكل ملف بيتتحقق منه ببصمة SHA-256، والتحقق من الطرف التاني برمز QR أو أربع رموز تعبيرية، والأجهزة الموثوقة بتتعرّف بمفتاح هوية. مفيش حسابات ولا سيرفرات بتشوف ملفاتك."),
 ("فين بتتحفظ الملفات؟", "في مجلد Download/Jisr على الموبايل، والنسخ الاحتياطي في Download/Jisr Backup."),
 ("بيتوافق مع حصن؟", "أيوه، جسر وحصن بيتبادلوا الملفات مع بعض. وحصن متصفحي اللي بيحجب الإعلانات ويحمّل الفيديو، وفيه جسر جواه: <a href=\"https://iegy.net/H/\">iegy.net/H</a>."),
 ("ليه التثبيت بيسأل عن «مصدر غير معروف»؟", "لأن التطبيق بيتحمّل من الموقع مباشرة مش من متجر. الـ APK موقّع، وبصمته منشورة في ملف version.json وقدامك على صفحة الإصدار في GitHub."),
]

CSS = r"""
<style>
.jz{--g1:#2A9468;--g2:#1F7A55;--g3:#0E3B2A;--g4:#07241A;--gold:#F0A52A;--ivory:#F6F3EC;--bad:#ff7a59}
.jz section{padding-block:clamp(54px,8vw,96px)}
.jz .eyebrow{color:var(--g2)}html[data-theme=dark] .jz .eyebrow{color:var(--g1)}
.jz svg[viewBox="0 0 58 78"]{aspect-ratio:58/78}
.jz-dark{background:radial-gradient(1200px 600px at 80% -10%,#14583f 0,transparent 60%),linear-gradient(180deg,var(--g4),var(--g3));color:#EAF4EE}
.jz-dark p,.jz-dark .lead{color:rgba(234,244,238,.78)}
.jz-dark h1,.jz-dark h2,.jz-dark h3{color:#fff}
.jz-dark .eyebrow{color:var(--gold)}
.jz-dark .eyebrow::before,.jz-dark .eyebrow::after{color:rgba(255,255,255,.4)}
.jz-btn{background:var(--gold);color:#241800!important;border-color:var(--gold)}
.jz-btn:hover{background:#ffbb4a!important;color:#241800!important;box-shadow:0 14px 28px -12px rgba(240,165,42,.8)!important}
.jz-btn-g{background:var(--g2);color:#fff!important}
.jz-btn-g:hover{background:var(--g1)!important;color:#fff!important}
.jz-ghost{border-color:rgba(255,255,255,.35);color:#fff}
.jz-ghost:hover{background:#fff!important;color:var(--g3)!important}
/* hero */
.jz-hero{padding-block:clamp(34px,6vw,72px) clamp(38px,6vw,76px)!important;position:relative;overflow:hidden}
.jz-hero-grid{display:grid;gap:clamp(26px,4vw,54px);align-items:center;grid-template-columns:1fr}
@media(min-width:980px){.jz-hero-grid{grid-template-columns:.9fr 1.1fr}}
.jz-hero h1{font-size:clamp(2.1rem,5.2vw,3.6rem);line-height:1.4}
.jz-hero h1 em{font-style:normal;color:var(--gold);white-space:nowrap}
.jz-cta{display:flex;gap:12px;flex-wrap:wrap;margin-top:26px}
.jz-qr{display:none;align-items:center;gap:14px;margin-top:20px;font-size:.92rem;line-height:1.6;color:rgba(255,255,255,.82)}
.jz-qrbox{width:112px;height:112px;padding:6px;background:#fff;border-radius:12px;flex:none}
.jz-qrbox svg{width:100%;height:100%;display:block}
@media (hover:hover) and (pointer:fine) and (min-width:900px){.jz-qr{display:flex}}
.jz-pills{display:flex;gap:8px;flex-wrap:wrap;margin-top:22px}
.jz-pill{font-family:var(--font-mono);font-size:.74rem;padding:6px 13px;border:1px solid rgba(255,255,255,.22);border-radius:99px;color:#EAF4EE;background:rgba(255,255,255,.06);direction:rtl}
.jz-note{font-size:.86rem;margin-top:14px;opacity:.85}
/* scene */
.jz-scene{position:relative;direction:ltr;aspect-ratio:16/10;border-radius:22px;overflow:hidden;container-type:inline-size;background:linear-gradient(180deg,#06231A 0%,#0C3A29 56%,#0E4A34 100%);box-shadow:0 40px 80px -36px rgba(0,0,0,.8),inset 0 0 0 1px rgba(255,255,255,.08);isolation:isolate}
.jz-deco{position:absolute;inset:0;width:100%;height:100%}
.jz-star{animation:jzTw 3.2s ease-in-out infinite}
.jz-star:nth-child(2n){animation-delay:.8s}.jz-star:nth-child(3n){animation-delay:1.7s}
@keyframes jzTw{0%,100%{opacity:.25}50%{opacity:1}}
.jz-wave{animation:jzWave 7s linear infinite}
@keyframes jzWave{to{transform:translateX(-80px)}}
.jz-phone{position:absolute;top:10%;width:17%;height:56%;border-radius:2.2cqw;background:#10161B;border:.45cqw solid #26313A;box-shadow:0 2cqw 4cqw -1.4cqw rgba(0,0,0,.7);display:flex;flex-direction:column;overflow:hidden;z-index:3}
.jz-phone.s{right:1.5%}.jz-phone.r{left:1.5%}
.jz-phone .bar{height:6%;display:flex;justify-content:center;align-items:center}
.jz-phone .bar i{width:30%;height:34%;border-radius:9px;background:#26313A;display:block}
.jz-phone .scr{flex:1;margin:0 7% 7%;border-radius:1.4cqw;background:linear-gradient(180deg,#F6F3EC,#E8F1EB);direction:rtl;padding:6% 7%;display:flex;flex-direction:column;gap:5%;font-size:clamp(7px,1.45cqw,15px);line-height:1.35;color:#0E3B2A;text-align:center;justify-content:center;align-items:center}
.jz-phone .scr b{font-size:1.1em}
.jz-phone .scr small{font-size:.82em;opacity:.7}
.jz-phone .ico{font-size:2.5em;line-height:1}
.jz-ring{--p:0;width:6.2cqw;height:6.2cqw;border-radius:50%;display:grid;place-items:center;background:conic-gradient(var(--g2) calc(var(--p)*1%),#cfe3d8 0)}
.jz-ring span{width:76%;height:76%;border-radius:50%;background:#F6F3EC;display:grid;place-items:center;font-weight:700;font-size:1.35cqw;font-family:var(--font-mono);color:#0E3B2A}
.jz-lbl{position:absolute;top:68%;font-size:clamp(8px,1.5cqw,15px);color:rgba(255,255,255,.7);font-family:var(--font-ar);direction:rtl;z-index:3;width:17%;text-align:center}
.jz-lbl.s{right:1.5%}.jz-lbl.r{left:1.5%}
.jz-deck{position:absolute;left:17%;right:17%;top:66%;height:3.2%;z-index:2}
.jz-walker{position:absolute;bottom:100%;width:8.4cqw;left:50%;transform:translateX(-50%);z-index:4;transition:filter .3s}
.jz-walker svg{width:100%;height:auto;display:block;transform:scaleX(-1);overflow:visible}
.jz-walker.go svg{animation:jzBob .5s ease-in-out infinite}
@keyframes jzBob{0%,100%{transform:scaleX(-1) translateY(0)}50%{transform:scaleX(-1) translateY(-3.2%)}}
.jz-pack{position:absolute;bottom:108%;left:50%;transform:translateX(-50%);white-space:nowrap;font-size:clamp(8px,1.5cqw,15px);font-family:var(--font-mono);background:var(--gold);color:#241800;padding:.25em .7em;border-radius:99px;direction:ltr;box-shadow:0 6px 14px -6px rgba(0,0,0,.6)}
.jz-pack::after{content:"";position:absolute;top:100%;left:50%;margin-left:-.4em;border:.4em solid transparent;border-top-color:var(--gold)}
.jz-gap{position:absolute;top:-2px;bottom:-2px;width:7%;margin-left:-3.5%;background:#06231A;opacity:0;pointer-events:none;transition:opacity .25s;z-index:3;border-inline:.25cqw dashed var(--bad)}
.jz-gap::after{content:"⚡";position:absolute;left:50%;top:-340%;transform:translateX(-50%);font-size:3cqw;filter:drop-shadow(0 0 8px var(--bad))}
.jz-scene.cut .jz-gap{opacity:1}
.jz-scene.cut .jz-walker{filter:saturate(.4) brightness(.85)}
.jz-chip{position:absolute;left:50%;top:5%;transform:translateX(-50%);z-index:5;direction:rtl;font-size:clamp(9px,1.7cqw,16px);padding:.35em 1.1em;border-radius:99px;background:rgba(7,36,26,.72);border:1px solid rgba(255,255,255,.2);color:#fff;backdrop-filter:blur(6px);white-space:nowrap;transition:background .3s,border-color .3s}
.jz-scene.cut .jz-chip{background:rgba(120,30,10,.75);border-color:var(--bad)}
.jz-scene.done .jz-chip{background:rgba(31,122,85,.85);border-color:#6fe0ae}
/* demo */
.jz-demo{display:grid;gap:22px;grid-template-columns:1fr;margin-top:30px}
@media(min-width:980px){.jz-demo{grid-template-columns:1.35fr .65fr;align-items:stretch}}
.jz-panel{background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.14);border-radius:18px;padding:18px;display:flex;flex-direction:column;gap:14px}
.jz-stats{display:grid;grid-template-columns:repeat(3,1fr);gap:10px}
.jz-stats div{background:rgba(0,0,0,.22);border-radius:12px;padding:10px 12px;text-align:center}
.jz-stats b{display:block;font-family:var(--font-mono);font-size:1.15rem;direction:ltr;color:#fff}
.jz-stats span{font-size:.76rem;color:rgba(234,244,238,.65)}
.jz-bar{height:10px;border-radius:99px;background:rgba(255,255,255,.14);overflow:hidden}
.jz-bar i{display:block;height:100%;width:0;background:linear-gradient(90deg,var(--g1),var(--gold));border-radius:99px}
.jz-ctrl{display:flex;gap:8px;flex-wrap:wrap}
.jz-ctrl button{font-family:var(--font-ar);font-weight:700;font-size:.86rem;padding:9px 16px;border-radius:10px;border:1px solid rgba(255,255,255,.25);background:rgba(255,255,255,.08);color:#fff;cursor:pointer;transition:background .2s,transform .2s}
.jz-ctrl button:hover:not(:disabled){background:rgba(255,255,255,.18);transform:translateY(-1px)}
.jz-ctrl button:disabled{opacity:.35;cursor:not-allowed}
.jz-ctrl button.cut{border-color:var(--bad);color:#ffb7a6}
.jz-ctrl button.go{background:var(--gold);color:#241800;border-color:var(--gold)}
.jz-log{flex:1;min-height:210px;max-height:300px;overflow:auto;background:#031610;border-radius:12px;padding:12px 14px;font-family:var(--font-mono);font-size:.76rem;line-height:1.9;direction:ltr;text-align:left;color:#BFE8D2}
.jz-log div{animation:jzIn .3s ease both}
@keyframes jzIn{from{opacity:0;transform:translateY(4px)}}
.jz-log .t{color:#5d9a7f}.jz-log .w{color:#ffb37a}.jz-log .k{color:#6fe0ae}
.jz-emo{font-size:1.5rem;letter-spacing:.3em;direction:ltr;text-align:center}
/* features */
.jz-filters{display:flex;flex-wrap:wrap;gap:9px;margin:0 0 26px}
.jz-grid{display:grid;gap:16px;grid-template-columns:repeat(auto-fill,minmax(255px,1fr))}
.jz-card{position:relative;background:var(--surface);border:1px solid var(--line);border-radius:18px;padding:22px 20px 20px;transition:transform .3s var(--ease),box-shadow .3s var(--ease),border-color .3s,opacity .25s;overflow:hidden}
.jz-card::before{content:"";position:absolute;inset-inline-end:-30px;top:-30px;width:110px;height:110px;border-radius:50%;background:radial-gradient(circle,color-mix(in srgb,var(--g1) 22%,transparent),transparent 70%);transition:transform .4s var(--ease)}
.jz-card:hover{transform:translateY(-5px);box-shadow:var(--shadow-md);border-color:color-mix(in srgb,var(--g1) 55%,var(--line))}
.jz-card:hover::before{transform:scale(1.8)}
.jz-card.hide{display:none}
.jz-ic{width:46px;height:46px;border-radius:14px;display:grid;place-items:center;font-size:1.5rem;background:color-mix(in srgb,var(--g1) 14%,var(--bg-alt));margin-bottom:12px;position:relative}
.jz-card h3{margin:0 0 6px;font-size:1.03rem}
.jz-card p{margin:0;font-size:.92rem;line-height:1.85;position:relative}
/* bridge divider */
.jz-bd{position:relative;height:104px;margin:0 auto;max-width:var(--maxw);padding-inline:var(--gutter);overflow:hidden}
.jz-bd::before{content:"";position:absolute;inset-inline:var(--gutter);bottom:14px;height:0;border-top:3px dashed color-mix(in srgb,var(--g1) 60%,transparent)}
.jz-bd .m{position:absolute;bottom:16px;width:56px;inset-inline-start:calc(100% - var(--gutter) - 56px);transition:inset-inline-start 3.4s cubic-bezier(.45,.05,.3,1)}
.jz-bd.in .m{inset-inline-start:var(--gutter)}
.jz-bd .m svg{width:100%;height:auto;display:block;transform:scaleX(-1)}
html[dir=ltr] .jz-bd .m{inset-inline-start:var(--gutter)}
/* room mock */
.jz-room{display:grid;gap:30px;grid-template-columns:1fr;align-items:center}
@media(min-width:960px){.jz-room{grid-template-columns:.9fr 1.1fr}}
.jz-browser{direction:ltr;background:var(--surface);border:1px solid var(--line-strong);border-radius:16px;overflow:hidden;box-shadow:var(--shadow-lg)}
.jz-bt{display:flex;align-items:center;gap:7px;padding:10px 12px;background:var(--bg-alt);border-bottom:1px solid var(--line)}
.jz-bt i{width:10px;height:10px;border-radius:50%;background:#e4894b;display:block}.jz-bt i:nth-child(2){background:#e8c56a}.jz-bt i:nth-child(3){background:#6fb58d}
.jz-url{flex:1;margin-inline-start:8px;font-family:var(--font-mono);font-size:.72rem;background:var(--bg);border:1px solid var(--line);border-radius:99px;padding:4px 12px;color:var(--text-soft);overflow:hidden;white-space:nowrap;text-overflow:ellipsis}
.jz-bb{padding:16px;direction:rtl;min-height:290px}
.jz-tabs{display:flex;gap:6px;margin-bottom:14px;flex-wrap:wrap}
.jz-tabs button{font-family:var(--font-ar);font-size:.82rem;font-weight:600;padding:7px 14px;border-radius:99px;border:1px solid var(--line-strong);background:transparent;color:var(--text-soft);cursor:pointer}
.jz-tabs button[aria-selected=true]{background:var(--g2);border-color:var(--g2);color:#fff}
.jz-pane{display:none;font-size:.88rem}.jz-pane.on{display:block;animation:jzIn .3s ease both}
.jz-row{display:flex;align-items:center;gap:10px;padding:10px 12px;border:1px solid var(--line);border-radius:12px;margin-bottom:8px;background:var(--bg)}
.jz-row b{font-weight:600}.jz-row small{margin-inline-start:auto;color:var(--text-soft);font-family:var(--font-mono);font-size:.7rem;direction:ltr}
.jz-pin{display:flex;gap:8px;justify-content:center;direction:ltr;margin:6px 0 12px}
.jz-pin span{width:38px;height:46px;border-radius:10px;border:1px solid var(--line-strong);display:grid;place-items:center;font-family:var(--font-mono);font-weight:700;font-size:1.3rem;background:var(--bg)}
.jz-steps{margin:18px 0 0;padding:0;list-style:none;display:grid;gap:12px;counter-reset:j}
.jz-steps li{display:grid;grid-template-columns:34px 1fr;gap:12px;align-items:start;counter-increment:j;color:var(--text-soft)}
.jz-steps li::before{content:counter(j);width:34px;height:34px;border-radius:50%;display:grid;place-items:center;background:var(--g2);color:#fff;font-weight:700;font-family:var(--font-mono);font-size:.85rem}
.jz-steps b{color:var(--text)}
/* hood */
.jz-hood{display:grid;gap:26px;grid-template-columns:1fr;align-items:center}
@media(min-width:960px){.jz-hood{grid-template-columns:1fr 1fr}}
.jz-term{background:#031610;border-radius:16px;padding:20px;border:1px solid rgba(255,255,255,.1);font-family:var(--font-mono);font-size:.8rem;line-height:2;direction:ltr;text-align:left;color:#BFE8D2;overflow:auto;box-shadow:var(--shadow-lg);white-space:pre}
.jz-term .c{color:#5d9a7f}.jz-term .a{color:var(--gold)}.jz-term .o{color:#6fe0ae}
/* compare */
.jz-tw{overflow:auto;border:1px solid var(--line);border-radius:18px;background:var(--surface)}
.jz-tw table{width:100%;border-collapse:collapse;min-width:640px;font-size:.92rem}
.jz-tw th,.jz-tw td{padding:13px 16px;text-align:center;border-bottom:1px solid var(--line)}
.jz-tw th:first-child,.jz-tw td:first-child{text-align:start;font-weight:600}
.jz-tw thead th{background:var(--bg-alt);font-family:var(--font-disp)}
.jz-tw th.me,.jz-tw td.me{background:color-mix(in srgb,var(--g1) 12%,transparent);font-weight:700}
.jz-tw tr:last-child td{border-bottom:0}
.y{color:#2e8a5c}.n{color:#c24a32}.m{color:#a88a5f}
html[data-theme=dark] .y{color:#6fe0ae}html[data-theme=dark] .n{color:#f0806a}
.jz-q{background:var(--surface);border:1px solid var(--line);border-radius:14px;padding:4px 18px;margin-top:10px}
.jz-q summary{cursor:pointer;font-weight:700;padding:13px 0;list-style:none;display:flex;justify-content:space-between;gap:10px}
.jz-q summary::after{content:"+";color:var(--g2);font-family:var(--font-mono);font-size:1.2rem;transition:transform .2s}
.jz-q[open] summary::after{transform:rotate(45deg)}
.jz-q p{margin:0 0 14px;line-height:1.9}
.jz-final{text-align:center;position:relative;overflow:hidden}
.jz-final .big{width:clamp(110px,16vw,170px);margin:0 auto 6px}
.jz-final .big svg{width:100%;height:auto;display:block;overflow:visible}
.jz-final .big{animation:jzFloat 3.2s ease-in-out infinite}
@keyframes jzFloat{0%,100%{transform:translateY(0)}50%{transform:translateY(-8px)}}
.jz-final .jz-cta{justify-content:center}
.jz-verify{font-family:var(--font-mono);font-size:.72rem;opacity:.7;direction:ltr;word-break:break-all;margin-top:18px}
@media(prefers-reduced-motion:reduce){.jz *,.jz *::before{animation:none!important}.jz-bd .m{transition:none}}
</style>
"""

BODY = r"""
<div class="jz">
<svg width="0" height="0" style="position:absolute" aria-hidden="true" focusable="false"><symbol id="jz-mo" viewBox="-24 -2 58 78"><g transform="translate(0,74) scale(1,-1)">__MO__</g></symbol></svg>

<section class="jz-dark jz-hero">
  <div class="wrap jz-hero-grid">
    <div>
      <div class="eyebrow">JISR · جسر</div>
      <h1>الملف بيعدّي… <em>مهما كان حجمه</em>، ومن غير نت</h1>
      <p class="lead" style="margin-top:16px;max-width:560px">جسر بيوصّل موبايلك بأي جهاز جنبك: ملفات ومجلدات وتطبيقات ونصوص. مشفّر، ومبيبدأش من الأول لو الاتصال قطع، ومن غير حساب ولا سيرفر.</p>
      <div class="jz-cta">
        <a id="jz-dl" class="btn btn-lg jz-btn" href="https://github.com/iegy/Jisr/releases/latest/download/Jisr.apk" download>حمّل جسر مجانًا ⬇</a>
        <a class="btn btn-lg jz-ghost" href="#demo">جرّب الجسر بنفسك ↓</a>
      </div>
      <div class="jz-qr"><div class="jz-qrbox">__QR__</div><div><b>على الكمبيوتر؟</b><br>صوّر الكود بموبايلك وحمّل جسر مباشرة.</div></div>
      <div class="jz-pills"><span class="jz-pill">بدون إنترنت</span><span class="jz-pill">بدون حساب</span><span class="jz-pill">مشفّر AES-256</span><span class="jz-pill">ملفات +4GB</span><span class="jz-pill">مجاني</span></div>
      <p class="jz-note" id="jz-ver">أندرويد 9 أو أحدث · من غير إعلانات ولا تتبّع</p>
    </div>
    <div class="jz-scene" id="heroScene" data-mode="auto" role="img" aria-label="رسم متحرك: الروبوت مو بيعدّي جسر شايل ملف من موبايل لموبايل، والاتصال بيقطع ويكمّل من نفس النقطة">
      __SCENE__
    </div>
  </div>
</section>

<section class="section-alt" style="padding-block:34px">
  <div class="wrap">
    <div class="stats reveal">
      <div class="stat"><b>0</b><span>إنترنت محتاجه</span></div>
      <div class="stat"><b>0</b><span>حسابات ولا سيرفرات</span></div>
      <div class="stat"><b>4GB+</b><span>للملف الواحد</span></div>
      <div class="stat"><b>256-bit</b><span>تشفير لكل جلسة</span></div>
    </div>
  </div>
</section>

<section class="jz-dark" id="demo">
  <div class="wrap">
    <div class="section-head reveal"><div class="eyebrow">TRY IT</div><h2>اقطع الجسر… وشوف اللي هيحصل</h2><p>محاكاة حيّة لنقل فيلم 4.7 جيجا. وقّفه، اقطع الاتصال، وكمّل — جسر بيرجع من آخر بايت.</p></div>
    <div class="jz-demo">
      <div>
        <div class="jz-scene" id="demoScene" data-mode="manual">__SCENE__</div>
      </div>
      <div class="jz-panel">
        <div class="jz-emo" id="dEmo" title="رموز التحقق">🔥 🌙 🚀 🐢</div>
        <div class="jz-bar"><i id="dBar"></i></div>
        <div class="jz-stats">
          <div><b id="dPct">0%</b><span>اكتمل</span></div>
          <div><b id="dSpd">—</b><span>السرعة</span></div>
          <div><b id="dEta">—</b><span>الباقي</span></div>
        </div>
        <div class="jz-ctrl">
          <button class="go" id="bStart">ابدأ النقل</button>
          <button id="bPause" disabled>إيقاف مؤقت</button>
          <button class="cut" id="bCut" disabled>✂ اقطع الاتصال</button>
          <button id="bCancel" disabled>إلغاء</button>
        </div>
        <div class="jz-log" id="dLog" aria-live="polite"></div>
        <small style="color:rgba(234,244,238,.55)">محاكاة توضيحية بسرعة مُسرَّعة، الأرقام للتوضيح.</small>
      </div>
    </div>
  </div>
</section>

<div class="jz-bd reveal"><span class="m"><svg viewBox="0 0 58 78"><use href="#jz-mo"/></svg></span></div>

<section>
  <div class="wrap">
    <div class="section-head reveal"><div class="eyebrow">FEATURES</div><h2>كل اللي محتاجه عشان تنقل أي حاجة، ولأي حد</h2><p>20+ ميزة اتبنت من الصفر على بروتوكول واحد: النقل والأمان والمتصفح وتغيير الموبايل.</p></div>
    <div class="jz-filters" role="group" aria-label="تصنيف المميزات">__FILTERS__</div>
    <div class="jz-grid">__CARDS__</div>
  </div>
</section>

<section class="section-alt">
  <div class="wrap jz-room">
    <div>
      <div class="eyebrow">WEB ROOM</div>
      <h2 class="reveal">آيفون أو لابتوب؟ مفيش مشكلة — الغرفة بتتفتح في المتصفح</h2>
      <p class="lead reveal" style="margin-top:12px">من التطبيق افتح «غرفة مشاركة»، وأي جهاز بمتصفح يدخلها من غير ما يثبّت أي حاجة. الغرفة مؤقتة وبتتقفل لوحدها. ولو بتنقل كتير لكمبيوتر ويندوز، استخدم <a href="https://github.com/iegy/Jisr/releases/latest/download/Jisr-Windows.zip">تطبيق جسر للويندوز</a>: من غير تثبيت وأسرع.</p>
      <ol class="jz-steps">
        <li><span><b>افتح الغرفة</b> واختار مدتها، وحط PIN لو عايز.</span></li>
        <li><span><b>الطرف التاني يمسح الـ QR</b> أو يكتب العنوان في المتصفح.</span></li>
        <li><span><b>وافق على دخوله</b>، وابدأ شارك: ملفات، نصوص، حافظة، مجلد للتصفح.</span></li>
      </ol>
    </div>
    <div class="jz-browser reveal" id="roomMock">
      <div class="jz-bt"><i></i><i></i><i></i><span class="jz-url">http://192.168.43.1:8080 · جسر</span></div>
      <div class="jz-bb">
        <div class="jz-tabs" role="tablist">
          <button role="tab" aria-selected="true" data-t="feed">الخلاصة</button>
          <button role="tab" aria-selected="false" data-t="folder">المجلد</button>
          <button role="tab" aria-selected="false" data-t="clip">الحافظة</button>
          <button role="tab" aria-selected="false" data-t="people">الأعضاء</button>
        </div>
        <div class="jz-pane on" data-p="feed">
          <div class="jz-row">📄 <b>عقد-الإيجار.pdf</b><small>2.4 MB</small></div>
          <div class="jz-row">🎬 <b>رحلة-الساحل.mp4</b><small>1.8 GB</small></div>
          <div class="jz-row">💬 <b>الباسورد: ••••••</b><small>نص</small></div>
        </div>
        <div class="jz-pane" data-p="folder">
          <div class="jz-row">📁 <b>صور الشغل</b><small>412 ملف</small></div>
          <div class="jz-row">📁 <b>مستندات</b><small>38 ملف</small></div>
          <div class="jz-row">🗜️ <b>تحميل المجلد كله ZIP</b><small>قراءة فقط</small></div>
        </div>
        <div class="jz-pane" data-p="clip">
          <div class="jz-row">📋 <b>https://iegy.net/jisr</b><small>من الموبايل</small></div>
          <div class="jz-row">📋 <b>اجتماع 5 المغرب</b><small>من اللابتوب</small></div>
        </div>
        <div class="jz-pane" data-p="people">
          <div class="jz-row">💻 <b>لابتوب سارة</b><small>متصل</small></div>
          <div class="jz-row">📱 <b>آيفون كريم</b><small>متصل</small></div>
          <div class="jz-row">⏳ <b>طلب دخول جديد</b><small>وافق · ارفض</small></div>
        </div>
      </div>
    </div>
  </div>
</section>

<div class="jz-bd reveal"><span class="m"><svg viewBox="0 0 58 78"><use href="#jz-mo"/></svg></span></div>

<section>
  <div class="wrap jz-hood">
    <div>
      <div class="eyebrow">UNDER THE HOOD</div>
      <h2 class="reveal">جوه الجسر: أمان بيتبني بالمفاتيح، مش بالوعود</h2>
      <p class="lead reveal" style="margin-top:12px">ملفاتك مبتعدّيش على أي سيرفر. الجهازين بيتفقوا على مفتاح بينهم، والتشفير بيحصل على الموبايل قبل ما أول بايت يتحرك.</p>
    </div>
    <div class="jz-term reveal"><span class="c"># 1) QR / emoji → verify peer</span>
<span class="a">ticket</span> = HISNJISR1:&lt;ip, port, secret&gt;
<span class="c"># 2) key agreement</span>
<span class="a">shared</span> = ECDH(P-256, mine, theirs)
<span class="a">key</span>    = HKDF-SHA256(shared, ticket)
<span class="c"># 3) every frame</span>
<span class="a">frame</span>  = AES-256-GCM(key, nonce++, chunk)
<span class="c"># 4) every file</span>
<span class="a">sha256</span> = hash(file) <span class="o">== peer.sha256 ✓</span>
<span class="c"># 5) resume</span>
<span class="a">offset</span> = ledger[transferId]  <span class="o">→ continue</span></div>
  </div>
</section>

<section class="section-alt">
  <div class="wrap">
    <div class="section-head reveal"><div class="eyebrow">COMPARE</div><h2>ليه جسر مش طريقة تانية؟</h2></div>
    <div class="jz-tw reveal">
      <table>
        <thead><tr><th></th><th class="me">جسر</th><th>بلوتوث</th><th>تطبيقات الرسائل</th><th>السحابة</th></tr></thead>
        <tbody>
          <tr><td>محتاج إنترنت؟</td><td class="me y">لا</td><td class="y">لا</td><td class="n">أيوه</td><td class="n">أيوه</td></tr>
          <tr><td>ملفات كبيرة جدًا</td><td class="me y">أكتر من 4GB</td><td class="m">بطيء جدًا</td><td class="n">حد أقصى</td><td class="m">حسب المساحة</td></tr>
          <tr><td>جودة الصور والفيديو</td><td class="me y">أصلية</td><td class="y">أصلية</td><td class="n">غالبًا مضغوطة</td><td class="y">أصلية</td></tr>
          <tr><td>يكمّل لو اتقطع</td><td class="me y">أيوه</td><td class="n">غالبًا لأ</td><td class="m">بيختلف</td><td class="m">بيختلف</td></tr>
          <tr><td>الخصوصية</td><td class="me y">بين جهازين بس</td><td class="y">بين جهازين</td><td class="m">عبر سيرفر</td><td class="n">على سيرفر</td></tr>
          <tr><td>أي جهاز بمتصفح</td><td class="me y">أيوه (الغرفة)</td><td class="n">لأ</td><td class="y">أيوه</td><td class="y">أيوه</td></tr>
        </tbody>
      </table>
    </div>
  </div>
</section>

<section>
  <div class="wrap">
    <div class="section-head reveal"><div class="eyebrow">HOW IT WORKS</div><h2>تبعت في ثلاث خطوات</h2></div>
    <div class="grid-3 stagger reveal">
      <div class="card"><div class="num">01</div><h3>افتح «استقبال»</h3><p>الجهاز المستقبل بيعرض رمز QR، وبيظهر كمان تلقائيًا للأجهزة اللي جنبه.</p></div>
      <div class="card"><div class="num">02</div><h3>اختار وامسح</h3><p>من الجهاز المرسل اختار الملفات أو المجلد، وامسح الرمز أو اختار الجهاز من القايمة.</p></div>
      <div class="card"><div class="num">03</div><h3>وافق وخلاص</h3><p>المستقبل بيوافق (أو الجهاز الموثوق بيدخل على طول) والنقل يبدأ، وبيكمّل لو اتقطع.</p></div>
    </div>
  </div>
</section>

<section class="section-alt">
  <div class="wrap" style="max-width:820px">
    <div class="section-head reveal"><div class="eyebrow">FAQ</div><h2>أسئلة بتتسأل</h2></div>
    __FAQ__
    <p style="margin-top:30px"><a class="link-out" href="work-jisr.html">قصة بناء جسر ←</a></p>
  </div>
</section>

<section class="jz-dark jz-final">
  <div class="wrap">
    <div class="big"><svg viewBox="0 0 58 78"><use href="#jz-mo"/></svg></div>
    <h2 class="reveal">يلا نعدّي؟</h2>
    <p class="lead reveal" style="margin:10px auto 0;max-width:520px">حمّل جسر وانقل أول ملف في دقيقة. مجاني، من غير إعلانات، ومن غير ما تسجّل.</p>
    <div class="jz-cta"><a id="jz-dl2" class="btn btn-lg jz-btn" href="https://github.com/iegy/Jisr/releases/latest/download/Jisr.apk" download>حمّل جسر لأندرويد ⬇</a><a class="btn btn-lg jz-ghost" href="https://github.com/iegy/Jisr/releases">كل الإصدارات</a><a class="btn btn-lg jz-ghost" href="jisr-privacy.html">سياسة الخصوصية</a><a class="btn btn-lg jz-ghost" href="https://iegy.net/H/">جرّب حصن</a></div>
    <p class="jz-note" id="jz-ver2">أندرويد 9 أو أحدث</p>
    <p class="jz-note" style="max-width:560px;margin-inline:auto">أول ما تفتح الملف، أندرويد هيسألك تسمح بالتثبيت من «مصدر غير معروف» — ده عادي لأي تطبيق مش من المتجر.</p>
    <p class="jz-verify" id="jz-sha"></p>
  </div>
</section>
</div>
"""

SCENE = r"""
<svg class="jz-deco" viewBox="0 0 1000 625" preserveAspectRatio="none" aria-hidden="true">
  <circle cx="500" cy="60" r="150" fill="#F0A52A" opacity=".05"/>
  <g fill="#fff">__STARS__</g>
  <circle cx="500" cy="92" r="30" fill="#F0A52A"/><circle cx="500" cy="92" r="52" fill="#F0A52A" opacity=".14"/>
  <path d="M0 430Q120 360 240 405T480 392T740 410T1000 380V625H0Z" fill="#0B3324"/>
  <path d="M170 412Q500 150 830 412" fill="none" stroke="#F6F3EC" stroke-width="7" stroke-linecap="round"/>
  <g stroke="#F6F3EC" stroke-width="2" opacity=".55">__HANGERS__</g>
  <rect x="170" y="410" width="660" height="22" rx="6" fill="#F6F3EC"/><rect x="170" y="405" width="660" height="6" rx="3" fill="#F0A52A"/>
  <g fill="#D8D1BE"><rect x="250" y="432" width="22" height="70"/><rect x="494" y="432" width="22" height="70"/><rect x="728" y="432" width="22" height="70"/></g>
  <rect x="0" y="490" width="1000" height="135" fill="#07241A"/>
  <g class="jz-wave" fill="none" stroke="#2A9468" stroke-width="3" opacity=".55"><path d="M-80 520q20-12 40 0t40 0t40 0t40 0t40 0t40 0t40 0t40 0t40 0t40 0t40 0t40 0t40 0t40 0t40 0t40 0t40 0t40 0t40 0t40 0t40 0t40 0t40 0t40 0t40 0t40 0"/><path d="M-60 560q20-12 40 0t40 0t40 0t40 0t40 0t40 0t40 0t40 0t40 0t40 0t40 0t40 0t40 0t40 0t40 0t40 0t40 0t40 0t40 0t40 0t40 0t40 0t40 0t40 0t40 0t40 0" opacity=".6"/></g>
</svg>
<div class="jz-phone s"><div class="bar"><i></i></div><div class="scr"><div class="ico">🎬</div><b data-j="fname">رحلة-الساحل.mp4</b><small data-j="fsize">4.7 GB</small></div></div>
<div class="jz-phone r"><div class="bar"><i></i></div><div class="scr"><div class="jz-ring" data-j="ring"><span data-j="rpct">0%</span></div><b data-j="rtitle">جاهز للاستقبال</b><small data-j="rsub">جهاز موثوق ✓</small></div></div>
<div class="jz-lbl s">المُرسِل</div><div class="jz-lbl r">المستقبِل</div>
<div class="jz-deck" data-j="deck"><span class="jz-gap" data-j="gap"></span>
  <div class="jz-walker" data-j="walker"><span class="jz-pack" data-j="pack">4.7 GB</span><svg viewBox="0 0 58 78"><use href="#jz-mo"/></svg></div>
</div>
<div class="jz-chip" data-j="chip">جاهز</div>
"""

JS = r"""
<script>
(function(){
  var reduce=window.matchMedia&&matchMedia('(prefers-reduced-motion:reduce)').matches;
  /* ---------- transfer simulator ---------- */
  var TOTAL=4.7*1024*1024*1024, SECS=15;
  function fmt(b){return b>=1073741824?(b/1073741824).toFixed(2)+' GB':b>=1048576?(b/1048576).toFixed(0)+' MB':(b/1024).toFixed(0)+' KB'}
  function mmss(s){s=Math.max(0,Math.round(s));var m=Math.floor(s/60),x=s%60;return m+':'+(x<10?'0':'')+x}
  function Sim(root,o){
    var q=function(k){return root.querySelector('[data-j="'+k+'"]')};
    var S={p:0,state:'idle',spd:0,cutDone:false,t:0,wait:0};
    var el={walker:q('walker'),deck:q('deck'),gap:q('gap'),chip:q('chip'),ring:q('ring'),rpct:q('rpct'),rtitle:q('rtitle'),rsub:q('rsub'),pack:q('pack')};
    o=o||{};
    function pos(){var x=94-S.p*88;el.walker.style.left=x+'%';el.gap.style.left=x+'%'}
    function paint(){
      pos();var pc=Math.round(S.p*100);
      el.ring.style.setProperty('--p',pc);el.rpct.textContent=pc+'%';
      root.classList.toggle('cut',S.state==='cut');root.classList.toggle('done',S.state==='done');
      el.walker.classList.toggle('go',S.state==='run');
      var chip={idle:'جاهز',run:'بيتنقل…',pause:'إيقاف مؤقت ⏸',cut:'الاتصال قطع ⚡',done:'وصل ✓ البصمة مطابقة',cancel:'اتلغى'}[S.state];
      el.chip.textContent=chip;
      el.rtitle.textContent={idle:'جاهز للاستقبال',run:'بيستقبل…',pause:'متوقف',cut:'مستني الاتصال',done:'اكتمل',cancel:'اتلغى'}[S.state];
      el.rsub.textContent=S.state==='cut'?'محفوظ عند '+fmt(S.p*TOTAL):S.state==='done'?'SHA-256 ✓':'جهاز موثوق ✓';
      if(o.onPaint)o.onPaint(S);
    }
    function loop(ts){
      if(!S.last)S.last=ts;var dt=Math.min(.1,(ts-S.last)/1000);S.last=ts;
      if(S.state==='run'){
        S.spd+=((34+Math.sin(ts/700)*6+Math.random()*3)-S.spd)*.08;
        S.p=Math.min(1,S.p+dt/SECS);
        if(o.auto&&!S.cutDone&&S.p>=.5){S.cutDone=true;api.cut()}
        if(S.p>=1){S.p=1;S.state='done';S.spd=0;if(o.onDone)o.onDone(S);if(o.auto)S.wait=3.2}
        paint();
      }else if(S.state==='cut'&&o.auto){S.wait-=dt;if(S.wait<=0)api.resume()}
      else if(S.state==='done'&&o.auto){S.wait-=dt;if(S.wait<=0)api.reset(true)}
      else if(S.state==='idle'&&o.auto&&S.wait>0){S.wait-=dt;if(S.wait<=0)api.start()}
      requestAnimationFrame(loop);
    }
    var api={
      S:S,
      start:function(){if(S.state==='run')return;S.state='run';if(o.onEvent)o.onEvent('start');paint()},
      pause:function(){if(S.state==='run'){S.state='pause';if(o.onEvent)o.onEvent('pause');paint()}else if(S.state==='pause'){S.state='run';if(o.onEvent)o.onEvent('resume');paint()}},
      cut:function(){if(S.state!=='run'&&S.state!=='pause')return;S.state='cut';S.spd=0;S.wait=2.6;if(o.onEvent)o.onEvent('cut');paint()},
      resume:function(){if(S.state!=='cut')return;S.state='run';if(o.onEvent)o.onEvent('reconnect');paint()},
      cancel:function(){if(S.state==='idle'||S.state==='done')return;S.state='cancel';S.spd=0;if(o.onEvent)o.onEvent('cancel');paint()},
      reset:function(autoRun){S.p=0;S.state='idle';S.cutDone=false;S.spd=0;S.wait=autoRun?1:0;if(o.onEvent)o.onEvent('reset');paint()}
    };
    el.pack.textContent=fmt(TOTAL);
    paint();
    if(!reduce)requestAnimationFrame(loop);else{S.p=.5;paint()}
    if(o.auto){S.wait=1.2}
    return api;
  }
  /* hero: auto loop */
  var hero=document.getElementById('heroScene');
  if(hero)Sim(hero,{auto:true});
  /* demo: manual */
  var demo=document.getElementById('demoScene');
  if(demo){
    var $=function(i){return document.getElementById(i)};
    var log=$('dLog'),bar=$('dBar'),pct=$('dPct'),spd=$('dSpd'),eta=$('dEta'),
        bS=$('bStart'),bP=$('bPause'),bC=$('bCut'),bX=$('bCancel');
    var emoji=['🔥 🌙 🚀 🐢','🦊 🍉 ⚡ 🎯','🐙 🌵 🎈 🧭'],k=0;
    function L(txt,cls){var d=document.createElement('div');d.innerHTML=(cls?'<span class="'+cls+'">':'')+txt+(cls?'</span>':'');log.appendChild(d);log.scrollTop=log.scrollHeight}
    function now(){var d=new Date();return '<span class="t">'+d.toTimeString().slice(0,8)+'</span> '}
    var sim=Sim(demo,{
      onPaint:function(S){
        bar.style.width=(S.p*100)+'%';pct.textContent=Math.round(S.p*100)+'%';
        var run=S.state==='run';
        spd.textContent=run?(S.spd.toFixed(0)+' MB/s'):'—';
        eta.textContent=run&&S.spd>1?mmss((1-S.p)*TOTAL/1048576/S.spd):'—';
        bS.disabled=!(S.state==='idle'||S.state==='cancel'||S.state==='done'||S.state==='cut');
        bS.textContent=S.state==='cut'?'كمّل من نفس النقطة':(S.state==='done'||S.state==='cancel')?'ابدأ من جديد':'ابدأ النقل';
        bP.disabled=!(S.state==='run'||S.state==='pause');bP.textContent=S.state==='pause'?'كمّل':'إيقاف مؤقت';
        bC.disabled=!(S.state==='run'||S.state==='pause');
        bX.disabled=!(S.state==='run'||S.state==='pause'||S.state==='cut');
      },
      onEvent:function(e){
        var o=Math.round(sim.S.p*TOTAL);
        if(e==='start'){$('dEmo').textContent=emoji[k++%3];L(now()+'اتصال مع المستقبل — التشفير تمام (ECDH P-256 ← AES-256-GCM)','k');L(now()+'بدأ إرسال: رحلة-الساحل.mp4 · '+fmt(TOTAL))}
        if(e==='pause')L(now()+'إيقاف مؤقت عند '+fmt(o),'w');
        if(e==='resume')L(now()+'كمّل من '+fmt(o));
        if(e==='cut')L(now()+'⚡ الاتصال قطع عند '+fmt(o)+' — الباقي محفوظ، مفيش بداية من الأول','w');
        if(e==='reconnect')L(now()+'رجع الاتصال ← استئناف من offset='+o+' بايت','k');
        if(e==='cancel')L(now()+'اتلغى النقل','w');
        if(e==='reset'&&sim.S.state==='idle'){}
      },
      onDone:function(){L(now()+'اكتمل ✓ SHA-256 مطابق، الملف اتحفظ في Download/Jisr','k')}
    });
    L('<span class="t">//</span> اضغط «ابدأ النقل»، وبعد ما يمشي جرّب «اقطع الاتصال».');
    bS.onclick=function(){var S=sim.S;if(S.state==='cut')sim.resume();else{if(S.state==='done'||S.state==='cancel')sim.reset();sim.start()}};
    bP.onclick=function(){sim.pause()};
    bC.onclick=function(){sim.cut()};
    bX.onclick=function(){sim.cancel()};
  }
  /* ---------- feature filters ---------- */
  var fl=document.querySelectorAll('.jz-filters .filter'),cards=document.querySelectorAll('.jz-card');
  fl.forEach(function(b){b.addEventListener('click',function(){
    fl.forEach(function(x){x.setAttribute('aria-pressed',x===b?'true':'false')});
    var c=b.getAttribute('data-c');cards.forEach(function(el){el.classList.toggle('hide',c!=='all'&&el.getAttribute('data-c')!==c)});
  })});
  /* ---------- room tabs ---------- */
  var tabs=document.querySelectorAll('#roomMock .jz-tabs button'),panes=document.querySelectorAll('#roomMock .jz-pane');
  tabs.forEach(function(b){b.addEventListener('click',function(){
    tabs.forEach(function(x){x.setAttribute('aria-selected',x===b?'true':'false')});
    panes.forEach(function(p){p.classList.toggle('on',p.getAttribute('data-p')===b.getAttribute('data-t'))});
  })});
  /* ---------- version from GitHub ---------- */
  fetch("https://raw.githubusercontent.com/iegy/Jisr/main/version.json",{cache:"no-store"}).then(function(r){return r.ok?r.json():null}).then(function(j){
    if(!j||!j.versionName)return;
    var mb=j.size?(j.size/1048576).toFixed(1).replace(/\.0$/,"")+" ميجا · ":"";
    var t="الإصدار "+j.versionName+" · "+mb+"أندرويد 9 أو أحدث";
    var a=document.getElementById("jz-ver"),b=document.getElementById("jz-ver2");
    if(a)a.textContent=t+" · من غير إعلانات";if(b)b.textContent=t;
    if(j.sha256){var s=document.getElementById("jz-sha");if(s)s.textContent="SHA-256: "+j.sha256}
  }).catch(function(){});
})();
</script>
"""


def _stars():
    pts = [(80,40),(150,110),(240,55),(330,130),(380,30),(610,50),(690,120),(760,40),(850,95),(930,45),(60,170),(960,160),(450,150),(560,160)]
    return "".join(f'<circle class="jz-star" cx="{x}" cy="{y}" r="{1.4 if i%3 else 2.2}"/>' for i, (x, y) in enumerate(pts))


def _hangers():
    out = []
    for x in range(230, 780, 50):
        t = (x - 170) / 660.0
        y = 412 - (4 * t * (1 - t)) * 131  # y of the quadratic arch at parameter t (approx.)
        out.append(f'<line x1="{x}" y1="{y:.0f}" x2="{x}" y2="406"/>')
    return "".join(out)


def page():
    mo = open(os.path.join(HERE, "jisr-mo-body.txt"), encoding="utf-8").read()
    scene = SCENE.replace("__STARS__", _stars()).replace("__HANGERS__", _hangers())
    filters = "".join(
        f'<button class="filter" type="button" data-c="{k}" aria-pressed="{"true" if k=="all" else "false"}" style="direction:rtl;font-family:var(--font-ar)">{n}</button>'
        for k, n in CATS)
    cards = "".join(
        f'<article class="jz-card reveal" data-c="{c}"><div class="jz-ic" aria-hidden="true">{i}</div><h3>{t}</h3><p>{d}</p></article>'
        for c, i, t, d in FEATS)
    faq = "".join(f'<details class="jz-q reveal"><summary>{q}</summary><p>{a}</p></details>' for q, a in FAQ)
    body = (BODY.replace("__MO__", mo).replace("__SCENE__", scene).replace("__QR__", open(os.path.join(HERE, "jisr-qr.svg.txt"), encoding="utf-8").read())
            .replace("__FILTERS__", filters).replace("__CARDS__", cards).replace("__FAQ__", faq))
    return CSS + body + JS
