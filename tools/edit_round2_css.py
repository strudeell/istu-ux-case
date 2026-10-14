"""Правки по замечаниям (раунд 2): стили."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
css = ROOT / "css" / "sections.css"
s = css.read_text(encoding="utf8")


def block(start, end_incl):
    """Заменяемый диапазон строк: от строки, начинающейся с start, до строки, начинающейся с end_incl (включительно)."""
    lines = s.split("\n")
    i = next(k for k, l in enumerate(lines) if l.startswith(start))
    j = next(k for k in range(i, len(lines)) if lines[k].startswith(end_incl))
    return "\n".join(lines[i:j + 1])


def rep(a, b):
    global s
    assert a in s, a[:80]
    s = s.replace(a, b, 1)


# ---------- Анализ ЦА: раскрывающиеся пункты ----------
rep(block(".ca__grid {", ".orbit__item:nth-of-type(3) i::after"), """.ca__grid { display: grid; grid-template-columns: 1fr 1fr; gap: 40px; margin-top: 32px; }
.orbit { display: flex; align-items: center; gap: 24px; min-width: 0; }
.orbit__label { flex: none; letter-spacing: .04em; white-space: nowrap; }
.orbit .h-xl.orbit__label { width: 94px; }
.orbit__items { position: relative; height: 300px; flex: 1; min-width: 0; }
.orbit__arc { position: absolute; left: 18px; top: 19px; width: 45px; height: 219px; overflow: visible; }
.orbit__arc path { fill: none; stroke: rgba(31, 144, 236, .18); stroke-width: 1.5; stroke-dasharray: 260; stroke-dashoffset: 260; transition: stroke-dashoffset 1.4s var(--ease) .3s; }
.orbit.in .orbit__arc path { stroke-dashoffset: 0; }
.orbit__item {
  position: absolute; left: 0; right: 0; display: flex; align-items: flex-start; gap: 28px; padding: 10px; text-align: left;
  opacity: 0; transform: translateX(20px); transition: opacity .6s, transform .6s var(--ease);
  -webkit-tap-highlight-color: transparent;
}
.orbit__item:nth-of-type(1) { top: 0; transition-delay: .4s; }
.orbit__item:nth-of-type(2) { top: 109px; left: 40px; transition-delay: .6s; }
.orbit__item:nth-of-type(3) { top: 218px; transition-delay: .8s; }
.orbit.in .orbit__item { opacity: 1; transform: none; }
.orbit__item i {
  position: relative; width: 15px; height: 15px; margin: 4.5px; border-radius: 50%; flex: none;
  background: rgba(31, 144, 236, .9); box-shadow: 0 2px 6px rgba(31, 144, 236, .45), inset 0 1px 2px rgba(255, 255, 255, .6);
  transform: scale(.55); transition: transform .45s var(--ease);
}
.orbit__item i::after { content: ""; position: absolute; inset: -6px; border-radius: 50%; border: 2px solid var(--blue); opacity: 0; }
.orbit__item.on i { transform: scale(1.1); }
.orbit__item.on i::after { animation: ping 1.6s ease-out infinite; }
.orbit__text { min-width: 0; }
.orbit__text b { display: block; font-size: 16px; font-weight: 600; color: var(--blue-hover); transition: font-size .4s var(--ease); }
.orbit__item.on .orbit__text b { font-size: 20px; font-weight: 700; }
.orbit__text small {
  display: block; max-width: 300px; font-size: 14px; line-height: 1.3; color: var(--text-muted);
  max-height: 0; opacity: 0; overflow: hidden; transition: max-height .5s var(--ease), opacity .4s, margin .4s var(--ease);
}
.orbit__item.on .orbit__text small { max-height: 60px; opacity: 1; margin-top: 6px; }""")

# ---------- Инсайты: раскрывающийся список ----------
rep(block(".insights__list {", ".insights__list b::after"), """.insights__list { list-style: none; padding: 0; display: grid; gap: 16px; font-size: 16px; counter-reset: i; }
.insights__list li { counter-increment: i; }
.insights__list li::before { content: counter(i) ". "; font-weight: 500; }
.insights__list b { font-weight: 500; display: inline; }
.insights__list b::after { content: ""; display: block; }
.insights__more { display: grid; grid-template-rows: 0fr; transition: grid-template-rows .6s var(--ease); }
.insights__more > div { overflow: hidden; }
.insights__more .insights__list { counter-reset: i 3; padding-top: 16px; }
.insights__more li { opacity: 0; transform: translateY(12px); transition: opacity .4s, transform .5s var(--ease); }
.insights__more.open { grid-template-rows: 1fr; }
.insights__more.open li { opacity: 1; transform: none; }
.insights__more.open li:nth-child(2) { transition-delay: .08s; }
.insights__more.open li:nth-child(3) { transition-delay: .16s; }
.insights__toggle { margin-top: 18px; font-size: 16px; }
.insights__toggle::after { content: "↓"; }
.insights__toggle[aria-expanded="true"]::after { transform: rotate(180deg); }
.links-row { display: flex; flex-wrap: wrap; align-items: center; gap: 16px 24px; margin: 32px 0; }
.link-folder { display: inline-flex; align-items: center; gap: 8px; font-weight: 600; color: var(--blue-hover); border-bottom: 1px dashed transparent; padding: 4px 0; transition: border-color .25s; }
.link-folder svg { width: 20px; height: 20px; fill: none; stroke: currentColor; stroke-width: 1.8; stroke-linejoin: round; }""")

# ---------- Чипсы: без «подвисания» при наведении ----------
rep(".chip:hover { transform: translateY(-3px) !important; background: var(--blue-hover); color: #fff; }",
    ".chip:hover { transform: translateY(-3px); background: var(--blue-hover); color: #fff; }")
rep(".chips-col.in .chip { animation: pop .5s var(--ease) forwards; animation-delay: calc(var(--i) * 60ms + .2s); }",
    ".chips-col.in .chip { animation: pop .5s var(--ease) backwards; animation-delay: calc(var(--i) * 60ms + .2s); opacity: 1; transform: none; }")

# ---------- Вайрфреймы: тексты отдельно сверху, гифки не разрываются текстом ----------
rep(block(".wires__grid {", ".wire--a { grid-column: 2; }"), """.wires__grid { display: grid; grid-template-columns: repeat(4, 1fr); grid-template-rows: 1fr auto; gap: 24px 20px; margin-top: 32px; }
.wires__texts { grid-column: 2 / 5; grid-row: 1; display: grid; grid-template-columns: 1fr 1fr; gap: 20px; font-size: 16px; }
.wires__texts p { max-width: 413px; }
.wires__texts p:nth-child(2) { margin: 119px 0 0 6px; }
.wire { margin: 0; position: relative; border-radius: 10px; overflow: hidden; background: #fff; box-shadow: var(--shadow-200); }
.wire img { width: 100%; height: auto; }
.wire--tall { grid-column: 1; grid-row: 1 / 3; }
.wire--a, .wire--b, .wire--c { grid-row: 2; align-self: end; }
.wire--a { grid-column: 2; } .wire--b { grid-column: 3; } .wire--c { grid-column: 4; }""")

# ---------- Навигация: задержка только у появления, наведение мгновенное ----------
s = re.sub(r"\.sitemap__cols li, \.node \{\n(.*?)\n\}", lambda m: """.sitemap__cols li, .node {
  position: relative; display: flex; align-items: center; min-height: 43px; padding: 12px; border-radius: 8px; background: #fff; font-size: 16px;
  opacity: 0; transform: translateY(14px);
  transition: opacity .5s var(--sd, 0s), transform .5s var(--ease) var(--sd, 0s), background .2s, color .2s, box-shadow .2s;
}""", s, count=1, flags=re.S)
rep(".sitemap.in .node, .sitemap.in li { opacity: 1; transform: none; transition-delay: calc(var(--i) * 35ms); }",
    """.sitemap .node, .sitemap li { --sd: calc(var(--i) * 30ms); }
.sitemap.in .node, .sitemap.in li { opacity: 1; transform: none; }
/* ключевой путь пользователя: «Поступающим» -> «Образовательные программы» */
.sitemap.in .sitemap__top .node:nth-child(3) { animation: keyNode .6s var(--ease) 1.4s forwards; }
.sitemap.in .sitemap__cols li.hl { animation: keyPulse 2.4s ease-in-out 2s infinite; }
@keyframes keyNode { to { background: var(--blue); color: #fff; } }
@keyframes keyPulse { 0%, 100% { box-shadow: inset 0 0 0 2px var(--blue), 0 0 0 0 rgba(31, 144, 236, .35); } 50% { box-shadow: inset 0 0 0 2px var(--blue), 0 0 0 8px rgba(31, 144, 236, 0); } }""")

# ---------- Видео с компьютера: родные пропорции, без обрезки ----------
rep(".result__videos { display: grid; grid-template-columns: 847px 1fr; gap: 20px; margin-top: 32px; align-items: stretch; }",
    ".result__videos { display: grid; grid-template-columns: 847px 1fr; gap: 20px; margin-top: 32px; align-items: center; }")
rep(".device--laptop video { aspect-ratio: 16 / 9; height: auto; flex: 1; }",
    ".device--laptop video { aspect-ratio: 16 / 9; height: auto; flex: none; object-fit: contain; }")

# ---------- Восприятие и доработки: одна сетка, одинаковая высота карточек ----------
rep(block(".perception {", ".quotes {"), """.perception { display: grid; grid-template-columns: repeat(3, 1fr); grid-template-rows: auto 1fr; gap: 20px; align-items: stretch; }
.perception__h1 { grid-column: 1 / 3; }
.perception__h2 { grid-column: 3; font-weight: 700; }
.quotes { padding: 17px; border: 1px solid #d9d9d9; border-radius: var(--r); display: grid; gap: 12px; align-content: start; background: rgba(255, 255, 255, .4); }""")
rep(".todo h3 { font-weight: 700; margin-bottom: 32px; }",
    ".todo { padding: 17px; border: 1px dashed var(--blue-secondary-hover); border-radius: var(--r); background: #fff; display: grid; gap: 14px; align-content: start; }")
rep(".todo__item { max-width: 384px; padding: 0 0 16px 16px; position: relative; font-size: 16px; }",
    ".todo__item { padding: 0 0 0 18px; position: relative; font-size: 16px; }")

# ---------- адаптив: планшет ----------
rep("  .result__videos, .perception { grid-template-columns: 2fr 1fr; }", "  .result__videos { grid-template-columns: 2fr 1fr; }")
rep("""  .wires__grid { grid-template-columns: 1fr 1fr; gap: 20px; }
  .wire--tall { grid-row: auto; grid-column: 1 / -1; max-width: 420px; justify-self: center; }
  .wires__t1, .wires__t2 { grid-column: auto; margin: 0; max-width: none; }
  .wire--a, .wire--b, .wire--c { grid-row: auto; grid-column: auto; margin: 0; }""", """  .wires__grid { grid-template-columns: 1fr 1fr; grid-template-rows: none; gap: 20px; }
  .wires__texts { grid-column: 1 / -1; grid-row: auto; }
  .wires__texts p, .wires__texts p:nth-child(2) { margin: 0; max-width: none; }
  .wire--tall { grid-row: auto; grid-column: 1 / -1; max-width: 420px; justify-self: center; }
  .wire--a, .wire--b, .wire--c { grid-row: auto; grid-column: auto; margin: 0; }""")
rep("  .perception { grid-template-columns: 1fr; gap: 40px; }", """  .perception { grid-template-columns: 1fr 1fr; grid-template-rows: none; }
  .perception__h1 { grid-column: 1 / -1; }
  .perception__h2 { grid-column: 1 / -1; order: 4; margin-top: 20px; }
  .todo { grid-column: 1 / -1; order: 5; }""")

# ---------- адаптив: телефон ----------
rep("""  .orbit__items { width: 100%; flex: none; height: 262px; }
  .orbit__item { font-size: 16px; gap: 28px; }""", """  .orbit__items { width: 100%; flex: none; height: 330px; }
  .orbit__item { gap: 18px; }
  .orbit__item:nth-of-type(2) { top: 115px; left: 28px; }
  .orbit__item:nth-of-type(3) { top: 230px; }
  .orbit__item.on .orbit__text b { font-size: 18px; }
  .orbit__text small { max-width: none; }
  .orbit__item.on .orbit__text small { max-height: 80px; }""")
rep("  .wires__grid { grid-template-columns: 1fr; }", "  .wires__grid { grid-template-columns: 1fr; }\n  .wires__texts { grid-template-columns: 1fr; }")
rep("  .perception__cols { grid-template-columns: 1fr; }", """  .perception { grid-template-columns: 1fr; }
  .chip { background: var(--blue-secondary); color: var(--text); }
  .chip:nth-child(even) { background: var(--blue); color: #fff; }
  .reveal.from-left, .reveal.from-right { transform: translateY(30px); }
  .reveal.in.from-left, .reveal.in.from-right { transform: none; }
  .swipe-hint { display: flex; }
  .flow__canvas { -webkit-mask-image: linear-gradient(90deg, #000 80%, transparent); mask-image: linear-gradient(90deg, #000 80%, transparent); }
  .flow__canvas.at-end { -webkit-mask-image: none; mask-image: none; }
  .links-row { gap: 12px; }
  .links-row .btn { width: 100%; }""")

# ---------- подсказка «листайте» ----------
rep("/* ============ Анализ ЦА ============ */", """.swipe-hint { display: none; align-items: center; gap: 12px; margin: 0 0 12px; font-size: 14px; font-weight: 600; color: var(--blue-hover); }
.swipe-hint__hand { position: relative; width: 44px; height: 22px; border-radius: 11px; background: var(--blue-tertiary-hover); flex: none; }
.swipe-hint__hand::before { content: ""; position: absolute; left: 4px; top: 4px; width: 14px; height: 14px; border-radius: 50%; background: var(--blue); animation: swipe 1.8s var(--ease) infinite; }
.swipe-hint__hand::after { content: ""; position: absolute; right: -14px; top: 6px; width: 7px; height: 7px; border: solid var(--blue); border-width: 2px 2px 0 0; transform: rotate(45deg); animation: swipeArrow 1.8s ease-in-out infinite; }
@keyframes swipe { 0% { transform: translateX(0); opacity: 0; } 15% { opacity: 1; } 70% { transform: translateX(22px); opacity: 1; } 100% { transform: translateX(22px); opacity: 0; } }
@keyframes swipeArrow { 0%, 100% { translate: 0 0; opacity: .4; } 60% { translate: 4px 0; opacity: 1; } }

/* ============ Анализ ЦА ============ */""")

# ---------- hover — только для устройств с мышью ----------
rep(".device:hover .device__play, .uikit__video:hover .device__play, .device__play.paused { opacity: 1; }",
    ".device:hover .device__play, .uikit__video:hover .device__play { opacity: 1; }\n.device__play.paused { opacity: 1; }")


def hover_only(text):
    """Переносит однострочные правила с :hover верхнего уровня в @media (hover: hover)."""
    out, moved, depth = [], [], 0
    for line in text.split("\n"):
        st = line.strip()
        if depth == 0 and ":hover" in st and st.endswith("}") and st.count("{") == 1:
            moved.append(line)
        else:
            out.append(line)
        depth += line.count("{") - line.count("}")
    return "\n".join(out), moved


s, moved = hover_only(s)
touch = """
/* ============ Наведение — только мышь; на сенсорных экранах свои анимации ============ */
@media (hover: hover) {
""" + "\n".join("  " + l.strip() for l in moved) + """
  .link-folder:hover { border-bottom-color: currentColor; }
}
@media (hover: none) {
  .zoomable::after { opacity: 1; transform: scale(.8); right: 6px; top: 6px; }
  .wire figcaption, .device__play { opacity: 1; transform: none; }
  .swatch::after { opacity: 1; transform: translate(-50%, 0); font-size: 10px; bottom: -10px; }
  .design__row:nth-child(1) .swatches { padding-bottom: 12px; }
  .type-spec.in .type-spec__aa b, .design__row.in .type-spec__aa b { animation: weights 3.2s steps(1) infinite; }
  @keyframes weights { 0% { font-weight: 400; } 25% { font-weight: 500; } 50% { font-weight: 600; } 75% { font-weight: 700; } }
  .btn:active, .slider-btn:active, .chip:active, .acc summary:active .acc__btn { transform: scale(.96); }
  .sitemap__cols li:active, .node:active { background: var(--blue-tertiary); }
  .persona, .metric { -webkit-tap-highlight-color: transparent; }
}
"""
i = s.index("/* ================= Адаптив ================= */")
s = s[:i] + touch.lstrip("\n") + "\n" + s[i:]
css.write_text(s, encoding="utf8")
print("sections.css: moved", len(moved), "hover rules")

# ---------- base.css ----------
b = ROOT / "css" / "base.css"
t = b.read_text(encoding="utf8")
t, moved_b = hover_only(t)
t = t.replace("  overflow-x: hidden;\n  -webkit-font-smoothing: antialiased;\n}", "  overflow-x: hidden;\n  -webkit-font-smoothing: antialiased;\n}\nhtml { overflow-x: hidden; }\n@supports (overflow: clip) { html, body { overflow-x: clip; } }")
t = t.replace("/* ============ Анимации появления ============ */", "@media (hover: hover) {\n" + "\n".join("  " + l.strip() for l in moved_b) + "\n}\n\n/* ============ Анимации появления ============ */")
b.write_text(t, encoding="utf8")
print("base.css: moved", len(moved_b), "hover rules")
