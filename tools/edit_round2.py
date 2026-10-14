"""Правки по замечаниям (раунд 2): разметка index.html."""
from pathlib import Path
from urllib.parse import quote

p = Path(__file__).resolve().parent.parent / "index.html"
s = p.read_text(encoding="utf8")
B = "https://disk.yandex.ru/d/cltu1ibdZa6NSg"
f = lambda n: B + "/" + quote(n)
SUS = f("Оценка удобства SUS.xlsx")
SURV = f("Результаты опроса.xlsx")
CA = f("ЦА ИжГТУ — анализ.pdf")
UT = f("Юзабилити-тест ИжГТУ — сводная таблица.docx")
ARW = '<img class="ico" src="assets/icons/arrow-up-right-white.svg" alt="">'
ARB = '<img class="ico" src="assets/icons/arrow-up-right-blue.svg" alt="">'
FOLDER = (f'<a class="link-folder" href="{B}" target="_blank" rel="noopener"><svg viewBox="0 0 24 24" aria-hidden="true">'
          '<path d="M3 7a2 2 0 0 1 2-2h4l2 2h8a2 2 0 0 1 2 2v8a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/></svg>Вся папка с аналитикой</a>')


def rep(a, b):
    global s
    assert a in s, a[:70]
    s = s.replace(a, b)


def cut(start, end):
    i = s.index(start)
    return s[i:s.index(end, i)]


def item(t, d):
    return f'<button class="orbit__item" type="button"><i></i><span class="orbit__text"><b>{t}</b><small>{d}</small></span></button>'


ARC = ('<svg class="orbit__arc" viewBox="0 0 45 219.5" preserveAspectRatio="none" aria-hidden="true">'
       '<path d="M7.13 219.49C32.62 188.25 46.02 148.9 44.9 108.61 43.77 68.31 28.2 29.77 1.02 0"/></svg>')

rep(cut('      <div class="ca__grid">', '  <!-- ===================== ПОРТРЕТЫ'), f'''      <div class="ca__grid">
        <div class="orbit reveal from-left">
          <p class="orbit__label h-xl grad-text">ЦА</p>
          <div class="orbit__items">
            {ARC}
            {item('Одиннадцатиклассники', 'Им предстоит поступление, самые частые пользователи сайта вуза')}
            {item('Родители абитуриентов', 'Помогают своим детям определиться с профессией')}
            {item('Первокурсники', 'Некоторые студенты на 1 курсе решают перепоступить')}
          </div>
        </div>
        <div class="orbit reveal from-right" style="--d:.15s">
          <p class="orbit__label h-lg grad-text">Что важно<br>на сайте</p>
          <div class="orbit__items">
            {ARC}
            {item('Скорость отклика', 'Ответ на главный вопрос за 2–3 действия, понятный интерфейс')}
            {item('Лёгкость поиска информации', 'Подбор по предметам ЕГЭ, понятные фильтры и поиск по названию')}
            {item('Удобство с телефона', 'Фильтры сверху, карточки в одну колонку, без таблиц')}
          </div>
        </div>
      </div>
      <div class="links-row reveal">
        <a class="btn btn--outline" href="{CA}" target="_blank" rel="noopener">Полный анализ ЦА {ARB}</a>
        {FOLDER}
      </div>
    </div>
  </section>

''')

rep(f'''      <a class="btn reveal" href="{B}" target="_blank" rel="noopener">Перейти к аналитике {ARW}</a>

      <div class="insights offset-block">''', f'''      <div class="links-row reveal">
        <a class="btn" href="{UT}" target="_blank" rel="noopener">Перейти к аналитике {ARW}</a>
        <a class="btn btn--outline" href="{SUS}" target="_blank" rel="noopener">Анкета SUS {ARB}</a>
        {FOLDER}
      </div>

      <div class="insights offset-block">''')

ins = cut('        <ol class="insights__list">', '      </div>\n    </div>\n  </section>\n\n  <!-- ===================== ОПРОС')
rep(ins, '''        <div class="insights__body">
          <ol class="insights__list">
            <li class="reveal"><b>В списке нет проходного балла, бюджетных мест и цены.</b> Каждую программу приходится открывать отдельно</li>
            <li class="reveal" style="--d:.1s"><b>Неудобный ползунок проходного балла.</b> Его не замечают, настраивают наоборот («от 165» вместо «до 165»), хочется ввести число.</li>
            <li class="reveal" style="--d:.2s"><b>На телефоне фильтры спрятаны под списком.</b> Пользователю приходится перелистывать все программы.</li>
          </ol>
          <div class="insights__more" id="insights-more">
            <div>
              <ol class="insights__list" start="4">
                <li><b>Первый клик уводит не туда.</b> Разделы «Выбрать факультет», «Рейтинг абитуриентов», «Подать документы» путают.</li>
                <li><b>Кнопка «Применить» внизу фильтров или их две.</b> Результат обновляется не сразу, приходится искать и нажимать кнопку.</li>
                <li><b>Устаревший разношёрстный визуал.</b> Узкий мелкий шрифт, прописное письмо (капс), старые фото раздражают пользователей.</li>
              </ol>
            </div>
          </div>
          <button class="link-more insights__toggle reveal" type="button" aria-expanded="false" aria-controls="insights-more" style="--d:.3s">Читать полностью</button>
        </div>
''')

rep(f'''      <a class="btn reveal" href="{B}" target="_blank" rel="noopener">Перейти к аналитике {ARW}</a>

      <div class="survey__insights">''', f'''      <div class="links-row reveal">
        <a class="btn" href="{SURV}" target="_blank" rel="noopener">Перейти к аналитике {ARW}</a>
        {FOLDER}
      </div>

      <div class="survey__insights">''')

rep(cut('      <div class="perception">', '  <!-- ===================== UI-KIT'), f'''      <div class="links-row reveal">
        <a class="btn btn--outline" href="{SUS}" target="_blank" rel="noopener">Результаты анкеты SUS {ARB}</a>
        {FOLDER}
      </div>

      <div class="perception">
        <h3 class="t-20 accent perception__h1 reveal">Что изменилось в восприятии</h3>
        <h3 class="t-20 perception__h2 reveal">Что можно доработать</h3>
        <div class="quotes quotes--before reveal from-left">
          <p class="quotes__head"><b>Было</b><i></i>Первое впечатление от istu.ru</p>
          <blockquote>«Много информации, сверху маленькие шрифты»<cite>Респондент 2</cite></blockquote>
          <blockquote>«Ляпистый»: современные картинки вперемешку со старыми фото, нет единого стиля<cite>Респондент 3</cite></blockquote>
          <blockquote>«Огромная реклама, которая неправильно отображается с телефона»<cite>Респондент 4</cite></blockquote>
        </div>
        <div class="quotes quotes--after reveal" style="--d:.1s">
          <p class="quotes__head"><b>Стало</b><i></i>Первое впечатление от редизайна</p>
          <blockquote>«Запомнилась чистота интерфейса»<cite>Респондент 4</cite></blockquote>
          <blockquote>«Интерфейс стал современнее и удобнее»<cite>Респондент 2</cite></blockquote>
          <blockquote>«Теперь в интерфейсе нет раздражающих факторов, всё чётко и понятно»<cite>Респондент 4</cite></blockquote>
        </div>
        <div class="todo reveal from-right" style="--d:.2s">
          <div class="todo__item">
            <b>Добавить чекбокс с русским языком в предметах ЕГЭ, а не учитывать его по умолчанию</b>
            <p>3 из 4 респондентов потратили время, чтобы заметить подсказку о том, что русский язык всегда включён, — лучше вернуть его в список.</p>
          </div>
          <div class="todo__item">
            <b>Добавить подсказку «Подбери по баллам ЕГЭ», которая перенаправляет в фильтры</b>
            <p>Один респондент не догадался, что баллы ЕГЭ находятся в фильтрах. Перед доработкой проверить гипотезу необходимости этой правки.</p>
          </div>
          <div class="todo__item">
            <b>Добавить СПО в меню</b>
            <p>Два респондента искали программы для СПО в выпадающем бургер-меню.</p>
          </div>
        </div>
      </div>
    </div>
  </section>

''')

rep(cut('      <div class="wires__grid">', '  <!-- ===================== НАВИГАЦИЯ'), '''      <div class="wires__grid">
        <div class="wires__texts">
          <p class="reveal">Следующим шагом после определения дизайн‑концепции стала разработка вайрфреймов (схематичное представление структуры будущего цифрового продукта)</p>
          <p class="reveal" style="--d:.1s">В данном проекте создание чернового варианта стало важнейшим процессом, так как цель — упростить пользовательский путь, а он продумывается именно на этом этапе</p>
        </div>
        <figure class="wire wire--tall reveal from-left">
          <img src="assets/gif/wf1.gif" alt="Вайрфрейм превращается в готовый дизайн: главная страница" loading="lazy" width="480" height="965">
          <figcaption><span>Черновик</span><i></i><span>Дизайн</span></figcaption>
        </figure>
        <figure class="wire wire--a reveal" style="--d:.05s"><img src="assets/gif/wf3.gif" alt="Вайрфрейм превращается в готовый дизайн: список программ" loading="lazy" width="560" height="507"><figcaption><span>Черновик</span><i></i><span>Дизайн</span></figcaption></figure>
        <figure class="wire wire--b reveal" style="--d:.15s"><img src="assets/gif/wf2.gif" alt="Вайрфрейм превращается в готовый дизайн: каталог программ" loading="lazy" width="560" height="507"><figcaption><span>Черновик</span><i></i><span>Дизайн</span></figcaption></figure>
        <figure class="wire wire--c reveal" style="--d:.25s"><img src="assets/gif/wf4.gif" alt="Вайрфрейм превращается в готовый дизайн: страница программы" loading="lazy" width="560" height="507"><figcaption><span>Черновик</span><i></i><span>Дизайн</span></figcaption></figure>
      </div>
    </div>
  </section>

''')

rep('        <div class="flow__canvas">', '''        <p class="swipe-hint" aria-hidden="true"><span class="swipe-hint__hand"></span>Листайте экраны</p>
        <div class="flow__canvas">''')
p.write_text(s, encoding="utf8")
print("ok")
