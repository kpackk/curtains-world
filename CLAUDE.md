# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Статический сайт «Curtains World» — шторы на заказ в Дубае (домен: curtainsfactory.ae). Клон Tilda-сайта, полностью локализованный для автономного хостинга. Ноль внешних CDN-зависимостей — все ассеты (JS, CSS, шрифты, изображения) скачаны локально.

## Architecture

### Два типа страниц

**Tilda-страницы (home.html):**
- `home.html` — основная русская версия (~650 строк, строки длинные — 50-100KB каждая, общий размер ~370KB)
- `home-ru.html` — резервная копия оригинала
- Построены на Tilda-фреймворке: абсолютное позиционирование (T396), div-блоки с ID `recXXXXXX`
- Зависят от Tilda CSS/JS из `assets/css/` и `assets/js/`

**Генерируемые продуктовые страницы (семантический HTML):**
- `blackout-shtory-dubai.html`, `tyul-na-zakaz-dubai.html`, `karnizy-dubai.html`, `motorizirovannye-shtory-dubai.html`, `zhalyuzi-dubai.html`
- Создаются скриптом `generate_pages.py` — семантический HTML, `<details>` для FAQ, BreadcrumbList schema
- Не зависят от Tilda CSS/JS — свои встроенные стили
- Перегенерация: `python3 generate_pages.py`

### Python-утилиты

| Скрипт | Назначение |
|--------|-----------|
| `generate_pages.py` | Генерирует 5 продуктовых лендингов с schema, аналитикой, навигацией |
| `optimize_images.py` | Конвертирует PNG/JPG → WebP через Pillow (качество 80, экономия ~90%) |
| `clone_page.py` | Клонирует страницу с curtainsfactory.ae, скачивает ассеты |
| `download_fonts.py` | Скачивает Google Fonts (Ubuntu, Montserrat) → `assets/fonts/` |
| `fix_images.py` | Переcкачивает изображения с Tilda CDN, исправляет lazy-loading |

### Ассеты

`assets/` содержит как организованные подпапки, так и файлы в корне (legacy от clone_page.py):
- `css/` (11 файлов) — Tilda CSS + `fonts.css`
- `js/` (21 файл) — jQuery 1.10.2, HammerJS, модули Tilda
- `fonts/` (11 woff2) — Ubuntu и Montserrat
- `images/` (54 файла) — PNG-оригиналы + WebP-версии
- Корень `assets/` — дубли изображений и скриптов (legacy, используются в home.html напрямую)

**Конфигурации:** `assets_mapping.json` (URL → локальный файл), `assets_to_download.json` (манифест для clone_page.py)

**SEO:** `robots.txt`, `sitemap.xml` (индексируются только 3 из 6 страниц), Schema.org JSON-LD в каждой странице

## Commands

```bash
# Локальный сервер для разработки
python3 -m http.server 8888

# Публичный туннель для тестирования на телефоне
ssh -R 80:localhost:8888 -o ServerAliveInterval=30 serveo.net

# Перегенерировать продуктовые страницы после изменений в generate_pages.py
python3 generate_pages.py

# Конвертировать изображения в WebP (требует: pip3 install Pillow)
python3 optimize_images.py

# Клонировать страницу и скачать все ассеты
python3 clone_page.py

# Скачать шрифты
python3 download_fonts.py
```

Сборки, тестов и линтинга нет — проект полностью статический.

## Tilda-специфичные паттерны

### Формы бронирования
Формы `form849367596` (мобильная) и `form849367597` (десктопная) отправляют данные в WhatsApp (+971 58 940 8100). Tilda backend отключён: класс `js-form-proccess` заменён на `js-form-whatsapp`, `data-formactiontype="0"`. jQuery-обработчик submit собирает поля и открывает `wa.me`.

### CTA-кнопки "Бесплатный замер"
Кнопки `href="#booking"` прокручивают к форме через jQuery-обработчик с `setTimeout(50)` — задержка нужна, чтобы обойти Tilda-обработчики, которые перехватывают scroll. JS определяет видимую форму: `rec849367597` (десктоп, `screen-min 480px`) → fallback `rec849367595` (мобильная).

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
- Страничные стили привязаны к ID страниц Tilda (`tilda-blocks-page61146805.min.css`)
- Калькулятор: ucalc.pro виджет (ID 451257) в блоке `rec849367592`
- Аналитика: Google Tag Manager (GTM-W7SR8MSV), Yandex.Metrika (96561300)
- WhatsApp номер: +971 58 940 8100 (используется в формах и плавающей кнопке)
