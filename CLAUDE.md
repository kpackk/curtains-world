# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Статический сайт «Curtains World» — шторы на заказ в Дубае. Клон Tilda-сайта (curtainsfactory.ae), локализованный для автономного хостинга. Бренд: Curtains World (ранее Curtains Factory).

## Architecture

**HTML-страницы:**
- `home.html` — основная русская версия (653 строки, ~350KB). Содержит длинные строки (по ~50-100KB каждая) с встроенными CSS и HTML-блоками
- `home-ru.html` — резервная копия оригинала (521 строка)

**Python-утилиты:**
- `clone_page.py` — клонирует страницу, парсит через BeautifulSoup, скачивает ассеты, перезаписывает пути
- `download_fonts.py` — скачивает Google Fonts (Ubuntu, Montserrat), генерирует `assets/css/fonts.css`
- `fix_images.py` — повторно скачивает изображения с Tilda CDN, исправляет lazy-loading (data-original → src)

**Ассеты (`assets/`):**
- `css/` (11 файлов) — Tilda CSS-фреймворк + `fonts.css`
- `js/` (20 файлов) — jQuery 1.10.2, HammerJS, модули Tilda
- `fonts/` (29 woff2) — Ubuntu и Montserrat
- `images/` (44 файла) — фото продуктов, UI-элементы

**SEO-файлы:** `robots.txt`, `sitemap.xml`

## Commands

```bash
# Локальный сервер для разработки
python3 -m http.server 8888

# Клонировать страницу и скачать все ассеты
python3 clone_page.py

# Скачать шрифты
python3 download_fonts.py

# Переcкачать изображения и исправить lazy-loading
python3 fix_images.py
```

Сборки, тестов и линтинга нет — проект полностью статический.

## Tilda-специфичные паттерны

### Дублирование блоков (КРИТИЧЕСКИ ВАЖНО)
Tilda T809 (UTM-блок) создаёт **два идентичных hero-блока** с одинаковыми ID элементов:
- `rec849367567` — **СКРЫТЫЙ** (display:none, управляется T809 UTM-логикой)
- `rec849367570` — **ВИДИМЫЙ** (display:block, реально отображается)

При редактировании hero-секции всегда проверяй `display` через JS: `window.getComputedStyle(document.getElementById('recXXX')).display`

### Позиционирование T396 (абсолютные блоки)
Tilda T396 использует абсолютное позиционирование. Для мобильных breakpoints нужно менять **оба места**:
1. `data-field-top-res-320-value` / `data-field-top-res-480-value` (data-атрибуты, читаются JS)
2. Inline CSS: `@media (max-width:479px)` / `@media (max-width:639px)` (фактический стиль)

### Редактирование длинных строк
HTML содержит строки по 50-100KB. Инструмент Edit не всегда находит подстроки. Надёжный способ — Python-скрипт:
```bash
python3 -c "
p='/Users/rus/Desktop/FENESTRA/сайт 1 рус дубай/home.html'
c=open(p).read()
c=c.replace('OLD_STRING','NEW_STRING',1)
open(p,'w').write(c)
"
```

### Прочие паттерны
- Lazy-loading: `data-original` вместо `src` для изображений
- Страничные стили: привязаны к ID страниц Tilda (`tilda-blocks-page47546363.min.css`)
- HTML содержит `onerror`/`onload` обработчики для fallback-загрузки
- Конфигурации: `assets_mapping.json` (URL → файл), `assets_to_download.json` (манифест)
- Аналитика: Google Tag Manager (GTM-W7SR8MSV), Yandex.Metrika, Facebook Pixel
- Schema.org: JSON-LD (LocalBusiness + FAQPage) встроен в home.html
