/* =========================================================
   MOHAMMED HUSSEIN — portfolio behaviour
   ========================================================= */
(function () {
  'use strict';

  var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---------- theme (set early in <head> to avoid flash) ---------- */
  var toggle = document.querySelector('.theme-toggle');
  if (toggle) {
    toggle.addEventListener('click', function () {
      var next = document.documentElement.dataset.theme === 'dark' ? 'light' : 'dark';
      document.documentElement.dataset.theme = next;
      try { localStorage.setItem('mh-theme', next); } catch (e) {}
      toggle.setAttribute('aria-label', next === 'dark' ? 'تفعيل الوضع النهاري' : 'تفعيل الوضع الليلي');
    });
  }

  /* ---------- mobile nav ---------- */
  var navToggle = document.querySelector('.nav-toggle');
  var navLinks = document.querySelector('nav.links');
  if (navToggle && navLinks) {
    var setNav = function (open) {
      navLinks.classList.toggle('open', open);
      navToggle.setAttribute('aria-expanded', String(open));
      document.body.style.overflow = open ? 'hidden' : '';
    };
    navToggle.addEventListener('click', function () {
      setNav(navToggle.getAttribute('aria-expanded') !== 'true');
    });
    navLinks.querySelectorAll('a').forEach(function (a) {
      a.addEventListener('click', function () { setNav(false); });
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && navLinks.classList.contains('open')) { setNav(false); navToggle.focus(); }
    });
  }

  /* ---------- active nav link ---------- */
  var current = document.body.dataset.page;
  document.querySelectorAll('nav.links a').forEach(function (a) {
    if (a.dataset.page === current) { a.classList.add('active'); a.setAttribute('aria-current', 'page'); }
  });

  /* ---------- sticky header shadow + scroll progress ---------- */
  var header = document.querySelector('header.site');
  var bar = document.querySelector('.progress');
  var ticking = false;
  function onScroll() {
    if (header) header.classList.toggle('stuck', window.scrollY > 8);
    if (bar) {
      var h = document.documentElement.scrollHeight - window.innerHeight;
      bar.style.width = (h > 0 ? (window.scrollY / h) * 100 : 0) + '%';
    }
    ticking = false;
  }
  window.addEventListener('scroll', function () {
    if (!ticking) { ticking = true; requestAnimationFrame(onScroll); }
  }, { passive: true });
  onScroll();

  /* ---------- reveal on scroll ---------- */
  var revealEls = document.querySelectorAll('.reveal, .stagger');
  if ('IntersectionObserver' in window && !reduced) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) { entry.target.classList.add('in'); io.unobserve(entry.target); }
      });
    }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });
    revealEls.forEach(function (el) { io.observe(el); });
  } else {
    revealEls.forEach(function (el) { el.classList.add('in'); });
  }

  /* ---------- animated counters ---------- */
  var counters = document.querySelectorAll('[data-count]');
  if (counters.length) {
    var run = function (el) {
      var target = parseFloat(el.dataset.count);
      var suffix = el.dataset.suffix || '';
      if (reduced) { el.textContent = target + suffix; return; }
      var start = performance.now(), dur = 1400;
      var tick = function (now) {
        var p = Math.min((now - start) / dur, 1);
        var eased = 1 - Math.pow(1 - p, 3);
        el.textContent = Math.round(target * eased) + suffix;
        if (p < 1) requestAnimationFrame(tick);
      };
      requestAnimationFrame(tick);
    };
    if ('IntersectionObserver' in window) {
      var cio = new IntersectionObserver(function (es) {
        es.forEach(function (e) { if (e.isIntersecting) { run(e.target); cio.unobserve(e.target); } });
      }, { threshold: 0.5 });
      counters.forEach(function (el) { cio.observe(el); });
    } else counters.forEach(run);
  }

  /* ---------- hero typing ---------- */
  var typeEl = document.querySelector('[data-typing]');
  if (typeEl) {
    var lines = JSON.parse(typeEl.dataset.typing);
    if (reduced) {
      typeEl.textContent = lines[lines.length - 1];
    } else {
      var li = 0, ci = 0, deleting = false;
      var cursor = document.createElement('span');
      cursor.className = 'type-cursor';
      cursor.textContent = '█';
      cursor.setAttribute('aria-hidden', 'true');
      var out = document.createElement('span');
      typeEl.textContent = '';
      typeEl.append(out, cursor);
      (function tick() {
        var full = lines[li];
        if (!deleting) {
          ci++;
          out.textContent = full.slice(0, ci);
          if (ci === full.length) {
            deleting = li < lines.length - 1;
            setTimeout(tick, deleting ? 1500 : 100000);
            return;
          }
        } else {
          ci--;
          out.textContent = full.slice(0, ci);
          if (ci === 0) { deleting = false; li++; }
        }
        setTimeout(tick, deleting ? 20 : 45);
      })();
    }
  }

  /* ---------- portfolio filters ---------- */
  var filters = document.querySelectorAll('.filter');
  if (filters.length) {
    var items = document.querySelectorAll('[data-cat]');
    var empty = document.querySelector('#no-results');
    filters.forEach(function (btn) {
      btn.addEventListener('click', function () {
        var cat = btn.dataset.filter;
        filters.forEach(function (b) { b.setAttribute('aria-pressed', String(b === btn)); });
        var shown = 0;
        items.forEach(function (it) {
          var match = cat === 'all' || it.dataset.cat.split(' ').indexOf(cat) > -1;
          it.classList.toggle('hide', !match);
          if (match) shown++;
        });
        if (empty) empty.hidden = shown !== 0;
      });
    });
  }

  /* ---------- contact form ---------- */
  var form = document.querySelector('#contact-form');
  if (form) {
    var status = form.querySelector('.form-status');
    var setErr = function (input, on) { input.closest('.field').classList.toggle('invalid', on); };

    form.querySelectorAll('input,textarea').forEach(function (i) {
      i.addEventListener('input', function () { setErr(i, false); });
    });

    var buildText = function (d) {
      return 'مرحبًا محمد، اسمي ' + d.name + '.\n' +
        'وسيلة تواصل بديلة: ' + d.contact + '\n' +
        (d.budget ? 'الميزانية التقريبية: ' + d.budget + '\n' : '') + '\n' + d.message;
    };

    var readForm = function () {
      return {
        name: form.name.value.trim(),
        contact: form.contact.value.trim(),
        budget: form.budget ? form.budget.value : '',
        message: form.message.value.trim()
      };
    };

    var validate = function () {
      var ok = true;
      ['name', 'contact', 'message'].forEach(function (k) {
        var el = form[k];
        var bad = el.value.trim().length < (k === 'message' ? 10 : 2);
        setErr(el, bad);
        if (bad && ok) { el.focus(); ok = false; }
      });
      return ok;
    };

    // WhatsApp path
    var waBtn = form.querySelector('[data-send="whatsapp"]');
    if (waBtn) {
      waBtn.addEventListener('click', function () {
        if (!validate()) return;
        window.open('https://wa.me/201000220606?text=' + encodeURIComponent(buildText(readForm())), '_blank', 'noopener');
        if (status) { status.className = 'form-status ok'; status.textContent = 'فتحنا لك واتساب برسالة جاهزة — ابعتها وهرد عليك في أقرب وقت.'; }
      });
    }

    // Email path (Web3Forms — replace the access key with your own)
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      if (!validate()) return;
      var key = form.dataset.accessKey;
      var submitBtn = form.querySelector('[type="submit"]');

      if (!key || key.indexOf('YOUR-') === 0) {
        // Not configured yet → fall back to the user's mail client, nothing is lost.
        var d = readForm();
        window.location.href = 'mailto:egyup@outlook.com?subject=' +
          encodeURIComponent('مشروع جديد من ' + d.name) + '&body=' + encodeURIComponent(buildText(d));
        if (status) { status.className = 'form-status ok'; status.textContent = 'فتحنا لك برنامج الإيميل برسالة جاهزة. لو مفتحش، ابعت على egyup@outlook.com مباشرة.'; }
        return;
      }

      var oldLabel = submitBtn.textContent;
      submitBtn.disabled = true; submitBtn.textContent = 'جاري الإرسال…';
      var d2 = readForm();
      fetch('https://api.web3forms.com/submit', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
        body: JSON.stringify({
          access_key: key, subject: 'مشروع جديد من ' + d2.name,
          from_name: d2.name, name: d2.name, contact: d2.contact,
          budget: d2.budget, message: d2.message
        })
      }).then(function (r) { return r.json(); }).then(function (j) {
        if (j.success) {
          form.reset();
          status.className = 'form-status ok';
          status.textContent = 'وصلتني رسالتك ✔ هرد عليك خلال يوم عمل واحد.';
        } else throw new Error('failed');
      }).catch(function () {
        status.className = 'form-status bad';
        status.textContent = 'حصلت مشكلة في الإرسال. جرّب زرار الواتساب تحت، أو ابعت على egyup@outlook.com.';
      }).finally(function () {
        submitBtn.disabled = false; submitBtn.textContent = oldLabel;
      });
    });
  }


  /* ============================================================
     الروبوت — ساكن الترمينال + رفيق الركن
     ============================================================ */
  (function robot(){
    var bot = document.getElementById('bot');
    if (!bot) return;
    var bubble = document.getElementById('botBubble');
    var term   = document.querySelector('.term-host');
    var page   = document.body.dataset.page || '';
    bot.hidden = false;

    var docked = false, lastTalk = 0, hideTimer = null, rollTimer = null, flipping = false;

    /* ---------- الكلام ---------- */
    function say(txt, ms){
      if (!txt) return;
      bubble.textContent = txt;
      bubble.classList.add('show');
      bot.classList.add('talking');
      lastTalk = Date.now();
      clearTimeout(hideTimer);
      hideTimer = setTimeout(function(){
        bubble.classList.remove('show');
        bot.classList.remove('talking');
      }, ms || 3200);
    }
    function pick(a){ return a[Math.floor(Math.random()*a.length)]; }

    var GREET = {
      home:      'أهلًا 👋 أنا مو، مساعد محمد',
      about:     'دي صفحة محمد الشخصية',
      services:  'دول الخدمات اللي بيقدمها',
      portfolio: 'كل مشروع هنا شغّال أونلاين — جرّبه',
      contact:   'املا النموذج، بيرد في يوم عمل واحد'
    };
    var POKES = [
      'أنا مو — مبني من SVG، مفيش صور خالص 🙂',
      'دوس على أي مشروع وشوف تفاصيله',
      'جرّب زرار القمر فوق — الوضع الليلي حلو',
      'كل حاجة هنا اتعملت من الصفر',
      'محتاج حاجة؟ صفحة التواصل تحت',
      'اسألني عن الوقت أو الطقس كمان 🌤️'
    ];
    var IDLE = [
      'لسه هنا لو محتاج حاجة',
      'خد وقتك، أنا مش مستعجل',
      'اسكرول تحت، في حاجات حلوة'
    ];

    /* ---------- التفاعل ---------- */
    function poke(){
      if (!reduced){
        bot.classList.add('jumping','waving');
        setTimeout(function(){ bot.classList.remove('jumping'); }, 700);
        setTimeout(function(){ bot.classList.remove('waving'); }, 1750);
      }
      clearTimeout(hideTimer);
      bubble.classList.remove('show');
      bot.classList.remove('talking');
      if (window.Chat) window.Chat.toggle();
      else say(pick(POKES));
    }
    bot.addEventListener('click', poke);
    bot.addEventListener('keydown', function(e){
      if (e.key === 'Enter' || e.key === ' '){ e.preventDefault(); poke(); }
    });

    /* ---------- الانتقال الناعم بين الترمينال والركن (FLIP) ---------- */
    function moveTo(toDock){
      if (docked === toDock || flipping) return;
      var a = bot.getBoundingClientRect();
      if (toDock) term.appendChild(bot), bot.classList.add('docked');
      else document.body.appendChild(bot), bot.classList.remove('docked');
      docked = toDock;
      if (reduced) return;
      var b = bot.getBoundingClientRect();
      var dx = a.left - b.left, dy = a.top - b.top, sc = a.width / b.width;
      flipping = true;
      bot.style.transition = 'none';
      bot.style.transform  = 'translate(' + dx + 'px,' + dy + 'px) scale(' + sc + ')';
      requestAnimationFrame(function(){
        bot.style.transition = 'transform .75s cubic-bezier(.34,1.3,.5,1)';
        bot.style.transform  = '';
        setTimeout(function(){ bot.style.transition = ''; flipping = false; }, 780);
      });
    }

    /* ---------- المشي مع السكرول ---------- */
    function walk(){
      if (docked || reduced) return;
      var h = document.documentElement.scrollHeight - window.innerHeight;
      var p = h > 0 ? Math.min(1, Math.max(0, window.scrollY / h)) : 0;
      var max = window.innerWidth - bot.offsetWidth - 44;
      bot.style.insetInlineStart = (22 + p * max) + 'px';
      bot.classList.add('rolling');
      clearTimeout(rollTimer);
      rollTimer = setTimeout(function(){ bot.classList.remove('rolling'); }, 340);
    }

    /* ---------- يعلّق على القسم اللي انت فيه ---------- */
    if ('IntersectionObserver' in window){
      var secs = [].slice.call(document.querySelectorAll('section')).filter(function(s){
        return s.querySelector('h2');
      });
      var sio = new IntersectionObserver(function(es){
        es.forEach(function(e){
          if (!e.isIntersecting || docked) return;
          if (Date.now() - lastTalk < 7000) return;
          var h = e.target.querySelector('h2');
          if (h) say(h.textContent.trim().replace(/\s+/g, ' '), 2600);
        });
      }, { threshold: .45 });
      secs.forEach(function(s){ sio.observe(s); });
    }

    /* ---------- الالتحام بالترمينال ---------- */
    if (term){
      bot.style.insetInlineStart = '';
      moveTo(true);
      if ('IntersectionObserver' in window){
        new IntersectionObserver(function(es){
          var vis = es[0].isIntersecting && es[0].intersectionRatio > .35;
          moveTo(vis);
          if (!vis) walk();
        }, { threshold: [0, .35, .7] }).observe(term);
      }
      // يلوّح لما تعدّي على أي زرار وهو في الترمينال
      document.querySelectorAll('.btn').forEach(function(b){
        b.addEventListener('mouseenter', function(){
          if (!docked || reduced) return;
          bot.classList.add('waving');
          setTimeout(function(){ bot.classList.remove('waving'); }, 1750);
        });
      });
      setTimeout(function(){ say(GREET[page] || GREET.home, 3600); }, 1100);
    } else {
      setTimeout(function(){ say(GREET[page] || GREET.home, 3600); }, 900);
    }

    window.addEventListener('scroll', function(){
      requestAnimationFrame(walk);
    }, { passive: true });
    window.addEventListener('resize', walk);

    /* ---------- كلمة كل شوية لو مفيش تفاعل ---------- */
    setInterval(function(){
      if (document.hidden || docked) return;
      if (Date.now() - lastTalk > 42000) say(pick(IDLE), 2800);
    }, 12000);
  })();


  /* ============================================================
     محرك المحادثة — مطابقة عربية محلية
     ============================================================ */
  var Chat = (function(){
    var KB = window.BOT_KB;
    if (!KB) return null;

    var panel = document.getElementById('chat');
    var log   = document.getElementById('chatLog');
    var chips = document.getElementById('chatChips');
    var form  = document.getElementById('chatForm');
    var input = document.getElementById('chatInput');
    var close = document.getElementById('chatClose');
    if (!panel) return null;
    panel.hidden = false;

    /* ---------- تطبيع النص العربي ---------- */
    function norm(t){
      return (t || '')
        .replace(/[ً-ْٰـ]/g, '')   // تشكيل وتطويل
        .replace(/[أإآٱ]/g, 'ا')
        .replace(/ى/g, 'ي').replace(/ئ/g, 'ي')
        .replace(/ة/g, 'ه').replace(/ؤ/g, 'و')
        .replace(/[^ء-يa-zA-Z0-9\s]/g, ' ')
        .toLowerCase()
        .replace(/\s+/g, ' ')
        .trim();
    }
    var STOP = norm('في من على عن الى الي مع هو هي ما ايه ازاي انا انت هل ال و يا ممكن عايز عاوز لو كان بقى بقا ده دي دا كده ولا كمان برضه');
    var STOPS = STOP.split(' ');

    function stem(w){
      if (w.length > 4) w = w.replace(/^(بال|كال|فال|وال|لل|ال)/, '');
      if (w.length > 4) w = w.replace(/(ات|ين|ون|ها|هم|كم|نا|ية|ك|ي|ه)$/, '');
      return w;
    }
    function words(t){
      return norm(t).split(' ').filter(function(w){
        return w.length > 1 && STOPS.indexOf(w) === -1;
      }).map(stem);
    }

    /* ---------- الفهرس + وزن الندرة (IDF) ---------- */
    var INDEX = KB.topics.map(function(t){
      var seen = {}, keys = [];
      words(t.k).forEach(function(k){ if (!seen[k]){ seen[k] = 1; keys.push(k); } });
      return { t: t, keys: keys };
    });
    var DF = {};
    INDEX.forEach(function(it){ it.keys.forEach(function(k){ DF[k] = (DF[k] || 0) + 1; }); });
    var N = INDEX.length;
    function idf(k){ return Math.log(N / (DF[k] || 1)) + 1; }

    /* تشابه كلمتين */
    function sim(w, k){
      if (w === k) return 1;
      if (w.length < 3 || k.length < 3) return 0;
      var lo = Math.min(w.length, k.length), hi = Math.max(w.length, k.length);
      if (hi - lo > 3) return 0;
      if (w.indexOf(k) === 0 || k.indexOf(w) === 0) return lo / hi;
      if (w.indexOf(k) > -1 || k.indexOf(w) > -1) return .82 * lo / hi;
      return 0;
    }

    function score(q){
      var qw = words(q);
      if (!qw.length) return null;
      var best = null, bestScore = 0;
      INDEX.forEach(function(item){
        var total = 0;
        qw.forEach(function(w){
          var top = 0, topKey = null;
          item.keys.forEach(function(k){
            var v = sim(w, k);
            if (v > top){ top = v; topKey = k; }
          });
          if (topKey) total += top * idf(topKey);
        });
        var sc = total / qw.length;
        if (sc > bestScore){ bestScore = sc; best = item.t; }
      });
      return bestScore >= 0.5 ? best : null;
    }


    /* ============================================================
       مهارات حيّة — الوقت والطقس
       ============================================================ */
    /* الاسم المعروض ← [خط العرض، خط الطول] */
    var CITIES = {
      'القاهرة':[30.04,31.24],'الإسكندرية':[31.20,29.92],'الجيزة':[30.01,31.21],
      'المنصورة':[31.04,31.38],'طنطا':[30.79,31.00],'أسيوط':[27.18,31.18],
      'الأقصر':[25.69,32.64],'أسوان':[24.09,32.90],'بورسعيد':[31.26,32.30],'السويس':[29.97,32.53],
      'الغردقة':[27.26,33.81],'شرم الشيخ':[27.92,34.33],'دمياط':[31.42,31.81],'الفيوم':[29.31,30.84],
      'الإسماعيلية':[30.60,32.27],'بني سويف':[29.07,31.10],'المنيا':[28.09,30.75],'سوهاج':[26.56,31.70],
      'قنا':[26.16,32.72],'مرسى مطروح':[31.35,27.24],'العريش':[31.13,33.80],'الساحل الشمالي':[30.90,28.90],
      'دبي':[25.20,55.27],'أبوظبي':[24.45,54.38],'الشارقة':[25.35,55.39],
      'الرياض':[24.71,46.68],'جدة':[21.49,39.19],'مكة':[21.39,39.86],'المدينة المنورة':[24.52,39.57],
      'الدمام':[26.42,50.09],'الكويت':[29.38,47.99],'الدوحة':[25.29,51.53],'المنامة':[26.23,50.59],
      'مسقط':[23.59,58.41],'بيروت':[33.89,35.50],'عمّان':[31.95,35.93],'بغداد':[33.31,44.36],
      'دمشق':[33.51,36.29],'الخرطوم':[15.50,32.56],'تونس':[36.81,10.18],'الجزائر':[36.75,3.06],
      'الرباط':[34.02,-6.83],'الدار البيضاء':[33.57,-7.59],'طرابلس':[32.89,13.19],'صنعاء':[15.37,44.19],
      'إسطنبول':[41.01,28.98],'لندن':[51.51,-0.13]
    };
    var WMO = {
      0:['صافي','☀️'],1:['صافي غالبًا','🌤️'],2:['غيوم متفرقة','⛅'],3:['غائم','☁️'],
      45:['شبورة','🌫️'],48:['شبورة كثيفة','🌫️'],
      51:['رذاذ خفيف','🌦️'],53:['رذاذ','🌦️'],55:['رذاذ كثيف','🌦️'],
      56:['رذاذ متجمد','🌧️'],57:['رذاذ متجمد كثيف','🌧️'],
      61:['مطر خفيف','🌧️'],63:['مطر','🌧️'],65:['مطر غزير','⛈️'],
      66:['مطر متجمد','🌧️'],67:['مطر متجمد غزير','🌧️'],
      71:['ثلج خفيف','🌨️'],73:['ثلج','🌨️'],75:['ثلج كثيف','❄️'],77:['حبيبات ثلج','🌨️'],
      80:['زخات مطر','🌦️'],81:['زخات مطر قوية','🌧️'],82:['زخات عنيفة','⛈️'],
      85:['زخات ثلج','🌨️'],86:['زخات ثلج قوية','❄️'],
      95:['عاصفة رعدية','⛈️'],96:['رعدية مع بَرَد','⛈️'],99:['رعدية عنيفة','⛈️']
    };

    /* ---------- الوقت والتاريخ ---------- */
    function skillTime(){
      var d = new Date(), h = d.getHours();
      var greet = h < 5 ? 'ليلة سعيدة 🌙' : h < 12 ? 'صباح الخير ☀️'
                : h < 17 ? 'نهارك سعيد 🌤️' : h < 21 ? 'مساء الخير 🌆' : 'مساء الخير 🌙';
      var f = function(o){ try { return new Intl.DateTimeFormat('ar-EG', o).format(d); } catch(e){ return ''; } };
      var hijri = '';
      try { hijri = new Intl.DateTimeFormat('ar-EG-u-ca-islamic', { day:'numeric', month:'long', year:'numeric' }).format(d); } catch(e){}
      return {
        a: greet + '<br>' +
           '🕐 الساعة دلوقتي <b>' + f({ hour:'numeric', minute:'2-digit' }) + '</b><br>' +
           '📅 ' + f({ weekday:'long', day:'numeric', month:'long', year:'numeric' }) +
           (hijri ? '<br><small>الموافق ' + hijri + '</small>' : '') +
           '<br><small>حسب ساعة جهازك.</small>',
        c: ['الطقس عامل إيه؟', 'إيه الخدمات؟', 'تواصل']
      };
    }

    /* ---------- الطقس ---------- */
    function findCity(raw){
      var m = raw.match(/(?:في|فى|ب)\s+([^\?\.،]{2,30})\s*$/);
      var name = m ? m[1].trim() : '';
      if (!name) return { name:'القاهرة', lat:30.04, lon:31.24 };
      var n = norm(name).replace(/^ال/, '');
      for (var key in CITIES){
        var k = norm(key).replace(/^ال/, '');
        if (k === n || k.indexOf(n) === 0 || n.indexOf(k) === 0)
          return { name:key, lat:CITIES[key][0], lon:CITIES[key][1] };
      }
      return { name:name, lat:null, lon:null, q:name };
    }

    function skillWeather(raw){
      var city = findCity(raw);
      var geo = city.lat !== null ? Promise.resolve(city) :
        fetch('https://geocoding-api.open-meteo.com/v1/search?count=1&language=ar&format=json&name=' +
              encodeURIComponent(city.q))
          .then(function(r){ return r.json(); })
          .then(function(j){
            if (!j.results || !j.results.length) throw new Error('no city');
            return { name: j.results[0].name, lat: j.results[0].latitude, lon: j.results[0].longitude };
          });

      return geo.then(function(c){
        return fetch('https://api.open-meteo.com/v1/forecast?timezone=auto&forecast_days=1' +
                     '&current=temperature_2m,apparent_temperature,relative_humidity_2m,weather_code,wind_speed_10m' +
                     '&daily=temperature_2m_max,temperature_2m_min' +
                     '&latitude=' + c.lat + '&longitude=' + c.lon)
          .then(function(r){ return r.json(); })
          .then(function(j){
            var cur = j.current, day = j.daily;
            var w = WMO[cur.weather_code] || ['—','🌡️'];
            return {
              a: w[1] + ' الطقس في <b>' + c.name + '</b> دلوقتي: <b>' + Math.round(cur.temperature_2m) + '°</b> — ' + w[0] + '<br>' +
                 '• الإحساس الفعلي: ' + Math.round(cur.apparent_temperature) + '°<br>' +
                 '• الرطوبة: ' + cur.relative_humidity_2m + '%<br>' +
                 '• الرياح: ' + Math.round(cur.wind_speed_10m) + ' كم/س<br>' +
                 '• النهارده: من ' + Math.round(day.temperature_2m_min[0]) + '° إلى ' + Math.round(day.temperature_2m_max[0]) + '°<br>' +
                 '<small>البيانات من Open-Meteo — مجانية ومن غير حساب.</small>',
              c: ['كام الساعة؟', 'الطقس في الإسكندرية', 'إيه الخدمات؟']
            };
          });
      }).catch(function(){
        return {
          a: 'مقدرتش أجيب الطقس دلوقتي — يا إما الإنترنت واقف، يا إما المدينة دي مش معروفة عندي.<br>' +
             'جرّب تكتب اسم المدينة كده: <b>الطقس في الإسكندرية</b>',
          c: ['كام الساعة؟', 'إيه الخدمات؟']
        };
      });
    }

    /* ---------- البحث في النت ---------- */
    function skillSearch(raw){
      var m = raw.match(/(?:ابحث|بحث|دور|اسال جوجل|سيرش|search)(?:\s*(?:لي|لى|عن|على|علي|فى|في))*\s*(.+)$/i);
      var q = m ? m[1].trim().replace(/[\?\.،]+$/, '') : '';
      if (!q) return {
        a: 'أنا مقدرش أبحث في النت — أنا شغّال جوه الموقع من غير أي سيرفر ورايا.<br>' +
           'بس أعرف كل حاجة عن شغل محمد. اسألني عن الخدمات أو الأسعار أو المشاريع.',
        c: KB.starters
      };
      var g = 'https://www.google.com/search?q=' + encodeURIComponent(q);
      return {
        a: 'مقدرش أجيب نتايج البحث بنفسي — الموقع ده ملفات ساكنة من غير سيرفر، ومحركات البحث مبتسمحش بده مباشرة من المتصفح.<br>' +
           'بس جهّزتلك البحث: <a href="' + g + '" target="_blank" rel="noopener">ابحث عن «' + q.replace(/[<>]/g,'') + '» في جوجل ↗</a><br>' +
           '<small>ولو سؤالك عن شغل محمد، اسألني أنا وهجاوبك على طول.</small>',
        c: KB.starters
      };
    }

    var SKILLS = [
      { re: /(كام الساعه|الساعه كام|الساعه|الوقت|التاريخ|النهارده|انهارده|يوم كام|التقويم|هجري|تاريخ ايه)/, run: skillTime },
      { re: /(الطقس|طقس|الجو|الحراره|درجه الحراره|weather|مطر|هتمطر|شمس|برد)/,                            run: skillWeather },
      { re: /(ابحث|بحث|سيرش|search|جوجل|دور على|دورلي)/,                                                  run: skillSearch }
    ];
    function matchSkill(q){
      var n = norm(q);
      for (var i = 0; i < SKILLS.length; i++) if (SKILLS[i].re.test(n)) return SKILLS[i].run;
      return null;
    }

    /* ---------- الواجهة ---------- */
    function bubble(html, who){
      var d = document.createElement('div');
      d.className = 'msg from-' + who;
      d.innerHTML = html;
      log.appendChild(d);
      log.scrollTop = log.scrollHeight;
      return d;
    }
    function setChips(list){
      chips.innerHTML = '';
      (list || []).forEach(function(c){
        var b = document.createElement('button');
        b.type = 'button'; b.className = 'chip'; b.textContent = c;
        b.addEventListener('click', function(){ ask(c); });
        chips.appendChild(b);
      });
    }
    function thinking(){
      var d = document.createElement('div');
      d.className = 'msg from-bot typing';
      d.innerHTML = '<span></span><span></span><span></span>';
      log.appendChild(d); log.scrollTop = log.scrollHeight;
      return d;
    }

    function reply(q){
      var dots = thinking();
      function done(ans, cs){
        dots.remove();
        bubble(ans, 'bot');
        setChips(cs && cs.length ? cs : KB.starters);
        requestAnimationFrame(function(){ log.scrollTop = log.scrollHeight; });
      }
      var skill = matchSkill(q);
      if (skill){
        Promise.resolve().then(function(){ return skill(q); })
          .then(function(r){ done(r.a, r.c); })
          .catch(function(){ done('حصلت مشكلة وأنا بجيب المعلومة دي. جرّب تاني بعد شوية.', KB.starters); });
        return;
      }
      var hit = score(q);
      var ans = hit ? hit.a : KB.fallback.a;
      var cs  = hit ? hit.c : KB.fallback.c;
      setTimeout(function(){ done(ans, cs); }, reduced ? 60 : 420 + Math.random() * 340);
    }

    function ask(q){
      q = (q || '').trim();
      if (!q) return;
      bubble(q.replace(/[<>]/g, ''), 'me');
      setChips([]);
      reply(q);
    }

    var started = false;
    function open(){
      panel.classList.add('open');
      document.getElementById('bot').classList.add('chatting');
      if (!started){
        started = true;
        var hi = KB.hello[Math.floor(Math.random() * KB.hello.length)];
        setTimeout(function(){ bubble(hi, 'bot'); setChips(KB.starters); }, 260);
      }
      setTimeout(function(){ if (window.innerWidth > 560) input.focus(); }, 340);
    }
    function shut(){
      panel.classList.remove('open');
      document.getElementById('bot').classList.remove('chatting');
    }
    function toggle(){ panel.classList.contains('open') ? shut() : open(); }

    form.addEventListener('submit', function(e){
      e.preventDefault(); ask(input.value); input.value = '';
    });
    close.addEventListener('click', shut);
    document.addEventListener('keydown', function(e){
      if (e.key === 'Escape' && panel.classList.contains('open')) shut();
    });

    return { open: open, shut: shut, toggle: toggle, ask: ask };
  })();
  window.Chat = Chat;

  /* ---------- current year ---------- */
  document.querySelectorAll('[data-year]').forEach(function (el) {
    el.textContent = new Date().getFullYear();
  });
})();
