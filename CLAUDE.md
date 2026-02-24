# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Статический сайт для бизнеса по продаже штор (curtainsfactory.ae), созданный на платформе Tilda и локализованный для автономного хостинга. Python-скрипты используются для клонирования страниц и скачивания всех внешних зависимостей.

## Architecture

**Две HTML-страницы** — полные клоны Tilda-сайта с локализованными ассетами:
- `home.html` — русская версия (~7700 строк)
- `curtains-dubai.html` — английская версия (~8800 строк)

**Python-утилиты:**
- `clone_page.py` — скачивает страницу с curtainsfactory.ae, парсит через BeautifulSoup, скачивает все ассеты и перезаписывает пути на локальные
- `download_fonts.py` — скачивает Google Fonts (Ubuntu, Montserrat) и генерирует локальный `assets/css/fonts.css`

**Ассеты (`assets/`):**
- `css/` — Tilda CSS-фреймворк (grid, animation, forms, catalog, popup, slider, zoom) + `fonts.css`
- `js/` — jQuery 1.10.2, HammerJS, модули Tilda (22 файла, все минифицированные)
- `fonts/` — woff2-файлы Ubuntu и Montserrat
- `images/` — фото продуктов, UI-элементы, логотипы

## Commands

```bash
# Клонировать страницу и скачать все ассеты
python3 clone_page.py

# Скачать шрифты Google Fonts
python3 download_fonts.py
```

Сборки, тестов и линтинга нет — проект полностью статический.

## Key Patterns

- Tilda использует `data-original` вместо `src` для lazy-loading изображений — `clone_page.py` обрабатывает это отдельно
- Страничные стили и скрипты привязаны к ID страниц Tilda (например, `tilda-blocks-page47546363.min.css`)
- HTML содержит `onerror`/`onload` обработчики для fallback-загрузки стилей
- Конфигурации ассетов: `assets_mapping.json` (URL → имя файла), `assets_to_download.json` (полный манифест)
- Аналитика: Google Tag Manager (GTM-W7SR8MSV), Yandex.Metrika, Facebook Pixel
