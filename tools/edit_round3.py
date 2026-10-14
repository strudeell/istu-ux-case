"""Правки по замечаниям (раунд 3)."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def patch(rel, pairs):
    p = ROOT / rel
    s = p.read_text(encoding="utf8")
    for a, b in pairs:
        assert a in s, (rel, a[:70])
        s = s.replace(a, b)
    p.write_text(s, encoding="utf8")


patch("index.html", [
    # логотип: обычные буквы UX
    ('      <img src="assets/icons/favicon.svg" alt="" width="28" height="28">\n',
     '      <span class="topbar__badge" aria-hidden="true">UX</span>\n'),
    # резюме — страница просмотра на сайте
    ('href="https://disk.yandex.ru/d/Ne2PoKA05DAAwA" target="_blank" rel="noopener">Резюме',
     'href="resume.html">Резюме'),
    # подсказка «листайте»: стрелки после текста, без «тумблера»
    ('<p class="swipe-hint" aria-hidden="true"><span class="swipe-hint__hand"></span>Листайте экраны</p>',
     '<p class="swipe-hint" aria-hidden="true">Листайте экраны<span class="swipe-hint__arrows"><i></i><i></i><i></i></span></p>'),
    # «Что можно доработать» — короче
    ('''            <b>Добавить чекбокс с русским языком в предметах ЕГЭ, а не учитывать его по умолчанию</b>
            <p>3 из 4 респондентов потратили время, чтобы заметить подсказку о том, что русский язык всегда включён, — лучше вернуть его в список.</p>''',
     '''            <b>Чекбокс «Русский язык» в предметах ЕГЭ</b>
            <p>3 из 4 респондентов не сразу заметили подсказку, что русский учитывается всегда.</p>'''),
    ('''            <b>Добавить подсказку «Подбери по баллам ЕГЭ», которая перенаправляет в фильтры</b>
            <p>Один респондент не догадался, что баллы ЕГЭ находятся в фильтрах. Перед доработкой проверить гипотезу необходимости этой правки.</p>''',
     '''            <b>Подсказка «Подбери по баллам ЕГЭ» со ссылкой на фильтры</b>
            <p>Один респондент не нашёл баллы в фильтрах — гипотезу стоит проверить.</p>'''),
    ('''            <b>Добавить СПО в меню</b>
            <p>Два респондента искали программы для СПО в выпадающем бургер-меню.</p>''',
     '''            <b>СПО в меню</b>
            <p>Двое искали программы СПО в бургер-меню.</p>'''),
    # вайрфреймы: гифки — верхним рядом от верхнего края большой, тексты — под ними на тех же вертикалях
    ('''        <div class="wires__texts">
          <p class="reveal">Следующим шагом после определения дизайн‑концепции стала разработка вайрфреймов (схематичное представление структуры будущего цифрового продукта)</p>
          <p class="reveal" style="--d:.1s">В данном проекте создание чернового варианта стало важнейшим процессом, так как цель — упростить пользовательский путь, а он продумывается именно на этом этапе</p>
        </div>
''', ''),
    ('''        <figure class="wire wire--c reveal" style="--d:.25s"><img src="assets/gif/wf4.gif" alt="Вайрфрейм превращается в готовый дизайн: страница программы" loading="lazy" width="560" height="507"><figcaption><span>Черновик</span><i></i><span>Дизайн</span></figcaption></figure>
''', '''        <figure class="wire wire--c reveal" style="--d:.25s"><img src="assets/gif/wf4.gif" alt="Вайрфрейм превращается в готовый дизайн: страница программы" loading="lazy" width="560" height="507"><figcaption><span>Черновик</span><i></i><span>Дизайн</span></figcaption></figure>
        <p class="wires__t wires__t--1 reveal">Следующим шагом после определения дизайн‑концепции стала разработка вайрфреймов (схематичное представление структуры будущего цифрового продукта)</p>
        <p class="wires__t wires__t--2 reveal" style="--d:.1s">В данном проекте создание чернового варианта стало важнейшим процессом, так как цель — упростить пользовательский путь, а он продумывается именно на этом этапе</p>
'''),
    ('css/base.css?v=2', 'css/base.css?v=3'), ('css/sections.css?v=2', 'css/sections.css?v=3'), ('js/main.js?v=2', 'js/main.js?v=3'),
])

patch("js/main.js", [
    ("ava: ''", "ava: 'artem'"),
])
s = (ROOT / "js/main.js").read_text(encoding="utf8")
for n in ["polina", "olga", "dmitry"]:
    s = s.replace("ava: ''", f"ava: '{n}'", 1)
(ROOT / "js/main.js").write_text(s, encoding="utf8")

patch("css/sections.css", [
    # логотип
    (".topbar__logo b { color: var(--blue); }",
     ".topbar__logo b { color: var(--blue); }\n"
     ".topbar__badge { display: grid; place-items: center; width: 32px; height: 32px; border-radius: 9px; background: var(--grad); color: #fff; font-size: 14px; font-weight: 800; letter-spacing: .02em; }"),
    # вайрфреймы по 12-колоночной сетке: 4 модуля по 3 колонки
    (""".wires__grid { display: grid; grid-template-columns: repeat(4, 1fr); grid-template-rows: 1fr auto; gap: 24px 20px; margin-top: 32px; }
.wires__texts { grid-column: 2 / 5; grid-row: 1; display: grid; grid-template-columns: 1fr 1fr; gap: 20px; font-size: 16px; }
.wires__texts p { max-width: 413px; }
.wires__texts p:nth-child(2) { margin: 119px 0 0 6px; }""",
     """.wires__grid { display: grid; grid-template-columns: repeat(4, 1fr); grid-template-rows: auto 1fr; gap: 32px 20px; margin-top: 32px; }
.wires__t { grid-row: 2; align-self: start; font-size: 16px; line-height: 1.3; padding-top: 18px; border-top: 2px solid var(--blue-tertiary-hover); position: relative; }
.wires__t::before { content: ""; position: absolute; left: 0; top: -2px; width: 48px; height: 2px; background: var(--blue); }
.wires__t--1 { grid-column: 2; }
.wires__t--2 { grid-column: 3; }"""),
    (""".wire--tall { grid-column: 1; grid-row: 1 / 3; }
.wire--a, .wire--b, .wire--c { grid-row: 2; align-self: end; }""",
     """.wire--tall { grid-column: 1; grid-row: 1 / 3; }
.wire--a, .wire--b, .wire--c { grid-row: 1; align-self: start; }"""),
    ("""  .wires__texts { grid-column: 1 / -1; grid-row: auto; }
  .wires__texts p, .wires__texts p:nth-child(2) { margin: 0; max-width: none; }""",
     """  .wires__t { grid-row: auto; grid-column: auto; }
  .wires__t--1 { order: -2; } .wires__t--2 { order: -1; }"""),
    ("  .wires__texts { grid-template-columns: 1fr; }", ""),
    # подсказка «листайте»
    (""".swipe-hint__hand { position: relative; width: 44px; height: 22px; border-radius: 11px; background: var(--blue-tertiary-hover); flex: none; }
.swipe-hint__hand::before { content: ""; position: absolute; left: 4px; top: 4px; width: 14px; height: 14px; border-radius: 50%; background: var(--blue); animation: swipe 1.8s var(--ease) infinite; }
.swipe-hint__hand::after { content: ""; position: absolute; right: -14px; top: 6px; width: 7px; height: 7px; border: solid var(--blue); border-width: 2px 2px 0 0; transform: rotate(45deg); animation: swipeArrow 1.8s ease-in-out infinite; }
@keyframes swipe { 0% { transform: translateX(0); opacity: 0; } 15% { opacity: 1; } 70% { transform: translateX(22px); opacity: 1; } 100% { transform: translateX(22px); opacity: 0; } }
@keyframes swipeArrow { 0%, 100% { translate: 0 0; opacity: .4; } 60% { translate: 4px 0; opacity: 1; } }""",
     """.swipe-hint__arrows { display: inline-flex; gap: 1px; }
.swipe-hint__arrows i { width: 9px; height: 9px; border: solid var(--blue); border-width: 2px 2px 0 0; transform: rotate(45deg); opacity: .2; animation: chev 1.4s ease-in-out infinite; }
.swipe-hint__arrows i:nth-child(2) { animation-delay: .18s; }
.swipe-hint__arrows i:nth-child(3) { animation-delay: .36s; }
@keyframes chev { 0%, 100% { opacity: .2; } 40% { opacity: 1; } }"""),
])

# телефон: на узком экране тексты вайрфреймов — над гифками (до большой)
p = ROOT / "css/sections.css"
s = p.read_text(encoding="utf8")
assert "  .wires__grid { grid-template-columns: 1fr; }" in s
s = s.replace("  .wires__grid { grid-template-columns: 1fr; }", "  .wires__grid { grid-template-columns: 1fr; }\n  .wires__t { padding-top: 14px; }")
p.write_text(s, encoding="utf8")

# favicon: обычные буквы UX
(ROOT / "assets/icons/favicon.svg").write_text(
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><defs><linearGradient id="g" x1="0" x2="1" y1="0" y2="1">'
    '<stop offset="0" stop-color="#1f45ec"/><stop offset="1" stop-color="#1f90ec"/></linearGradient></defs>'
    '<rect width="64" height="64" rx="16" fill="url(#g)"/>'
    '<text x="32" y="42" text-anchor="middle" font-family="Manrope, Arial, Helvetica, sans-serif" font-size="28" font-weight="800" fill="#fff">UX</text></svg>',
    encoding="utf8")
print("ok")
