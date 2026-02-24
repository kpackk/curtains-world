#!/usr/bin/env python3
"""
Landing page generator for Curtains World product categories.

Reads configuration for each product landing page and generates clean,
semantic HTML files using a shared template. Each page includes:
- Unique meta tags (title, description, keywords, canonical)
- Header/navigation matching the main site
- H1, product description, booking CTA
- FAQ section with FAQPage schema
- BreadcrumbList schema
- Footer with contacts
- Analytics: GTM, Yandex.Metrika, Facebook Pixel
- WhatsApp floating button
"""

import os
import json
from html import escape

# ---------------------------------------------------------------------------
# Base URL & shared constants
# ---------------------------------------------------------------------------
BASE_URL = "https://curtainsfactory.ae"
PHONE = "+971 58 940 8100"
PHONE_LINK = "tel:+971589408100"
WA_LINK = (
    "https://wa.me/971589408100?text="
    "%D0%97%D0%B4%D1%80%D0%B0%D0%B2%D1%81%D1%82%D0%B2%D1%83%D0%B9%D1%82%D0%B5!"
    "%20%D0%A5%D0%BE%D1%87%D1%83%20%D1%83%D0%B7%D0%BD%D0%B0%D1%82%D1%8C"
    "%20%D0%BF%D1%80%D0%BE%20%D1%88%D1%82%D0%BE%D1%80%D1%8B"
)
EMAIL = "hello@curtainsfactory.ae"

# ---------------------------------------------------------------------------
# Page definitions
# ---------------------------------------------------------------------------
PAGES = [
    {
        "filename": "blackout-shtory-dubai.html",
        "slug": "blackout-shtory-dubai",
        "title": "Блэкаут шторы на заказ в Дубае | Curtains World",
        "h1": "Блэкаут шторы на заказ в Дубае",
        "description": (
            "Блэкаут шторы в Дубае — полная блокировка света. "
            "Натуральные ткани, пошив за 4-5 дней. "
            "Бесплатный замер и установка. Звоните: +971 58 940 8100"
        ),
        "keywords": (
            "блэкаут шторы дубай, затемняющие шторы дубай, "
            "blackout curtains dubai, шторы блэкаут ОАЭ"
        ),
        "breadcrumb_name": "Блэкаут шторы",
        "content_paragraphs": [
            (
                "Блэкаут шторы — идеальное решение для спален, детских комнат "
                "и домашних кинотеатров в Дубае. Благодаря специальной "
                "многослойной структуре ткани они блокируют до 99% солнечного "
                "света, обеспечивая полную темноту даже в самый яркий день."
            ),
            (
                "Мы используем ткани премиум-класса с термоизолирующим слоем, "
                "который не только защищает от света, но и снижает нагрев "
                "помещения. Это особенно важно в условиях жаркого климата "
                "Дубая — блэкаут шторы помогают экономить на кондиционировании."
            ),
            (
                "В нашем каталоге широкий выбор цветов и фактур: от матовых "
                "однотонных до текстурных с рисунком. Все шторы шьются "
                "индивидуально по вашим размерам. Замер, доставка и установка "
                "входят в стоимость. Срок изготовления — 4-5 рабочих дней."
            ),
        ],
        "faq": [
            {
                "q": "Сколько стоят блэкаут шторы на заказ?",
                "a": (
                    "Стоимость рассчитывается за квадратные метры и зависит от "
                    "выбранной ткани. В цену включены замер, карниз, доставка и "
                    "установка. Используйте калькулятор на нашем сайте для "
                    "мгновенного расчёта."
                ),
            },
            {
                "q": "На сколько процентов блэкаут шторы блокируют свет?",
                "a": (
                    "Наши блэкаут шторы блокируют от 95% до 99% солнечного света "
                    "в зависимости от выбранной ткани. Для максимального "
                    "затемнения рекомендуем трёхслойные ткани."
                ),
            },
            {
                "q": "Какие ткани доступны для блэкаут штор?",
                "a": (
                    "Мы предлагаем блэкаут ткани различных типов: классические "
                    "трёхслойные, с термоизоляцией, с текстурой льна, "
                    "а также варианты для детских комнат с яркими расцветками."
                ),
            },
            {
                "q": "Сколько времени занимает установка?",
                "a": (
                    "Пошив занимает 4-5 рабочих дней после замера. "
                    "Установка обычно выполняется в день доставки и занимает "
                    "1-2 часа в зависимости от количества окон."
                ),
            },
        ],
    },
    {
        "filename": "tyul-na-zakaz-dubai.html",
        "slug": "tyul-na-zakaz-dubai",
        "title": "Тюль на заказ в Дубае | Curtains World",
        "h1": "Тюль на заказ в Дубае",
        "description": (
            "Тюль на заказ в Дубае из натуральных тканей — лён и хлопок. "
            "Бесплатный замер, установка. Пошив за 4-5 дней. "
            "Звоните: +971 58 940 8100"
        ),
        "keywords": (
            "тюль дубай, тюль на заказ дубай, "
            "sheer curtains dubai, тюль ОАЭ"
        ),
        "breadcrumb_name": "Тюль на заказ",
        "content_paragraphs": [
            (
                "Тюль — это лёгкая полупрозрачная ткань, которая мягко "
                "рассеивает солнечный свет и создаёт уютную атмосферу "
                "в любом помещении. Наш тюль на заказ идеально подходит "
                "для гостиных, столовых и кухонь в Дубае."
            ),
            (
                "Мы используем только натуральные ткани премиум-класса — "
                "лён и хлопок. Эти материалы дышат, приятны на ощупь и "
                "долговечны. Тюль из натуральных волокон не электризуется "
                "и не притягивает пыль, что особенно актуально в климате ОАЭ."
            ),
            (
                "Каждый тюль шьётся индивидуально по размерам вашего окна. "
                "Мы предлагаем различные виды драпировки: классическую складку, "
                "люверсы, ленту. Замер и установка бесплатны, срок пошива — "
                "4-5 рабочих дней."
            ),
        ],
        "faq": [
            {
                "q": "Из каких тканей шьётся тюль?",
                "a": (
                    "Мы предлагаем тюль из натурального льна и хлопка "
                    "различной плотности — от лёгкого воздушного до более "
                    "плотного с текстурой. Все ткани экологичные и гипоаллергенные."
                ),
            },
            {
                "q": "Насколько прозрачный тюль?",
                "a": (
                    "Степень прозрачности зависит от выбранной ткани. "
                    "У нас есть варианты от почти полностью прозрачных до "
                    "полупрозрачных, которые хорошо скрывают от взглядов снаружи, "
                    "но пропускают свет."
                ),
            },
            {
                "q": "Как ухаживать за тюлем?",
                "a": (
                    "Тюль из натуральных тканей стирается в деликатном режиме "
                    "при 30°C. Рекомендуем стирку раз в 3-4 месяца. "
                    "Гладить на минимальной температуре или использовать отпариватель."
                ),
            },
            {
                "q": "Сколько стоит тюль на заказ?",
                "a": (
                    "Стоимость рассчитывается за квадратные метры готового изделия. "
                    "Замер, карниз, доставка и установка включены. "
                    "Используйте калькулятор на сайте для расчёта."
                ),
            },
        ],
    },
    {
        "filename": "motorizirovannye-shtory-dubai.html",
        "slug": "motorizirovannye-shtory-dubai",
        "title": "Моторизированные шторы в Дубае | Curtains World",
        "h1": "Моторизированные шторы в Дубае",
        "description": (
            "Электрические шторы с управлением с пульта и смартфона. "
            "Установка в Дубае. Бесплатный замер. "
            "Звоните: +971 58 940 8100"
        ),
        "keywords": (
            "моторизированные шторы дубай, электрические шторы дубай, "
            "motorized curtains dubai"
        ),
        "breadcrumb_name": "Моторизированные шторы",
        "content_paragraphs": [
            (
                "Моторизированные шторы — это современное решение для "
                "управления освещением в вашем доме. Откройте или закройте "
                "шторы одним нажатием кнопки на пульте, через приложение на "
                "смартфоне или голосовой командой."
            ),
            (
                "Наши электрические карнизы работают практически бесшумно "
                "и совместимы с системами умного дома: Apple HomeKit, "
                "Google Home, Amazon Alexa. Вы можете настроить расписание "
                "автоматического открытия и закрытия штор."
            ),
            (
                "Мы устанавливаем моторизированные системы для любых типов "
                "штор — тюль, блэкаут, рулонные. Питание от сети 220В или "
                "от аккумулятора с зарядкой через USB-C. Бесплатный замер "
                "и профессиональная установка включены."
            ),
        ],
        "faq": [
            {
                "q": "Как управлять моторизированными шторами?",
                "a": (
                    "Управление доступно с пульта ДУ, через мобильное приложение "
                    "на смартфоне, голосовыми командами (Siri, Alexa, Google), "
                    "а также по расписанию через приложение."
                ),
            },
            {
                "q": "Совместимы ли шторы с системами умного дома?",
                "a": (
                    "Да, наши моторизированные карнизы поддерживают Apple HomeKit, "
                    "Google Home, Amazon Alexa и работают через Wi-Fi или Bluetooth. "
                    "Интеграция настраивается при установке."
                ),
            },
            {
                "q": "Какое питание нужно для электрических штор?",
                "a": (
                    "Доступны два варианта: проводное подключение к сети 220В "
                    "(скрытая проводка) или аккумуляторные моторы с зарядкой "
                    "через USB-C, которые работают 6-12 месяцев без подзарядки."
                ),
            },
            {
                "q": "Как обслуживать моторизированные шторы?",
                "a": (
                    "Электрические карнизы практически не требуют обслуживания. "
                    "Рекомендуем протирать направляющие раз в полгода. "
                    "На мотор предоставляется гарантия 3 года."
                ),
            },
        ],
    },
    {
        "filename": "zhalyuzi-dubai.html",
        "slug": "zhalyuzi-dubai",
        "title": "Жалюзи на заказ в Дубае | Curtains World",
        "h1": "Жалюзи на заказ в Дубае",
        "description": (
            "Жалюзи на заказ в Дубае — вертикальные, горизонтальные, "
            "рулонные. Замер и установка бесплатно. "
            "Звоните: +971 58 940 8100"
        ),
        "keywords": (
            "жалюзи дубай, жалюзи на заказ дубай, "
            "blinds dubai, рулонные шторы дубай"
        ),
        "breadcrumb_name": "Жалюзи",
        "content_paragraphs": [
            (
                "Жалюзи — практичное и стильное решение для офисов, "
                "кухонь, ванных комнат и любых помещений в Дубае. "
                "Они позволяют точно регулировать количество света, "
                "легко чистятся и занимают минимум места."
            ),
            (
                "Мы предлагаем все основные типы жалюзи: вертикальные "
                "из ткани, горизонтальные алюминиевые и деревянные, "
                "а также рулонные шторы различной плотности. "
                "Для влажных помещений есть влагостойкие модели."
            ),
            (
                "Каждый заказ изготавливается индивидуально по вашим "
                "размерам. Широкий выбор цветов и материалов позволяет "
                "подобрать жалюзи под любой интерьер. Замер бесплатный, "
                "установка включена в стоимость."
            ),
        ],
        "faq": [
            {
                "q": "Какие типы жалюзи вы предлагаете?",
                "a": (
                    "Вертикальные тканевые, горизонтальные алюминиевые "
                    "и деревянные, рулонные шторы (в том числе день-ночь), "
                    "а также римские шторы. Все изготавливаются на заказ."
                ),
            },
            {
                "q": "Из каких материалов делают жалюзи?",
                "a": (
                    "Алюминий, натуральное дерево, бамбук, ткань, "
                    "ПВХ (для влажных помещений). Выбор материала зависит "
                    "от назначения помещения и ваших предпочтений."
                ),
            },
            {
                "q": "Подходят ли жалюзи для ванной комнаты?",
                "a": (
                    "Да, для ванных комнат мы предлагаем влагостойкие модели "
                    "из алюминия или ПВХ, которые не боятся воды и пара. "
                    "Они легко моются и долго сохраняют внешний вид."
                ),
            },
            {
                "q": "Сколько стоят жалюзи на заказ?",
                "a": (
                    "Цена зависит от типа жалюзи, материала и размеров окна. "
                    "Замер, изготовление и установка включены. "
                    "Свяжитесь с нами для бесплатного расчёта."
                ),
            },
        ],
    },
    {
        "filename": "karnizy-dubai.html",
        "slug": "karnizy-dubai",
        "title": "Карнизы в Дубае | Curtains World",
        "h1": "Карнизы в Дубае",
        "description": (
            "Карнизы для штор в Дубае — потолочные, настенные, электрические. "
            "Установка бесплатно. Звоните: +971 58 940 8100"
        ),
        "keywords": (
            "карнизы дубай, карнизы для штор дубай, "
            "curtain rods dubai, карнизы ОАЭ"
        ),
        "breadcrumb_name": "Карнизы",
        "content_paragraphs": [
            (
                "Карниз — важный элемент оформления окна, от которого зависит "
                "внешний вид и функциональность штор. Мы предлагаем широкий "
                "выбор карнизов для любых помещений в Дубае: потолочные, "
                "настенные и электрические."
            ),
            (
                "Потолочные карнизы визуально увеличивают высоту помещения "
                "и создают эффект штор \"от потолка до пола\". Настенные карнизы "
                "— классический вариант, который подходит для большинства "
                "интерьеров. Электрические карнизы обеспечивают управление "
                "с пульта и смартфона."
            ),
            (
                "Все карнизы устанавливаются нашими специалистами. "
                "При заказе штор карниз и установка входят в стоимость. "
                "Мы работаем с профильными алюминиевыми системами, "
                "которые надёжны, бесшумны и долговечны."
            ),
        ],
        "faq": [
            {
                "q": "Какие типы карнизов вы предлагаете?",
                "a": (
                    "Потолочные профильные (скрытые в нише или открытые), "
                    "настенные (круглые и профильные), электрические "
                    "с управлением с пульта и смартфона. Одно- и двухрядные."
                ),
            },
            {
                "q": "Что лучше — потолочный или настенный карниз?",
                "a": (
                    "Потолочный карниз создаёт эффект высоких потолков и "
                    "визуально расширяет пространство. Настенный карниз "
                    "проще в установке и подходит для подвесных потолков. "
                    "Выбор зависит от особенностей помещения."
                ),
            },
            {
                "q": "Есть ли электрические карнизы?",
                "a": (
                    "Да, мы устанавливаем электрические карнизы с мотором. "
                    "Управление через пульт, приложение на телефоне или "
                    "голосом через Apple HomeKit, Google Home, Alexa."
                ),
            },
            {
                "q": "Сколько стоит карниз с установкой?",
                "a": (
                    "При заказе штор карниз и установка включены в стоимость. "
                    "Отдельно карниз с установкой — от 200 AED за погонный метр "
                    "в зависимости от типа и материала."
                ),
            },
        ],
    },
]

# ---------------------------------------------------------------------------
# All landing pages for cross-links (slug -> label)
# ---------------------------------------------------------------------------
ALL_LANDING_PAGES = [
    ("blackout-shtory-dubai", "Блэкаут шторы"),
    ("tyul-na-zakaz-dubai", "Тюль на заказ"),
    ("motorizirovannye-shtory-dubai", "Моторизированные шторы"),
    ("zhalyuzi-dubai", "Жалюзи"),
    ("karnizy-dubai", "Карнизы"),
]


def build_nav_links_html(current_slug):
    """Build the list of navigation links, excluding the current page."""
    links = ['<li><a href="home.html">Главная</a></li>']
    for slug, label in ALL_LANDING_PAGES:
        if slug == current_slug:
            links.append(f'<li><a href="{slug}.html" aria-current="page"><strong>{escape(label)}</strong></a></li>')
        else:
            links.append(f'<li><a href="{slug}.html">{escape(label)}</a></li>')
    return "\n              ".join(links)


def build_faq_html(faq_items):
    """Build the FAQ section HTML."""
    items_html = []
    for item in faq_items:
        items_html.append(f"""          <details class="lp-faq__item">
            <summary class="lp-faq__question">{escape(item["q"])}</summary>
            <div class="lp-faq__answer">
              <p>{escape(item["a"])}</p>
            </div>
          </details>""")
    return "\n".join(items_html)


def build_faq_schema(faq_items):
    """Build the FAQPage JSON-LD schema."""
    entities = []
    for item in faq_items:
        entities.append({
            "@type": "Question",
            "name": item["q"],
            "acceptedAnswer": {
                "@type": "Answer",
                "text": item["a"],
            },
        })
    schema = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": entities,
    }
    return json.dumps(schema, ensure_ascii=False, indent=2)


def build_breadcrumb_schema(page):
    """Build the BreadcrumbList JSON-LD schema."""
    schema = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {
                "@type": "ListItem",
                "position": 1,
                "name": "Главная",
                "item": f"{BASE_URL}/",
            },
            {
                "@type": "ListItem",
                "position": 2,
                "name": page["breadcrumb_name"],
                "item": f"{BASE_URL}/{page['slug']}",
            },
        ],
    }
    return json.dumps(schema, ensure_ascii=False, indent=2)


def build_content_html(paragraphs):
    """Build the content paragraphs HTML."""
    return "\n".join(
        f"          <p>{escape(p)}</p>" for p in paragraphs
    )


def build_cross_links(current_slug):
    """Build the cross-links section for related pages."""
    links = []
    for slug, label in ALL_LANDING_PAGES:
        if slug != current_slug:
            links.append(
                f'          <li><a href="{slug}.html">{escape(label)}</a></li>'
            )
    return "\n".join(links)


def generate_page(page):
    """Generate the complete HTML for a landing page."""

    nav_links = build_nav_links_html(page["slug"])
    faq_html = build_faq_html(page["faq"])
    faq_schema = build_faq_schema(page["faq"])
    breadcrumb_schema = build_breadcrumb_schema(page)
    content_html = build_content_html(page["content_paragraphs"])
    cross_links = build_cross_links(page["slug"])

    html = f"""<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{escape(page["title"])}</title>
  <link rel="canonical" href="{BASE_URL}/{page['slug']}">
  <meta name="description" content="{escape(page["description"])}">
  <meta name="keywords" content="{escape(page["keywords"])}">

  <!-- Open Graph -->
  <meta property="og:title" content="{escape(page["title"])}">
  <meta property="og:description" content="{escape(page["description"])}">
  <meta property="og:type" content="website">
  <meta property="og:url" content="{BASE_URL}/{page['slug']}">
  <meta property="og:image" content="{BASE_URL}/assets/_2024-02-07_14131410.png">
  <meta property="og:locale" content="ru_RU">

  <!-- Twitter Card -->
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{escape(page["title"])}">
  <meta name="twitter:description" content="{escape(page["description"])}">
  <meta name="twitter:image" content="{BASE_URL}/assets/_2024-02-07_14131410.png">

  <!-- Geo -->
  <meta name="geo.region" content="AE-DU">
  <meta name="geo.placename" content="Dubai">
  <meta name="geo.position" content="25.2048;55.2708">
  <meta name="ICBM" content="25.2048, 55.2708">

  <!-- Verification -->
  <meta name="google-site-verification" content="gcDZYvtJ9pRFV-k5aVdlqdMJv5F6ZQyn_srlvuIBJck">
  <meta name="yandex-verification" content="ce618f2e30367a5c">

  <!-- Favicon -->
  <link href="assets/curtain_1.png" rel="shortcut icon" type="image/x-icon">

  <!-- CSS -->
  <link href="assets/tilda-grid-3.0.min.css" rel="stylesheet">
  <link href="assets/fonts.css" rel="stylesheet">
  <link href="assets/tilda-forms-1.0.min.css" rel="stylesheet">

  <!-- Structured Data: BreadcrumbList -->
  <script type="application/ld+json">
{breadcrumb_schema}
  </script>

  <!-- Structured Data: FAQPage -->
  <script type="application/ld+json">
{faq_schema}
  </script>

  <!-- Structured Data: LocalBusiness -->
  <script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "LocalBusiness",
  "name": "Curtains World",
  "description": "{escape(page["description"])}",
  "telephone": "+971589408100",
  "email": "{EMAIL}",
  "address": {{
    "@type": "PostalAddress",
    "streetAddress": "Warehouse 174 Jaddaf",
    "addressLocality": "Dubai",
    "addressRegion": "Dubai",
    "addressCountry": "AE"
  }},
  "geo": {{
    "@type": "GeoCoordinates",
    "latitude": 25.2048,
    "longitude": 55.2708
  }},
  "priceRange": "$$",
  "openingHours": "Mo-Sa 09:00-18:00",
  "url": "{BASE_URL}/{page['slug']}"
}}
  </script>

  <!-- Google Tag Manager -->
  <script>
  (function(w,d,s,l,i){{w[l]=w[l]||[];w[l].push({{'gtm.start':
  new Date().getTime(),event:'gtm.js'}});var f=d.getElementsByTagName(s)[0],
  j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
  'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
  }})(window,document,'script','dataLayer','GTM-W7SR8MSV');
  </script>

  <!-- Yandex.Metrika -->
  <script>
  (function(m,e,t,r,i,k,a){{m[i]=m[i]||function(){{(m[i].a=m[i].a||[]).push(arguments)}};
  m[i].l=1*new Date();
  for(var j=0;j<document.scripts.length;j++){{if(document.scripts[j].src===r){{return;}}}}
  k=e.createElement(t),a=e.getElementsByTagName(t)[0],k.async=1,k.src=r,a.parentNode.insertBefore(k,a)
  }})(window,document,"script","https://mc.yandex.ru/metrika/tag.js","ym");
  ym(96561300,"init",{{clickmap:true,trackLinks:true,accurateTrackBounce:true,webvisor:true}});
  </script>
  <noscript><div><img alt="" src="https://mc.yandex.ru/watch/96561300" style="position:absolute;left:-9999px;" /></div></noscript>

  <style>
    /* ===== Reset & Base ===== */
    *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
    html {{ scroll-behavior: smooth; }}
    body {{
      font-family: 'Montserrat', Arial, sans-serif;
      color: #333;
      line-height: 1.6;
      background: #fff;
      -webkit-font-smoothing: antialiased;
    }}
    a {{ color: #6e8b74; text-decoration: none; transition: color .2s; }}
    a:hover {{ color: #4a6b50; }}
    img {{ max-width: 100%; height: auto; }}

    /* ===== Header ===== */
    .lp-header {{
      position: sticky; top: 0; z-index: 100;
      background: #fff;
      border-bottom: 1px solid #eee;
      padding: 0 20px;
    }}
    .lp-header__inner {{
      max-width: 1200px; margin: 0 auto;
      display: flex; align-items: center; justify-content: space-between;
      min-height: 64px;
    }}
    .lp-header__logo {{
      font-family: 'Montserrat', Arial, sans-serif;
      font-size: 22px; font-weight: 700; color: #333;
    }}
    .lp-header__logo a {{ color: inherit; }}
    .lp-header__cta {{
      display: inline-block;
      padding: 10px 24px;
      background: #7a8d7e;
      color: #fff;
      border-radius: 5px;
      font-family: 'Montserrat', Arial, sans-serif;
      font-size: 14px; font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.02em;
      transition: background .2s;
    }}
    .lp-header__cta:hover {{ background: #6e8b74; color: #fff; }}

    /* Mobile menu toggle */
    .lp-header__menu-btn {{
      display: none; background: none; border: none; cursor: pointer;
      width: 28px; height: 20px; position: relative;
    }}
    .lp-header__menu-btn span {{
      display: block; position: absolute; width: 100%; height: 3px;
      background: #7a8d7e; left: 0; transition: .25s;
    }}
    .lp-header__menu-btn span:nth-child(1) {{ top: 0; }}
    .lp-header__menu-btn span:nth-child(2) {{ top: 8px; }}
    .lp-header__menu-btn span:nth-child(3) {{ top: 16px; }}

    /* ===== Navigation ===== */
    .lp-nav {{ background: #fafaf8; border-bottom: 1px solid #eee; }}
    .lp-nav__inner {{
      max-width: 1200px; margin: 0 auto; padding: 0 20px;
    }}
    .lp-nav ul {{
      list-style: none; display: flex; flex-wrap: wrap; gap: 0;
    }}
    .lp-nav li a {{
      display: block; padding: 12px 16px;
      font-size: 14px; font-weight: 600; color: #333;
      transition: color .2s, background .2s;
    }}
    .lp-nav li a:hover {{ color: #6e8b74; background: #f0ede8; }}
    .lp-nav li a[aria-current="page"] {{ color: #6e8b74; }}

    /* ===== Hero ===== */
    .lp-hero {{
      background: linear-gradient(135deg, #f8f2e9 0%, #e8e0d5 100%);
      padding: 60px 20px 50px;
      text-align: center;
    }}
    .lp-hero__inner {{ max-width: 800px; margin: 0 auto; }}
    .lp-hero h1 {{
      font-family: 'Montserrat', Arial, sans-serif;
      font-size: 36px; font-weight: 700; color: #333;
      margin-bottom: 16px; line-height: 1.25;
    }}
    .lp-hero__subtitle {{
      font-size: 18px; color: #555; margin-bottom: 28px; line-height: 1.5;
    }}
    .lp-hero__cta {{
      display: inline-block;
      padding: 14px 36px;
      background: #6e8b74;
      color: #fff;
      border-radius: 8px;
      font-size: 16px; font-weight: 700;
      text-transform: uppercase;
      transition: background .2s, transform .15s;
    }}
    .lp-hero__cta:hover {{ background: #5a7a60; color: #fff; transform: translateY(-1px); }}

    /* ===== Breadcrumb ===== */
    .lp-breadcrumb {{
      max-width: 1200px; margin: 0 auto; padding: 16px 20px;
      font-size: 13px; color: #888;
    }}
    .lp-breadcrumb a {{ color: #6e8b74; }}
    .lp-breadcrumb span {{ margin: 0 6px; }}

    /* ===== Content ===== */
    .lp-content {{
      max-width: 800px; margin: 0 auto;
      padding: 40px 20px 50px;
    }}
    .lp-content h2 {{
      font-family: 'Montserrat', Arial, sans-serif;
      font-size: 28px; font-weight: 700; color: #333;
      margin-bottom: 20px;
    }}
    .lp-content p {{
      font-size: 16px; color: #444; margin-bottom: 18px;
      font-family: 'Ubuntu', 'Montserrat', Arial, sans-serif;
    }}

    /* ===== CTA Banner ===== */
    .lp-cta-banner {{
      background: #6e8b74; color: #fff;
      padding: 50px 20px; text-align: center;
    }}
    .lp-cta-banner__inner {{ max-width: 700px; margin: 0 auto; }}
    .lp-cta-banner h2 {{
      font-size: 28px; font-weight: 700; margin-bottom: 12px; color: #fff;
    }}
    .lp-cta-banner p {{
      font-size: 16px; margin-bottom: 24px; opacity: .9;
    }}
    .lp-cta-banner__btn {{
      display: inline-block;
      padding: 14px 36px;
      background: #fff; color: #6e8b74;
      border-radius: 8px;
      font-size: 16px; font-weight: 700;
      transition: background .2s, transform .15s;
    }}
    .lp-cta-banner__btn:hover {{ background: #f0f0f0; color: #5a7a60; transform: translateY(-1px); }}

    /* ===== FAQ ===== */
    .lp-faq {{
      max-width: 800px; margin: 0 auto;
      padding: 50px 20px 60px;
    }}
    .lp-faq h2 {{
      font-family: 'Montserrat', Arial, sans-serif;
      font-size: 28px; font-weight: 700; color: #333;
      margin-bottom: 24px; text-align: center;
    }}
    .lp-faq__item {{
      border-bottom: 1px solid #e0e0e0;
    }}
    .lp-faq__question {{
      padding: 18px 40px 18px 0;
      font-size: 16px; font-weight: 600; color: #333;
      cursor: pointer; position: relative;
      list-style: none;
      font-family: 'Montserrat', Arial, sans-serif;
    }}
    .lp-faq__question::-webkit-details-marker {{ display: none; }}
    .lp-faq__question::after {{
      content: '+'; position: absolute; right: 0; top: 50%;
      transform: translateY(-50%);
      font-size: 22px; font-weight: 300; color: #6e8b74;
      transition: transform .2s;
    }}
    details[open] .lp-faq__question::after {{
      content: '\\2212'; /* minus sign */
    }}
    .lp-faq__answer {{
      padding: 0 0 18px;
      font-family: 'Ubuntu', 'Montserrat', Arial, sans-serif;
    }}
    .lp-faq__answer p {{ font-size: 15px; color: #555; line-height: 1.6; }}

    /* ===== Cross-links ===== */
    .lp-related {{
      background: #fafaf8; padding: 40px 20px;
    }}
    .lp-related__inner {{
      max-width: 800px; margin: 0 auto;
    }}
    .lp-related h2 {{
      font-family: 'Montserrat', Arial, sans-serif;
      font-size: 22px; font-weight: 700; color: #333;
      margin-bottom: 16px;
    }}
    .lp-related ul {{ list-style: none; display: flex; flex-wrap: wrap; gap: 10px; }}
    .lp-related li a {{
      display: inline-block;
      padding: 8px 20px;
      background: #fff;
      border: 1px solid #ddd;
      border-radius: 20px;
      font-size: 14px; font-weight: 600; color: #333;
      transition: border-color .2s, color .2s;
    }}
    .lp-related li a:hover {{ border-color: #6e8b74; color: #6e8b74; }}

    /* ===== Footer ===== */
    .lp-footer {{
      background: #333; color: #ccc; padding: 40px 20px;
    }}
    .lp-footer__inner {{
      max-width: 1200px; margin: 0 auto;
      display: flex; flex-wrap: wrap; gap: 40px;
      justify-content: space-between;
    }}
    .lp-footer__col {{ flex: 1; min-width: 200px; }}
    .lp-footer__col h3 {{
      font-size: 16px; font-weight: 700; color: #fff;
      margin-bottom: 12px;
      font-family: 'Montserrat', Arial, sans-serif;
    }}
    .lp-footer__col p, .lp-footer__col a {{
      font-size: 14px; color: #aaa; line-height: 1.8;
    }}
    .lp-footer__col a:hover {{ color: #fff; }}
    .lp-footer__col ul {{ list-style: none; }}
    .lp-footer__col ul li a {{
      display: block; padding: 2px 0;
      font-size: 14px; color: #aaa;
    }}
    .lp-footer__col ul li a:hover {{ color: #fff; }}
    .lp-footer__bottom {{
      max-width: 1200px; margin: 24px auto 0;
      padding-top: 20px; border-top: 1px solid #555;
      font-size: 13px; color: #777; text-align: center;
    }}

    /* ===== WhatsApp Button ===== */
    .wa-float {{
      position: fixed; bottom: 20px; right: 20px; z-index: 9999;
      width: 60px; height: 60px; border-radius: 50%;
      background: #25D366;
      display: flex; align-items: center; justify-content: center;
      box-shadow: 0 4px 12px rgba(0,0,0,.25);
      cursor: pointer; transition: transform .2s;
    }}
    .wa-float:hover {{ transform: scale(1.1); }}
    .wa-float svg {{ width: 32px; height: 32px; fill: #fff; }}

    /* ===== Responsive ===== */
    @media (max-width: 768px) {{
      .lp-hero h1 {{ font-size: 28px; }}
      .lp-hero__subtitle {{ font-size: 16px; }}
      .lp-content h2, .lp-faq h2, .lp-cta-banner h2 {{ font-size: 24px; }}
      .lp-header__cta {{ padding: 8px 16px; font-size: 12px; }}
      .lp-nav ul {{ flex-direction: column; }}
      .lp-nav li a {{ padding: 10px 16px; border-bottom: 1px solid #eee; }}
      .lp-footer__inner {{ flex-direction: column; gap: 24px; }}
    }}
    @media (max-width: 480px) {{
      .lp-hero {{ padding: 40px 16px 36px; }}
      .lp-hero h1 {{ font-size: 24px; }}
      .lp-content {{ padding: 30px 16px 40px; }}
      .lp-faq {{ padding: 30px 16px 40px; }}
      .lp-related {{ padding: 30px 16px; }}
    }}
    @media (min-width: 960px) {{
      .wa-float {{ bottom: 30px; right: 30px; }}
    }}
  </style>
</head>
<body>
  <!-- Google Tag Manager (noscript) -->
  <noscript><iframe src="https://www.googletagmanager.com/ns.html?id=GTM-W7SR8MSV" height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>

  <!-- Header -->
  <header class="lp-header">
    <div class="lp-header__inner">
      <div class="lp-header__logo"><a href="home.html">Curtains World</a></div>
      <a href="{WA_LINK}" target="_blank" rel="noopener" class="lp-header__cta">
        Бесплатный замер
      </a>
    </div>
  </header>

  <!-- Navigation -->
  <nav class="lp-nav" aria-label="Каталог">
    <div class="lp-nav__inner">
      <ul>
        {nav_links}
      </ul>
    </div>
  </nav>

  <!-- Breadcrumb -->
  <div class="lp-breadcrumb" aria-label="Хлебные крошки">
    <a href="home.html">Главная</a>
    <span>/</span>
    {escape(page["breadcrumb_name"])}
  </div>

  <!-- Hero -->
  <section class="lp-hero">
    <div class="lp-hero__inner">
      <h1>{escape(page["h1"])}</h1>
      <p class="lp-hero__subtitle">{escape(page["description"])}</p>
      <a href="{WA_LINK}" target="_blank" rel="noopener" class="lp-hero__cta">
        Заказать бесплатный замер
      </a>
    </div>
  </section>

  <!-- Content -->
  <article class="lp-content">
    <h2>О продукте</h2>
{content_html}
  </article>

  <!-- CTA Banner -->
  <section class="lp-cta-banner">
    <div class="lp-cta-banner__inner">
      <h2>Закажите бесплатный замер</h2>
      <p>Наш специалист приедет в удобное время, снимет размеры и поможет подобрать ткань. Замер, доставка и установка бесплатно.</p>
      <a href="{WA_LINK}" target="_blank" rel="noopener" class="lp-cta-banner__btn">
        Написать в WhatsApp
      </a>
      <p style="margin-top:16px; margin-bottom:0; font-size:14px;">
        Или позвоните: <a href="{PHONE_LINK}" style="color:#fff; text-decoration:underline;">{PHONE}</a>
      </p>
    </div>
  </section>

  <!-- FAQ -->
  <section class="lp-faq">
    <h2>Часто задаваемые вопросы</h2>
{faq_html}
  </section>

  <!-- Related pages -->
  <section class="lp-related">
    <div class="lp-related__inner">
      <h2>Другие услуги</h2>
      <ul>
{cross_links}
      </ul>
    </div>
  </section>

  <!-- Footer -->
  <footer class="lp-footer">
    <div class="lp-footer__inner">
      <div class="lp-footer__col">
        <h3>Curtains World</h3>
        <p>Шторы и занавески на заказ<br>в Дубае из натуральных тканей</p>
      </div>
      <div class="lp-footer__col">
        <h3>Контакты</h3>
        <p>
          <a href="{PHONE_LINK}">{PHONE}</a><br>
          <a href="mailto:{EMAIL}">{EMAIL}</a><br>
          Warehouse 174 Jaddaf, Dubai
        </p>
      </div>
      <div class="lp-footer__col">
        <h3>Каталог</h3>
        <ul>
          <li><a href="home.html">Главная</a></li>
          <li><a href="blackout-shtory-dubai.html">Блэкаут шторы</a></li>
          <li><a href="tyul-na-zakaz-dubai.html">Тюль на заказ</a></li>
          <li><a href="motorizirovannye-shtory-dubai.html">Моторизированные шторы</a></li>
          <li><a href="zhalyuzi-dubai.html">Жалюзи</a></li>
          <li><a href="karnizy-dubai.html">Карнизы</a></li>
        </ul>
      </div>
    </div>
    <div class="lp-footer__bottom">
      &copy; 2024 Curtains World. Все права защищены.
    </div>
  </footer>

  <!-- Meta Pixel Code -->
  <script>
  !function(f,b,e,v,n,t,s)
  {{if(f.fbq)return;n=f.fbq=function(){{n.callMethod?
  n.callMethod.apply(n,arguments):n.queue.push(arguments)}};
  if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';
  n.queue=[];t=b.createElement(e);t.async=!0;
  t.src=v;s=b.getElementsByTagName(e)[0];
  s.parentNode.insertBefore(t,s)}}(window,document,'script',
  'https://connect.facebook.net/en_US/fbevents.js');
  fbq('init','315622264851387');
  fbq('track','PageView');
  </script>
  <noscript><img height="1" width="1" style="display:none" src="https://www.facebook.com/tr?id=315622264851387&ev=PageView&noscript=1" alt="" /></noscript>

  <!-- WhatsApp Float Button -->
  <a href="{WA_LINK}" target="_blank" rel="noopener" class="wa-float" aria-label="Написать в WhatsApp">
    <svg viewBox="0 0 24 24"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z"/></svg>
  </a>
</body>
</html>"""

    return html


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))

    for page in PAGES:
        html = generate_page(page)
        filepath = os.path.join(script_dir, page["filename"])
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"Generated: {page['filename']}")

    print(f"\nDone! Generated {len(PAGES)} landing pages.")


if __name__ == "__main__":
    main()
