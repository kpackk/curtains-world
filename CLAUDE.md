# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Статический сайт «Curtains World» — шторы на заказ в Дубае. Клон Tilda-сайта, полностью локализованный для автономного хостинга. Своего домена пока нет — сайт хостится на GitHub Pages. Ноль внешних CDN-зависимостей — все ассеты (JS, CSS, шрифты, изображения) скачаны локально. Все изображения в формате WebP. Единственная внешняя зависимость — виджет калькулятора ucalc.pro (загружается по scroll).

**Хостинг:** GitHub Pages — https://kpackk.github.io/curtains-world/ (ветка `master`, `.nojekyll` отключает Jekyll)
**Репозиторий:** https://github.com/kpackk/curtains-world

## Architecture

### Три типа страниц

**Tilda-страница (home.html):**
- `home.html` — основная русская версия (~650 строк, строки длинные — 50-100KB каждая, общий размер ~370KB)
- Построена на Tilda-фреймворке: абсолютное позиционирование (T396), div-блоки с ID `recXXXXXX`
- Зависит от Tilda CSS/JS из `assets/`
- Schema.org JSON-LD: `HomeAndConstructionBusiness`, `LocalBusiness`, `FAQPage`, `ItemList`, `BreadcrumbList`

**Генерируемые страницы (семантический HTML) — `generate_pages.py`:**
- 5 продуктовых лендингов: `blackout-shtory-dubai.html`, `tyul-na-zakaz-dubai.html`, `karnizy-dubai.html`, `motorizirovannye-shtory-dubai.html`, `zhalyuzi-dubai.html`
- 8 блог-статей: `blog-kak-vybrat-shtory-dubai.html`, `blog-blackout-shtory-plyusy-minusy.html`, `blog-motorizirovannye-shtory-stoit-li.html`, `blog-ukhod-za-shtorami-oae.html`, `blog-shtory-dlya-arendnoj-kvartiry-dubai.html`, `blog-zhalyuzi-ili-shtory-dubai.html`, `blog-karnizy-tipy-i-vybor.html`, `blog-shtory-dlya-panoramnykh-okon.html`
- 1 индексная страница блога: `blog.html` (карточки статей, CollectionPage schema)
- Всего 14 страниц. Не зависят от Tilda CSS/JS — свои встроенные стили
- Перегенерация: `python3 generate_pages.py`

**Служебные страницы:**
- `index.html` — meta refresh редирект на `home.html`
- `404.html` — страница ошибки (тёмная тема, кнопка на главную с относительным путём `home.html`)

### Генератор страниц (generate_pages.py)

Центральный скрипт проекта. Структура:
1. **Константы** (BASE_URL, PHONE, WA_LINK, EMAIL)
2. **LANDING_PAGES** — конфиг 5 продуктовых страниц (title, desc, keywords, FAQ, контент)
3. **BLOG_ARTICLES** — конфиг 8 блог-статей (h1, content_sections с h2/h3, FAQ)
4. **Маппинги перелинковки:**
   - `ALL_LANDING_PAGES`, `ALL_BLOG_ARTICLES` — полные списки slug→label
   - `PRODUCT_BLOG_RELATED` — какие блог-статьи показывать на продуктовой странице
   - `BLOG_PRODUCT_RELATED` — какие продукты показывать на блог-странице
5. **Builder-функции** — `build_nav_links_html()`, `build_faq_html()`, `build_cross_links()`, `build_related_blog_links()`, `build_related_product_links()`, `build_footer_html()`
6. **Шаблоны** — `generate_blog_article()`, `generate_page()`, `generate_blog_index()` — полный HTML с inline CSS, аналитикой, schema
7. **main()** — генерирует все 14 файлов

**При добавлении нового блога** нужно обновить 4 места: `BLOG_ARTICLES`, `ALL_BLOG_ARTICLES`, `PRODUCT_BLOG_RELATED`, `BLOG_PRODUCT_RELATED`, а также `sitemap.xml`.

Продуктовые страницы: BreadcrumbList + FAQPage + LocalBusiness + AggregateRating schema
Блог-статьи: BreadcrumbList (3 уровня) + Article + FAQPage schema
Блог-индекс: BreadcrumbList + CollectionPage schema

### Перелинковка

- Продуктовые страницы: секция «Другие услуги» (4 продукта) + «Полезные статьи» (2 блога)
- Блог-статьи: секция «Читайте также» (4 статьи) + «Наши услуги» (2-3 продукта)
- Footer на всех сгенерированных страницах: полный каталог + все блог-статьи
- home.html: кнопка «Блог» → первая блог-статья

### Аналитика и трекинг

Аналитика **удалена**: Yandex.Metrika 96561300 принадлежала оригинальному сайту (клон). GTM-контейнер GTM-W7SR8MSV также удалён ранее. При необходимости — добавить свой счётчик.

- **UTM capture:** sessionStorage для utm_source/medium/campaign/term/content (сохраняется на сгенерированных страницах)

### Python-утилиты

| Скрипт | Назначение |
|--------|-----------|
| `generate_pages.py` | Генерирует 14 страниц (5 продуктов + 8 блогов + 1 индекс) |
| `optimize_images.py` | Конвертирует PNG/JPG → WebP через Pillow (качество 80) |
| `clone_page.py` | Клонирует страницу, скачивает ассеты |
| `download_fonts.py` | Скачивает Google Fonts (Ubuntu, Montserrat) → `assets/fonts/` |
| `fix_images.py` | Перескачивает изображения с Tilda CDN, исправляет lazy-loading |

### Ассеты

`assets/` — плоская структура (подпапки `js/` и `images/` удалены как дубликаты):
- `fonts/` (17 woff2) — Ubuntu (300, 400, 500, 700) и Montserrat (100-900 variable). Все `@font-face` имеют `font-display: swap`
- Корень `assets/` — WebP-изображения, JS-скрипты Tilda, CSS-файлы, `flags7.png` (спрайт флагов для телефонной маски)

**SEO:** `robots.txt`, `sitemap.xml` (15 URL), Schema.org JSON-LD на каждой странице, `favicon.ico` + `apple-touch-icon.png`

## Commands

```bash
# Локальный сервер для разработки
python3 -m http.server 8888

# Публичный туннель для тестирования на телефоне
ssh -R 80:localhost:8888 -o ServerAliveInterval=30 serveo.net

# Перегенерировать все страницы после изменений в generate_pages.py
python3 generate_pages.py

# Конвертировать изображения в WebP (требует: pip3 install Pillow)
python3 optimize_images.py

# Lighthouse-аудит (npx, без глобальной установки)
npx lighthouse https://kpackk.github.io/curtains-world/home.html --output=json --chrome-flags="--headless --no-sandbox" --only-categories=performance,accessibility,best-practices,seo
```

Сборки, тестов и линтинга нет — проект полностью статический.

## GitHub Pages

- Деплой: `git push origin master` — GitHub Pages автоматически публикует из корня ветки `master`
- `.nojekyll` в корне — отключает Jekyll. Без этого файлы с `_` в имени отдают 404
- Файлы изображений переименованы с `_2024-*` → `img_2024-*` из-за Jekyll-ограничения
- `tilda-forms-1.0.min.css` загружается асинхронно через `media="print" onload` на сгенерированных страницах

## Lighthouse scores

**home.html (февраль 2026):**
Performance 87-97 | Best Practices 96 | FCP 1.6s | TBT 10ms | CLS 0

**Сгенерированные страницы:**
Performance 95 | Accessibility 100 | Best Practices 100 | SEO 100

### Performance-оптимизации home.html
- Render-blocking CSS: 124KB → 0 (deferred forms/animation/cards/date-picker/page CSS)
- Critical CSS (2.6KB), fonts.css, grid CSS — inlined в `<head>`
- Hero image: `fetchpriority="high"` на preload, сжат до 86KB
- Lazy-bundle JS: 5 файлов загружаются по scroll/touchstart (forms, hammer, animation, blocks, cards)
- jQuery, tilda-products, tilda-slds — удалены (не используются)
- Yandex.Metrika, GTM — удалены (чужие счётчики от оригинального клона)
- Phone-mask flags sprite скачан локально (`assets/flags7.png`)

## Tilda-специфичные паттерны

### Формы бронирования
Формы `form849367596` (мобильная) и `form849367597` (десктопная) отправляют данные в WhatsApp (+971 58 940 8100). Tilda backend отключён: класс `js-form-proccess` заменён на `js-form-whatsapp`, `data-formactiontype="0"`. Vanilla JS обработчик submit собирает поля и открывает `wa.me`.

### CTA-кнопки "Бесплатный замер"
Кнопки `href="#booking"` прокручивают к форме через vanilla JS обработчик с `setTimeout(50)` — задержка нужна, чтобы обойти Tilda-обработчики, которые перехватывают scroll. JS определяет видимую форму: `rec849367597` (десктоп, `screen-min 480px`) → fallback `rec849367595` (мобильная).

### Tilda исключает якоря `#order*`
Tilda menu JS содержит `:not([href^="#order"])` — любые якоря, начинающиеся с `#order`, игнорируются. Поэтому используется `#booking`.

### Дублирование hero-блоков (T809 UTM)
Tilda T809 создаёт **два** hero-блока:
- `rec849367567` — СКРЫТЫЙ (display:none, UTM-логика)
- `rec849367570` — ВИДИМЫЙ

При редактировании hero проверяй `display` через JS.

### Позиционирование T396 (абсолютные блоки)
Для мобильных breakpoints менять **два места**:
1. `data-field-top-res-320-value` / `data-field-top-res-480-value`
2. Inline CSS: `@media (max-width:479px)` / `@media (max-width:639px)`

### Редактирование длинных строк
HTML содержит строки по 50-100KB. Если Edit не находит подстроку, использовать Python:
```bash
python3 -c "
p='/Users/rus/Desktop/FENESTRA/сайт 1 рус дубай/home.html'
c=open(p).read()
c=c.replace('OLD_STRING','NEW_STRING',1)
open(p,'w').write(c)
"
```

### Прочее
- Lazy-loading: `data-original` вместо `src` для изображений
- Страничные стили привязаны к ID страниц Tilda (`tilda-blocks-page61146805.min.css` в `assets/`)
- Калькулятор: ucalc.pro виджет (ID 451257) в блоке `rec849367592`
- WhatsApp номер: +971 58 940 8100 (используется в формах и плавающей кнопке)
