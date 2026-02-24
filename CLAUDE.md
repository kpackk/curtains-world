# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Статический сайт «Curtains World» — шторы на заказ в Дубае (домен: curtainsfactory.ae). Клон Tilda-сайта, полностью локализованный для автономного хостинга. Ноль внешних CDN-зависимостей — все ассеты (JS, CSS, шрифты, изображения) скачаны локально.

## Architecture

**HTML-страницы:**
- `home.html` — основная русская версия (~900 строк, но строки длинные — 50-100KB каждая, общий размер ~370KB)
- `home-ru.html` — резервная копия оригинала
- `blackout-shtory-dubai.html`, `tyul-na-zakaz-dubai.html`, `karnizy-dubai.html`, `motorizirovannye-shtory-dubai.html`, `zhalyuzi-dubai.html` — продуктовые страницы

**Python-утилиты:**
- `clone_page.py` — клонирует страницу с curtainsfactory.ae, парсит через BeautifulSoup, скачивает ассеты, перезаписывает пути
- `download_fonts.py` — скачивает Google Fonts (Ubuntu, Montserrat), генерирует `assets/css/fonts.css`
- `fix_images.py` — переcкачивает изображения с Tilda CDN, исправляет lazy-loading

**Ассеты (`assets/`):**
- `css/` — Tilda CSS-фреймворк (11 файлов) + `fonts.css`
- `js/` — jQuery 1.10.2, HammerJS, модули Tilda (21 файл, включая `tilda-phone-mask-1.1.min.js`)
- `fonts/` — woff2-файлы Ubuntu и Montserrat (11 файлов)
- `images/` — WebP-фото продуктов, UI-элементы (54 файла)

**SEO:** `robots.txt`, `sitemap.xml`, Schema.org JSON-LD (LocalBusiness + FAQPage) в home.html

## Commands

```bash
# Локальный сервер для разработки
python3 -m http.server 8888

# Публичный туннель для тестирования на телефоне
ssh -R 80:localhost:8888 -o ServerAliveInterval=30 serveo.net

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
