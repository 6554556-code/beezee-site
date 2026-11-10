# Генератор страниц раздела «Азбуки» (обзор + 3 азбуки). Пишет обычные HTML-файлы в репозиторий.
import json, os
ROOT = '/home/claude/beezee-site'
SITE = 'https://beezeetoys.ru'
COLOR = '#D8467F'

METRIKA = '''<!-- Yandex.Metrika counter -->
<script type="text/javascript">
    (function(m,e,t,r,i,k,a){
        m[i]=m[i]||function(){(m[i].a=m[i].a||[]).push(arguments)};
        m[i].l=1*new Date();
        for (var j = 0; j < document.scripts.length; j++) {if (document.scripts[j].src === r) { return; }}
        k=e.createElement(t),a=e.getElementsByTagName(t)[0],k.async=1,k.src=r,a.parentNode.insertBefore(k,a)
    })(window, document,'script','https://mc.yandex.ru/metrika/tag.js', 'ym');
    ym(53527606, 'init', {trackHash:true, clickmap:true, referrer: document.referrer, url: location.href, accurateTrackBounce:true, trackLinks:true});
</script>
<noscript><div><img src="https://mc.yandex.ru/watch/53527606" style="position:absolute; left:-9999px;" alt=""></div></noscript>
<!-- /Yandex.Metrika counter -->'''

ORG = {"@type": "Organization", "@id": SITE + "/#org", "name": "BeeZee Toys", "alternateName": ["Bee Zee Toys", "БиЗи Тойс"],
       "url": SITE + "/", "logo": SITE + "/img/logo.webp", "email": "toys@beezeetoys.ru"}

ROOMS_NAV = '''<nav class="rooms" aria-label="Другие этажи дома">
<h2>Загляните на другие этажи</h2>
<ul>
<li><a href="/kalendari/">Календари</a></li>
<li><a href="/pazly/">Пазлы</a></li>
<li><a href="/sortery/">Сортеры</a></li>
<li><a href="/odevashki/">Одевашки</a></li>
<li><a href="/istoriya/">История</a></li>
<li><a href="/pressa/">Пресса</a></li>
<li><a href="/kontakty/">Контакты</a></li>
</ul>
</nav>'''

def crumbs_html(items):
    lis = []
    for i, (name, url) in enumerate(items):
        lis.append(f'<li aria-current="page">{name}</li>' if i == len(items) - 1 else f'<li><a href="{url}">{name}</a></li>')
    return '<nav class="crumbs" aria-label="Хлебные крошки">\n<ol>' + ''.join(lis) + '</ol>\n</nav>'

def crumbs_ld(items):
    return {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": SITE + u} for i, (n, u) in enumerate(items)]}

def page(path, title, desc, og_title, og_desc, og_image, graph, body, gallery_js=False):
    url = SITE + path
    ld = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, indent=2)
    js = '\n<script src="/js/gallery.js" defer></script>' if gallery_js else ''
    html = f'''<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="BeeZee Toys">
<meta property="og:title" content="{og_title}">
<meta property="og:description" content="{og_desc}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}{og_image}">
<meta property="og:locale" content="ru_RU">
<link rel="icon" href="/img/logo.webp">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Rubik:wght@400;500;700;800&family=Caveat:wght@500;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/css/page.css">{js}

<script type="application/ld+json">
{ld}
</script>

{METRIKA}
</head>
<body style="--room:{COLOR}">

<header class="top">
<a href="/" aria-label="BeeZee Toys — на главную"><img src="/img/logo.webp" alt="BeeZee Toys — развивающие игрушки"></a>
<span class="since">Производитель игрушек с 2017 г.</span>
</header>

<main class="wrap">

{body}

{ROOMS_NAV}

</main>

<footer>
<span>© 2017–2026 BeeZee Toys · развивающие игрушки из Санкт-Петербурга</span>
<a href="mailto:toys@beezeetoys.ru">toys@beezeetoys.ru</a>
</footer>

</body>
</html>
'''
    out = os.path.join(ROOT, path.strip('/'), 'index.html')
    os.makedirs(os.path.dirname(out), exist_ok=True)
    open(out, 'w', encoding='utf-8').write(html)
    print('wrote', out)

def gallery(photos):
    figs = ''.join(f'<figure><img src="/img/{f}.webp" alt="{alt}" width="900" height="1200" loading="lazy"><figcaption>{cap}</figcaption></figure>\n'
                   for f, alt, cap in photos)
    return '<div class="gallery">\n' + figs + '</div>'

def specs(rows):
    return '<table class="specs">\n' + ''.join(f'<tr><th scope="row">{k}</th><td>{v}</td></tr>\n' for k, v in rows) + '</table>'

def faq(qs):
    html = '<div class="faq">\n' + ''.join(f'<details><summary>{q}</summary><p>{a}</p></details>\n' for q, a, _ in qs) + '</div>'
    ld = {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": plain}} for q, _, plain in qs]}
    return html, ld

# ---------- данные азбук ----------
A = [
  dict(slug='associacii', name='Магнитная азбука «Ассоциации»', short='«Ассоциации»', tag='54 буквы · туба',
       title='Магнитная азбука «Ассоциации» — 54 буквы с узорами | BeeZee Toys',
       desc='Магнитная азбука BeeZee Toys «Ассоциации»: 54 глянцевые буквы русского алфавита с узорами, сплошной магнит, хранение в тубе. Буквы на холодильник для игры и обучения чтению.',
       card='Каждая буква — со своим узором: горошек, облака, звёзды. Ребёнок запоминает букву по картинке.',
       photos=[('azbuka-tuba','Магнитная азбука BeeZee Toys «Ассоциации» в тубе — 54 буквы русского алфавита','54 буквы в тубе'),
               ('azbuka-dom','Магнитные буквы Д, О, М из азбуки «Ассоциации» BeeZee Toys','Складываем первые слова'),
               ('azbuka-papa','Слово ПАПА из магнитных букв на холодильнике','Послание на холодильнике'),
               ('azbuka-ch','Розовая магнитная буква Ч в цветочек из азбуки «Ассоциации»','Буква-картинка'),
               ('azbuka-girl','Девочка держит тубу с магнитной азбукой BeeZee Toys','Удобно хранить')],
       text='''<h2>Азбука, которую запоминают по картинке</h2>
<p>Каждая буква «Ассоциаций» раскрашена своим узором — горошек, облака, звёзды, цветы. Малыш запоминает не абстрактный значок, а «синюю Б в облаках» или «розовую Ч в цветочек»: так работает ассоциация, и алфавит укладывается в голове быстрее.</p>
<p>Дизайн лаконичный — такую азбуку не стыдно оставить на холодильнике в красивой кухне. Ассоциация, лаконичность, чувство стиля с детства.</p>
<h2>Какие буквы</h2>
<p>Буквы глянцевые, прочные и экологичные. Магнит сплошной — по всей обратной стороне, поэтому буквы крепко держатся на холодильнике, магнитной доске и любой стальной поверхности. После игры всё убирается в тубу — ничего не теряется.</p>
<h2>Во что играть</h2>
<ul>
<li>Ищем букву по узору: «где буква в звёздочку?»</li>
<li>Складываем имена и первые слова: МАМА, ПАПА, ДОМ.</li>
<li>Оставляем послания на холодильнике — папа тает быстрее мороженого.</li>
</ul>''',
       specs=[('Количество','54 буквы русского алфавита'),('Магнит','сплошной, по всей обратной стороне'),('Поверхность','глянцевая'),('Упаковка','туба'),('Производитель','BeeZee Toys, Санкт-Петербург')],
       image='azbuka-tuba'),
  dict(slug='klassika', name='Классическая магнитная азбука, 141 буква', short='Классическая, 141 буква', tag='141 буква · КМ-001',
       title='Магнитная азбука 141 буква — классический алфавит на магнитах | BeeZee Toys',
       desc='Классическая магнитная азбука BeeZee Toys: 141 буква русского алфавита, гласные красные, согласные синие, знаки зелёные. Брошюра с упражнениями, хранение в тубе.',
       card='Большой набор для длинных слов и предложений. Гласные красные, согласные синие, знаки зелёные.',
       photos=[],
       text='''<h2>Карманный букварь на холодильнике</h2>
<p>Классическая азбука — это большой набор из 141 буквы: хватит, чтобы складывать длинные слова, целые предложения и даже двустишия. Букв много, поэтому играть можно вдвоём или втроём — со старшим братом, сестрой или с мамой.</p>
<h2>Цвет подсказывает правила</h2>
<p>Гласные буквы — красные, согласные — синие, мягкий и твёрдый знаки — зелёные. Ребёнок с первых занятий видит, как устроено слово: где гласная, где согласная.</p>
<h2>Брошюра с упражнениями</h2>
<p>В комплекте брошюра с упражнениями — с ней понятно, с чего начать занятия. Игра развивает речь, память и словарный запас. После занятий буквы убираются в яркую тубу.</p>''',
       specs=[('Артикул','КМ-001'),('Количество','141 буква русского алфавита'),('Цвета','гласные — красные, согласные — синие, Ь и Ъ — зелёные'),('В комплекте','брошюра с упражнениями'),('Упаковка','туба'),('Производитель','BeeZee Toys, Санкт-Петербург')],
       image='logo'),
  dict(slug='zverobukvy', name='Магнитная азбука «Зверобуквы и вкусноцифры»', short='«Зверобуквы и вкусноцифры»', tag='55 букв + 20 цифр · от 3 лет',
       title='Магнитная азбука «Зверобуквы и вкусноцифры» — буквы с животными и цифры | BeeZee Toys',
       desc='Магнитная азбука BeeZee Toys «Зверобуквы и вкусноцифры»: 55 букв с животными и названиями, 20 цифр и знаки, стихи на каждую букву, цельный магнит, подарочная туба. Для детей от 3 лет.',
       card='Зверь и его название в каждой букве, «вкусные» цифры для математики и стишки на каждую букву.',
       photos=[('zverobukvy-bukvy','Магнитные буквы с животными «Зверобуквы» BeeZee Toys — весь алфавит','В каждой букве — зверь'),
               ('zverobukvy-slon','Магнитная буква С со слоном из азбуки «Зверобуквы»','С — слон'),
               ('zverobukvy-stihi','Стихи на каждую букву алфавита к азбуке «Зверобуквы» BeeZee Toys','Стишки на каждую букву'),
               ('zverobukvy-tuba','Подарочная туба магнитной азбуки «Зверобуквы и вкусноцифры»','Подарочная туба'),
               ('zverobukvy-kryshka','Магнитная азбука BeeZee Toys, артикул КМ-002','Артикул КМ-002')],
       text='''<h2>Зверь в каждой букве</h2>
<p>Буквы с животными? Прямо в каждой букве, да ещё с названием: А — аллигатор, Б — белка, В — верблюд, С — слон, Ш — шмель. А цифры — «вкусные». Буквы большие, с цельным магнитом и приятные на ощупь — от этой азбуки не могут оторваться даже взрослые.</p>
<h2>Буквы, цифры и знаки</h2>
<p>В наборе 55 букв и 20 цифр плюс знаки для первых примеров. Пишите слова и предложения, разгадывайте кроссворды, решайте простые примеры прямо на холодильнике. Приятные на ощупь буквы полезны для тактильного восприятия.</p>
<h2>Стихи на каждую букву</h2>
<p>К набору прилагаются стишки на каждую букву алфавита, которые мы сочинили сами: «Белки — рыжие малышки, собирают с ёлки шишки», «По песку верблюд идёт, воду долго он не пьёт». С ними алфавит запоминается быстрее, а заодно развиваются речь и память.</p>
<h2>Подарок и пособие для занятий</h2>
<p>Набор упакован в яркую подарочную тубу — хороший подарок мальчику или девочке на день рождения, Новый год и любой детский праздник. В тубе азбуку удобно хранить и брать с собой. Педагоги берут её для занятий в детском саду и развивающих центрах.</p>''',
       specs=[('Артикул','КМ-002'),('Количество','55 букв, 20 цифр и математические знаки'),('Особенности','животное и его название в каждой букве'),('Магнит','цельный'),('В комплекте','стихи на каждую букву алфавита'),('Упаковка','подарочная туба'),('Возраст','от 3 лет'),('Производитель','BeeZee Toys, Санкт-Петербург')],
       image='zverobukvy-bukvy'),
]

# ---------- обзорная страница /azbuki/ ----------
picks = ''
for a in A:
    img = (f'<img src="/img/{a["photos"][0][0]}.webp" alt="{a["photos"][0][1]}" width="900" height="1200" loading="lazy">'
           if a['photos'] else '<span class="ph-empty">фото скоро</span>')
    picks += f'''<a class="pick" href="/azbuki/{a["slug"]}/">
{img}
<span class="pick-body"><span class="tag">{a["tag"]}</span><strong>{a["name"]}</strong><p>{a["card"]}</p><span class="more">Подробнее →</span></span>
</a>
'''

faq_main = [
 ('Буквы держатся на холодильнике?', 'Да. Магнит у наших букв сплошной — по всей обратной стороне, поэтому буквы держатся на холодильнике, магнитной доске и любой стальной поверхности.', 'Да. Магнит у наших букв сплошной — по всей обратной стороне, поэтому буквы держатся на холодильнике, магнитной доске и любой стальной поверхности.'),
 ('Сколько букв в наборах?', '«Ассоциации» — 54 буквы, классическая азбука — 141 буква, «Зверобуквы и вкусноцифры» — 55 букв, 20 цифр и знаки для математики.', '«Ассоциации» — 54 буквы, классическая азбука — 141 буква, «Зверобуквы и вкусноцифры» — 55 букв, 20 цифр и знаки для математики.'),
 ('Какую азбуку выбрать?', 'Для знакомства с буквами — <a href="/azbuki/zverobukvy/">«Зверобуквы»</a> или <a href="/azbuki/associacii/">«Ассоциации»</a>: буквы запоминаются по картинке. Для чтения и составления длинных слов — <a href="/azbuki/klassika/">классическая на 141 букву</a>.', 'Для знакомства с буквами — «Зверобуквы» или «Ассоциации»: буквы запоминаются по картинке. Для чтения и составления длинных слов — классическая на 141 букву.'),
 ('Есть ли у игрушек сертификаты?', 'Да, все игрушки BeeZee Toys имеют сертификаты соответствия.', 'Да, все игрушки BeeZee Toys имеют сертификаты соответствия.'),
 ('Где купить магнитную азбуку BeeZee Toys?', 'Ссылки на наши магазины на маркетплейсах — <a href="/#buy">внизу главной страницы</a>. По оптовым закупкам пишите на <a href="mailto:toys@beezeetoys.ru">toys@beezeetoys.ru</a>.', 'Ссылки на наши магазины на маркетплейсах — внизу главной страницы beezeetoys.ru. По оптовым закупкам пишите на toys@beezeetoys.ru.'),
]
faq_html, faq_ld = faq(faq_main)
crumbs = [('Главная','/'),('Азбуки','/azbuki/')]
body = f'''{crumbs_html(crumbs)}

<section class="hero">
<div class="deco" aria-hidden="true">
<img src="/img/azbuki-a.webp" alt="" style="right:58%;top:12%;height:30%">
<img src="/img/azbuki-b.webp" alt="" style="right:22%;top:6%;height:26%;animation-delay:-1.2s">
<img src="/img/azbuki-v.webp" alt="" style="right:40%;top:52%;height:28%;animation-delay:-2.4s">
<img src="/img/azbuki-g.webp" alt="" style="right:4%;top:46%;height:30%;animation-delay:-3.6s">
</div>
<a class="home" href="/">← Вернуться в дом</a>
<span class="note hand">хит BeeZee</span>
<h1>Магнитная азбука для детей</h1>
<p class="lead">Три азбуки на магнитах: узорные «Ассоциации», классическая на 141 букву и «Зверобуквы» с животными в каждой букве. Играть на холодильнике и учить буквы можно каждый день.</p>
</section>

<article class="text wide">
<h2>Наши магнитные азбуки</h2>
<div class="picks">
{picks}</div>
</article>

<article class="text">

<h2>Зачем ребёнку магнитная азбука</h2>
<p>Азбука на холодильнике всегда на виду: ребёнок возвращается к буквам десятки раз в день — пока ждёт завтрак, помогает маме на кухне, играет со старшими. Буквы можно трогать, переставлять, складывать в слоги и слова, поэтому обучение чтению превращается в игру, а не в урок.</p>
<p>Магнитные буквы развивают сразу несколько навыков: зрительную память (буква узнаётся по цвету и рисунку), мелкую моторику (буквы нужно взять, повернуть и прикрепить), речь и словарный запас (из букв складываются первые слова).</p>

<h2>Как выбрать магнитную азбуку</h2>
<ul>
<li><strong>Магнит.</strong> Сплошной магнит по всей букве держится надёжнее, чем маленькая магнитная таблетка, которая может отклеиться.</li>
<li><strong>Размер.</strong> Крупные буквы удобно брать маленькими пальчиками, и их видно издалека.</li>
<li><strong>Количество.</strong> Чтобы складывать слова, нужны повторяющиеся буквы: МАМА — это две М и две А.</li>
<li><strong>Подсказки.</strong> Картинка или цвет на букве помогают запомнить её быстрее.</li>
<li><strong>Хранение.</strong> Туба или коробка — чтобы буквы не терялись по квартире.</li>
</ul>

<h2>Во что играть с магнитной азбукой</h2>
<ol>
<li><strong>Буква дня.</strong> Каждое утро вешаем на холодильник одну новую букву и ищем вокруг предметы на неё.</li>
<li><strong>Собери имя.</strong> Складываем имена всех членов семьи — и даже кота.</li>
<li><strong>Гласные и согласные.</strong> Разбираем буквы на две команды по цвету.</li>
<li><strong>Послание на холодильнике.</strong> Оставляем друг другу короткие слова: «МАМА», «ПАПА», «ЛЮБЛЮ». Проверено: папа тает быстрее мороженого.</li>
<li><strong>Слово-перевёртыш.</strong> Меняем одну букву — получаем новое слово: КОТ → КИТ → КОМ.</li>
<li><strong>Стишок на букву.</strong> Читаем стихотворение и ищем героя на холодильнике.</li>
<li><strong>Вкусная математика.</strong> Из цифр и знаков складываем первые примеры: 2 + 3 = 5.</li>
</ol>

<h2>Кто делает азбуки BeeZee Toys</h2>
<p>Мы придумываем и рисуем азбуки сами, в Санкт-Петербурге. Первые наши азбуки в 2017 году были деревянными — о том, как мы пришли к глянцевым буквам на магнитах, рассказываем в <a href="/istoriya/">истории бренда</a>. Все игрушки BeeZee Toys имеют сертификаты соответствия.</p>

<h2>Частые вопросы</h2>
{faq_html}

</article>'''
graph = [
  {"@type": "CollectionPage", "name": "Магнитная азбука для детей", "url": SITE + "/azbuki/", "inLanguage": "ru", "publisher": {"@id": SITE + "/#org"},
   "mainEntity": {"@type": "ItemList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "url": SITE + f"/azbuki/{a['slug']}/", "name": a['name']} for i, a in enumerate(A)]}},
  ORG, crumbs_ld(crumbs), faq_ld]
page('/azbuki/', 'Магнитная азбука для детей — буквы на магнитах | BeeZee Toys',
     'Магнитные азбуки BeeZee Toys: «Ассоциации» на 54 буквы, классическая на 141 букву и «Зверобуквы и вкусноцифры» с животными и цифрами. Как выбрать азбуку и во что с ней играть.',
     'Магнитная азбука для детей — BeeZee Toys', 'Три магнитные азбуки: «Ассоциации», классическая на 141 букву и «Зверобуквы и вкусноцифры».',
     '/img/azbuka-tuba.webp', graph, body)

# ---------- страницы азбук ----------
for a in A:
    crumbs = [('Главная','/'),('Азбуки','/azbuki/'),(a['short'], f"/azbuki/{a['slug']}/")]
    gal = gallery(a['photos']) if a['photos'] else '<div class="ph-wait"><span>Фото скоро появятся</span></div>'
    others = ''.join(f'<li><a href="/azbuki/{o["slug"]}/">{o["short"]}</a></li>' for o in A if o is not a)
    body = f'''{crumbs_html(crumbs)}

<section class="hero small">
<a class="home" href="/azbuki/">← Все азбуки</a>
<span class="note hand">{a["tag"]}</span>
<h1>{a["name"]}</h1>
</section>

{gal}

<article class="text">
{a["text"]}

<h2>Характеристики</h2>
{specs(a["specs"])}

<p style="margin-top:22px">Где купить: ссылки на наши магазины на маркетплейсах — <a href="/#buy">внизу главной страницы</a>. Опт — <a href="mailto:toys@beezeetoys.ru">toys@beezeetoys.ru</a>.</p>
</article>

<nav class="rooms" aria-label="Другие азбуки">
<h2>Другие азбуки</h2>
<ul><li><a href="/azbuki/">Все азбуки</a></li>{others}</ul>
</nav>'''
    images = [SITE + f'/img/{p[0]}.webp' for p in a['photos']] or [SITE + '/img/logo.webp']
    prod = {"@type": "Product", "name": a['name'], "description": a['desc'], "image": images,
            "brand": {"@type": "Brand", "name": "BeeZee Toys"}, "manufacturer": {"@id": SITE + "/#org"}, "category": "Магнитные азбуки"}
    sku = dict(a['specs']).get('Артикул')
    if sku: prod['sku'] = sku
    page(f"/azbuki/{a['slug']}/", a['title'], a['desc'], a['name'] + ' — BeeZee Toys', a['card'],
         f"/img/{a['image']}.webp", [prod, ORG, crumbs_ld(crumbs)], body, gallery_js=bool(a['photos']))
