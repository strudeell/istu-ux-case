(() => {
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => [...r.querySelectorAll(s)];
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---------- Портреты ЦА (данные из макета) ---------- */
  const ICONS = {
    book: '<svg viewBox="0 0 24 24"><path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2zM22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"/></svg>',
    target: '<svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/></svg>',
    cross: '<svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><path d="M22 12h-4M6 12H2M12 6V2M12 22v-4"/></svg>',
    x: '<svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><path d="m15 9-6 6M9 9l6 6"/></svg>'
  };
  const PERSONAS = [
    {
      name: 'Артём', ava: 'artem', info: [['Возраст', '17'], ['Пол', 'Мужской'], ['Статус', 'Ученик 11 класса'], ['ЕГЭ', 'Математика, русский, информатика']],
      about: 'Заканчивает школу и выбирает, куда подавать документы. Хочет учиться в родном городе и поступить на бюджет. Смотрит сайты нескольких вузов по вечерам с телефона и быстро уходит, если не находит ответ',
      goals: ['Найти направления, куда берут с его предметами ЕГЭ', 'Понять, проходит ли он на бюджет со своими баллами', 'Выбрать 2–3 программы для подачи документов'],
      main: [['Скорость', 'ответ за пару действий, без лишних переходов'], ['Лёгкость поиска', 'подбор по своим предметам и баллам'], ['Удобство', 'с телефона']],
      pain: ['Длинные списки и непонятные коды направлений', 'Важные цифры спрятаны глубоко в страницах', 'Мелкий текст, который неудобно читать с телефона']
    },
    {
      name: 'Полина', ava: 'polina', info: [['Возраст', '18'], ['Пол', 'Женский'], ['Статус', 'Студентка 1 курса'], ['Направление', 'Дизайн архитектурной среды']],
      about: 'Поступила туда, куда проходила на бюджет, почти не разбираясь в программах. После первого семестра поняла, что ей интереснее энергетика, и снова открывает каталог, чтобы найти, куда перевестись.',
      goals: ['Найти программы, куда можно перевестись', 'Сравнить новую программу с текущей', 'Узнать, есть ли бюджетные места для перевода'],
      main: [['Понятность', 'сразу видно, чему учат на программе'], ['Сравнение', 'несколько программ рядом'], ['', 'Не проходить поиск каждый раз заново']],
      pain: ['Описание программы спрятано в свёрнутых блоках', 'Нет информации о переводе', 'Поиск приходится начинать сначала']
    },
    {
      name: 'Ольга', ava: 'olga', info: [['Возраст', '46'], ['Пол', 'Женский'], ['Семья', 'Замужем, дочь в 11 классе'], ['Профессия', 'Бухгалтер']],
      about: 'Помогает дочери выбрать вуз и отвечает за семейный бюджет. Смотрит сайт с рабочего компьютера в обед. Ей важно заранее знать, сколько будет стоить учёба, если дочь не пройдёт на бюджет.',
      goals: ['Заранее узнать стоимость года обучения', 'Сравнить цену и срок обучения на разных программах', 'Понять, сколько бюджетных мест и есть ли шанс на бюджет'],
      main: [['Прозрачность цифр', 'цена, срок и места на виду'], ['Лёгкость поиска информации', 'всё в одном месте'], ['', 'Крупный читаемый текст']],
      pain: ['Нельзя сразу отфильтровать по форме обучения', 'Профили одного направления разбросаны по списку', 'Таблицы, которые не помещаются на экране']
    },
    {
      name: 'Дмитрий', ava: 'dmitry', info: [['Возраст', '21'], ['Пол', 'Мужской'], ['Образование', 'Колледж, техник-строитель'], ['Профессия', 'Мастер участка']],
      about: 'Работает на стройке после колледжа и хочет получить диплом бакалавра, чтобы вырасти в должности. Уходить с работы не готов, поэтому ищет очно-заочную форму и платит за учёбу сам.',
      goals: ['Найти программы с очно-заочной формой', 'Узнать цену и срок обучения', 'Выбрать подходящий профиль направления'],
      main: [['Скорость', 'нужная форма обучения находится сразу'], ['Цена на виду', 'сразу понятно, потянет ли он'], ['Удобство', 'с телефона в перерывах']],
      pain: ['Нельзя сразу отфильтровать по форме обучения', 'Профили одного направления разбросаны по списку', 'Таблицы, которые не помещаются на экране']
    }
  ];
  const track = $('#personas');
  if (track) {
    const li = a => a.map(t => `<li>${t}</li>`).join('');
    track.innerHTML = PERSONAS.map((p, i) => `
      <article class="persona reveal" style="--d:${i * .08}s" aria-label="Портрет: ${p.name}">
        <div class="persona__side">
          <div class="persona__ava"><span class="initial">${p.name[0]}</span><img src="assets/img/ava-${p.ava}.webp" alt="${p.name}" loading="lazy" onerror="this.remove()"></div>
          <p class="persona__name">${p.name}</p>
          ${p.info.map(([k, v]) => `<p class="persona__info"><span>${k}:</span>${v}</p>`).join('')}
        </div>
        <div class="persona__main">
          <div class="persona__block persona__block--wide tile"><h4>${ICONS.book}Кратко</h4><p>${p.about}</p></div>
          <div class="persona__block persona__block--wide tile"><h4>${ICONS.target}Цели</h4><ul>${li(p.goals)}</ul></div>
          <div class="persona__block persona__block--pos tile"><h4>${ICONS.cross}Что главное</h4><ul>${li(p.main.map(([b, t]) => b ? `<b>${b}:</b> ${t}` : t))}</ul></div>
          <div class="persona__block persona__block--neg tile"><h4>${ICONS.x}Что мешает</h4><ul>${li(p.pain)}</ul></div>
        </div>
      </article>`).join('');

    // перетаскивание мышью
    let down = false, sx = 0, sl = 0, moved = false;
    track.addEventListener('pointerdown', e => {
      if (e.pointerType !== 'mouse') return;
      down = true; moved = false; sx = e.clientX; sl = track.scrollLeft;
    });
    addEventListener('pointermove', e => {
      if (!down) return;
      const dx = e.clientX - sx;
      if (Math.abs(dx) > 4) { moved = true; track.classList.add('dragging'); }
      track.scrollLeft = sl - dx;
    });
    addEventListener('pointerup', () => {
      if (!down) return;
      down = false;
      track.classList.remove('dragging');
      if (moved) snapTo(nearest());
    });
    const cards = () => $$('.persona', track);
    const nearest = () => {
      const pad = parseFloat(getComputedStyle(track).scrollPaddingLeft) || 0;
      let best = 0, d = Infinity;
      cards().forEach((c, i) => { const v = Math.abs(c.offsetLeft - pad - track.scrollLeft); if (v < d) { d = v; best = i; } });
      return best;
    };
    const snapTo = i => {
      const c = cards()[Math.max(0, Math.min(cards().length - 1, i))];
      const pad = parseFloat(getComputedStyle(track).scrollPaddingLeft) || 0;
      track.scrollTo({ left: c.offsetLeft - pad, behavior: 'smooth' });
    };
    const btns = $$('.slider-btn'), count = $('.slider-count b'), bar = $('.personas__bar span');
    btns.forEach(b => b.addEventListener('click', () => snapTo(nearest() + +b.dataset.dir)));
    track.addEventListener('keydown', e => {
      if (e.key === 'ArrowRight') { e.preventDefault(); snapTo(nearest() + 1); }
      if (e.key === 'ArrowLeft') { e.preventDefault(); snapTo(nearest() - 1); }
    });
    const upd = () => {
      const max = track.scrollWidth - track.clientWidth;
      const p = max > 0 ? track.scrollLeft / max : 0;
      bar.style.transform = `translateX(${p * 300}%)`;
      const i = nearest();
      count.textContent = i + 1;
      btns[0].disabled = track.scrollLeft < 5;
      btns[1].disabled = track.scrollLeft > max - 5;
    };
    track.addEventListener('scroll', upd, { passive: true });
    addEventListener('resize', upd);
    upd();
  }

  /* ---------- индексы для каскадных анимаций ---------- */
  $$('.chips').forEach(c => $$('.chip', c).forEach((el, i) => el.style.setProperty('--i', i)));
  $$('.sitemap').forEach(s => $$('.node, li', s).forEach((el, i) => el.style.setProperty('--i', i)));

  /* ---------- Появление при скролле ---------- */
  const io = new IntersectionObserver(es => es.forEach(e => {
    if (!e.isIntersecting) return;
    e.target.classList.add('in');
    io.unobserve(e.target);
  }), { threshold: .15, rootMargin: '0px 0px -60px 0px' });
  $$('.reveal, .survey__note, .chips-col, .sitemap, .metric').forEach(el => io.observe(el));

  /* ---------- Счётчики ---------- */
  const animateCount = el => {
    const to = el.dataset.to, suf = el.dataset.suffix || '';
    if (reduce) return;
    const dur = 1400, t0 = performance.now();
    const isTime = to.includes(':');
    const target = isTime ? to.split(':').reduce((m, s) => +m * 60 + +s) : +to;
    const from = isTime ? 211 : 0; // 3:31 -> 0:24
    const fmt = v => isTime ? `${Math.floor(v / 60)}:${String(Math.round(v % 60)).padStart(2, '0')}` : Math.round(v) + suf;
    const step = t => {
      const k = Math.min(1, (t - t0) / dur), e = 1 - Math.pow(1 - k, 3);
      el.textContent = fmt(from + (target - from) * e);
      if (k < 1) requestAnimationFrame(step);
    };
    requestAnimationFrame(step);
  };
  const cio = new IntersectionObserver(es => es.forEach(e => {
    if (e.isIntersecting) { animateCount(e.target); cio.unobserve(e.target); }
  }), { threshold: .6 });
  $$('.count').forEach(el => cio.observe(el));

  /* ---------- AS IS: клики рисуются по мере прокрутки ---------- */
  const flow = $('#flow');
  if (flow) {
    const paths = $$('.flow__arrows path', flow);
    const caps = $$('.flow__cap', flow);
    const num = $('.flow__num', flow), counter = $('.flow__counter', flow);
    paths.forEach(p => p.setAttribute('pathLength', '1'));
    // для мобильной версии — те же шаги нумерованным списком под лентой скриншотов
    const ol = document.createElement('ol');
    ol.className = 'flow__steps';
    ol.innerHTML = caps.slice().sort((a, b) => a.dataset.step - b.dataset.step).map(c => `<li><span>${c.innerHTML}</span></li>`).join('');
    flow.appendChild(ol);
    let shown = -1;
    const onScroll = () => {
      const r = flow.getBoundingClientRect(), vh = innerHeight;
      flow.classList.toggle('in-view', r.top < vh * .7 && r.bottom > vh * .3);
      const p = Math.min(1, Math.max(0, (vh * .75 - r.top) / (r.height * .85)));
      const n = reduce ? 9 : Math.round(p * 9);
      if (n === shown) return;
      shown = n;
      paths.forEach(el => el.classList.toggle('on', +el.dataset.step <= n));
      caps.forEach(el => el.classList.toggle('on', +el.dataset.step <= n));
      num.textContent = n;
      counter.classList.toggle('done', n === 9);
    };
    addEventListener('scroll', onScroll, { passive: true });
    onScroll();
  }

  /* ---------- Шапка, прогресс, активный пункт, параллакс ---------- */
  const topbar = $('#topbar'), prog = $('.progress span'), hero = $('.hero');
  const par = $$('[data-parallax]');
  const links = $$('.topbar__nav a');
  const secs = links.map(a => $(a.getAttribute('href')));
  let ticking = false;
  const onFrame = () => {
    ticking = false;
    const y = scrollY, h = document.documentElement.scrollHeight - innerHeight;
    prog.style.transform = `scaleX(${h > 0 ? y / h : 0})`;
    topbar.classList.toggle('show', y > hero.offsetHeight - 80);
    if (!reduce) par.forEach(el => { if (y < hero.offsetHeight) el.style.transform = `translateY(${y * el.dataset.parallax}px)`; });
    let act = -1;
    secs.forEach((s, i) => { if (s && s.getBoundingClientRect().top < innerHeight * .4) act = i; });
    links.forEach((a, i) => a.classList.toggle('active', i === act));
  };
  addEventListener('scroll', () => { if (!ticking) { ticking = true; requestAnimationFrame(onFrame); } }, { passive: true });
  onFrame();

  /* ---------- Видео: играют, только когда видны ---------- */
  const vio = new IntersectionObserver(es => es.forEach(e => {
    const v = e.target;
    if (e.isIntersecting) {
      if (v.preload === 'none') { v.preload = 'auto'; }
      if (!v.dataset.userPaused) v.play().catch(() => {});
    } else v.pause();
  }), { threshold: .35 });
  $$('video.autoplay').forEach(v => {
    vio.observe(v);
    const btn = v.parentElement.querySelector('.device__play');
    const sync = () => { btn.classList.toggle('paused', v.paused); btn.setAttribute('aria-label', v.paused ? 'Воспроизвести' : 'Пауза'); };
    v.addEventListener('play', sync); v.addEventListener('pause', sync);
    btn.addEventListener('click', () => {
      if (v.paused) { delete v.dataset.userPaused; v.play(); } else { v.dataset.userPaused = 1; v.pause(); }
    });
  });

  /* ---------- Лайтбокс ---------- */
  const lb = $('#lightbox'), lbImg = $('img', lb);
  const close = () => { lb.hidden = true; document.body.style.overflow = ''; };
  $$('.zoomable').forEach(b => b.addEventListener('click', () => {
    lbImg.src = b.dataset.full; lbImg.alt = $('img', b).alt;
    lb.hidden = false; document.body.style.overflow = 'hidden';
  }));
  lb.addEventListener('click', close);
  addEventListener('keydown', e => { if (e.key === 'Escape' && !lb.hidden) close(); });

  /* ---------- Копирование цвета / почты ---------- */
  const toast = $('#toast');
  let tt;
  const say = t => { toast.textContent = t; toast.classList.add('show'); clearTimeout(tt); tt = setTimeout(() => toast.classList.remove('show'), 1800); };
  const copy = (txt, msg) => (navigator.clipboard ? navigator.clipboard.writeText(txt) : Promise.reject()).then(() => say(msg), () => say(txt));
  $$('.swatch').forEach(s => s.addEventListener('click', () => copy(s.dataset.hex, `Скопировано: ${s.dataset.hex}`)));
  $$('.copy').forEach(b => b.addEventListener('click', () => copy(b.dataset.copy, 'Почта скопирована')));
})();
