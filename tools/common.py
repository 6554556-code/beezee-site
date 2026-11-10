# Общие детали всех страниц разделов: шапка, подвал, Метрика, хлебные крошки, Schema.org, галерея, таблица, вопросы.
# Генераторы разделов (build_azbuki.py, build_kalendari.py, …) берут всё отсюда — правка здесь меняет все разделы сразу.
import json, os, hashlib

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # корень репозитория
SITE = 'https://beezeetoys.ru'

def ver(f):  # номер версии файла — браузер скачает заново, как только файл изменится
    return hashlib.md5(open(os.path.join(ROOT, f), 'rb').read()).hexdigest()[:8]

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

# Этажи дома сверху вниз: (папка, название). Меню «Загляните на другие этажи» строится отсюда.
SECTIONS = [('azbuki', 'Азбуки'), ('kalendari', 'Календари'), ('pazly', 'Пазлы'), ('sortery', 'Сортеры'),
            ('odevashki', 'Одевашки'), ('istoriya', 'История'), ('pressa', 'Пресса'), ('kontakty', 'Контакты')]

def rooms_nav(current):
    lis = ''.join(f'<li><a href="/{s}/">{n}</a></li>\n' for s, n in SECTIONS if s != current)
    return f'''<nav class="rooms" aria-label="Другие этажи дома">
<h2>Загляните на другие этажи</h2>
<ul>
{lis}</ul>
</nav>'''

def crumbs_html(items):
    lis = []
    for i, (name, url) in enumerate(items):
        lis.append(f'<li aria-current="page">{name}</li>' if i == len(items) - 1 else f'<li><a href="{url}">{name}</a></li>')
    return '<nav class="crumbs" aria-label="Хлебные крошки">\n<ol>' + ''.join(lis) + '</ol>\n</nav>'

def crumbs_ld(items):
    return {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": SITE + u} for i, (n, u) in enumerate(items)]}

def page(path, title, desc, og_title, og_desc, og_image, graph, body, section, color, gallery_js=False):
    url = SITE + path
    ld = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, indent=2)
    js = f'\n<script src="/js/gallery.js?v={ver("js/gallery.js")}" defer></script>' if gallery_js else ''
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
<link rel="stylesheet" href="/css/page.css?v={ver('css/page.css')}">{js}

<script type="application/ld+json">
{ld}
</script>

{METRIKA}
</head>
<body style="--room:{color}">

<header class="top">
<a href="/" aria-label="BeeZee Toys — на главную"><img src="/img/logo.webp" alt="BeeZee Toys — развивающие игрушки"></a>
<span class="since">Производитель игрушек с 2017 г.</span>
</header>

<main class="wrap">

{body}

{rooms_nav(section)}

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
