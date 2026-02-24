# Комплексное улучшение сайта Curtains World — План реализации

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Подготовить сайт Curtains World к запуску: SEO-оптимизация, повышение конверсий, контентное расширение, техническая оптимизация.

**Architecture:** Статический HTML-сайт, клонированный с Tilda. Файл `home.html` (653 строки, ~350KB) — основная русская страница. Tilda использует абсолютное позиционирование (T396), lazy-loading через `data-original`, и div'ы вместо семантических тегов. Строки в файле очень длинные (50-100KB), поэтому для замен лучше использовать Python-скрипт (см. CLAUDE.md).

**Tech Stack:** Статический HTML/CSS/JS, Python 3 для скриптов, Tilda CSS-фреймворк.

**Верификация:** `python3 -m http.server 8888` для локального просмотра, Google Rich Results Test для structured data, PageSpeed Insights для производительности.

---

## Фаза 1: SEO-фундамент

### Task 1: Добавить canonical и Twitter Card мета-теги

**Files:**
- Modify: `home.html` (head section, строка ~1)

**Step 1: Добавить canonical тег**

Найти закрывающий `</title>` в head и после него добавить:
```html
<link rel="canonical" href="https://curtainsfactory.ae/" />
```

**Step 2: Добавить Twitter Card мета-теги**

После блока Open Graph тегов добавить:
```html
<meta name="twitter:card" content="summary_large_image" />
<meta name="twitter:title" content="Шторы на заказ в Дубае | Curtains World" />
<meta name="twitter:description" content="Шторы и занавески на заказ в Дубае из натуральных тканей — лён и хлопок. Бесплатный замер, установка и карниз. Пошив за 4-5 дней." />
<meta name="twitter:image" content="https://curtainsfactory.ae/assets/_2024-02-07_14131410.png" />
```

**Step 3: Верификация**

Открыть `home.html` в браузере, View Source, убедиться что теги присутствуют в head.

**Step 4: Commit**
```bash
git add home.html
git commit -m "feat(seo): add canonical and Twitter Card meta tags"
```

---

### Task 2: Расширить robots.txt

**Files:**
- Modify: `robots.txt`

**Step 1: Обновить robots.txt**

Заменить содержимое на:
```
User-agent: *
Allow: /
Disallow: /assets/js/
Disallow: /assets/css/
Disallow: /*.json$

Sitemap: https://curtainsfactory.ae/sitemap.xml

# Curtains World — шторы на заказ в Дубае
```

**Step 2: Commit**
```bash
git add robots.txt
git commit -m "feat(seo): expand robots.txt with disallow rules and absolute sitemap URL"
```

---

### Task 3: Добавить семантические заголовки H1-H3

**Files:**
- Modify: `home.html`

**Контекст:** Tilda использует `<div class="t030__title t-title">` вместо `<h1>`. Нужно обернуть ключевые заголовки в семантические теги.

**Step 1: Добавить H1 в hero-секцию**

Найти главный заголовок "Шторы на заказ в Дубае" (в блоке T030 или T396 hero) и обернуть в `<h1>`:
```html
<h1 style="margin:0;padding:0;font:inherit;color:inherit;">Шторы на заказ в Дубае</h1>
```
Стиль `font:inherit;color:inherit;` обеспечивает совместимость с Tilda-дизайном.

**Step 2: Добавить H2 для секций**

Обернуть заголовки секций в `<h2>`:
- "Как мы работаем"
- "Забронировать бесплатный выезд"
- Любые другие заголовки секций

Формат: `<h2 style="margin:0;padding:0;font:inherit;color:inherit;">Текст</h2>`

**Step 3: Верификация**

```bash
python3 -c "
import re
html = open('home.html').read()
for tag in ['h1', 'h2', 'h3']:
    count = len(re.findall(f'<{tag}[ >]', html))
    print(f'{tag}: {count} found')
"
```
Ожидаем: h1: 1, h2: 2+

**Step 4: Commit**
```bash
git add home.html
git commit -m "feat(seo): add semantic h1/h2 heading tags"
```

---

### Task 4: Добавить alt-тексты ко всем изображениям

**Files:**
- Modify: `home.html`

**Контекст:** Большинство изображений используют `data-original` и имеют пустой `alt=""`. У некоторых div'ов с `role="img"` уже есть `aria-label`.

**Step 1: Составить список изображений без alt**

```bash
python3 -c "
from bs4 import BeautifulSoup
html = open('home.html').read()
soup = BeautifulSoup(html, 'html.parser')
for img in soup.find_all(['img', 'div']):
    if img.name == 'img':
        src = img.get('data-original') or img.get('src', '')
        alt = img.get('alt', 'MISSING')
        if 'assets/' in src and (alt == '' or alt == 'MISSING'):
            print(f'IMG: {src} | alt=\"{alt}\"')
    elif img.get('role') == 'img':
        label = img.get('aria-label', 'MISSING')
        bg = img.get('data-original', '')
        if label == 'MISSING':
            print(f'DIV: {bg} | aria-label MISSING')
"
```

**Step 2: Добавить описательные alt-тексты**

Примеры alt-текстов по файлам:
- `Mask_group.png` → "Шторы на заказ в интерьере — Curtains World Дубай"
- `_2024-02-07_14005275.png` → "Блэкаут шторы в спальне — затемняющие занавески Дубай"
- `_2024-02-07_14011771.png` → "Тюль на заказ — лёгкие занавески для гостиной Дубай"
- `_2024-02-07_14131410.png` → "Интерьер со шторами Curtains World — шторы на заказ ОАЭ"
- `_2024-02-03_14015764.png` → "Рулонные шторы — жалюзи на заказ в Дубае"
- `WhatsApp_logo-color-.png` → "WhatsApp" (декоративная иконка)

Использовать Python-скрипт для замены (строки слишком длинные для Edit):
```bash
python3 -c "
p='home.html'
c=open(p).read()
replacements = {
    'alt=\"\"': 'alt=\"описание\"'  # для каждого конкретного изображения
}
# Конкретные замены для каждого изображения
open(p,'w').write(c)
"
```

**Step 3: Верификация**

```bash
python3 -c "
from bs4 import BeautifulSoup
html = open('home.html').read()
soup = BeautifulSoup(html, 'html.parser')
empty = sum(1 for img in soup.find_all('img') if img.get('alt') == '' and 'assets/' in (img.get('src','') + img.get('data-original','')))
print(f'Images with empty alt: {empty}')
"
```
Ожидаем: 0 (или минимум для декоративных элементов)

**Step 4: Commit**
```bash
git add home.html
git commit -m "feat(seo): add descriptive alt texts to all images"
```

---

### Task 5: Расширить structured data (Product, BreadcrumbList)

**Files:**
- Modify: `home.html` (JSON-LD в head)

**Step 1: Добавить Product schema**

После существующего FAQPage JSON-LD добавить:
```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "ItemList",
  "name": "Шторы на заказ в Дубае",
  "itemListElement": [
    {
      "@type": "ListItem",
      "position": 1,
      "item": {
        "@type": "Product",
        "name": "Тюль на заказ",
        "description": "Тюль из натуральных тканей — лён и хлопок. Пошив за 4-5 дней.",
        "brand": {"@type": "Brand", "name": "Curtains World"},
        "offers": {
          "@type": "AggregateOffer",
          "priceCurrency": "AED",
          "lowPrice": "150",
          "highPrice": "800",
          "offerCount": "50"
        }
      }
    },
    {
      "@type": "ListItem",
      "position": 2,
      "item": {
        "@type": "Product",
        "name": "Блэкаут шторы",
        "description": "Затемняющие шторы для спальни. Полная блокировка света.",
        "brand": {"@type": "Brand", "name": "Curtains World"},
        "offers": {
          "@type": "AggregateOffer",
          "priceCurrency": "AED",
          "lowPrice": "200",
          "highPrice": "1200",
          "offerCount": "40"
        }
      }
    },
    {
      "@type": "ListItem",
      "position": 3,
      "item": {
        "@type": "Product",
        "name": "Моторизированные шторы",
        "description": "Шторы с электроприводом. Управление с пульта или смартфона.",
        "brand": {"@type": "Brand", "name": "Curtains World"},
        "offers": {
          "@type": "AggregateOffer",
          "priceCurrency": "AED",
          "lowPrice": "500",
          "highPrice": "3000",
          "offerCount": "20"
        }
      }
    },
    {
      "@type": "ListItem",
      "position": 4,
      "item": {
        "@type": "Product",
        "name": "Жалюзи",
        "description": "Жалюзи на заказ — вертикальные и горизонтальные.",
        "brand": {"@type": "Brand", "name": "Curtains World"},
        "offers": {
          "@type": "AggregateOffer",
          "priceCurrency": "AED",
          "lowPrice": "100",
          "highPrice": "600",
          "offerCount": "30"
        }
      }
    }
  ]
}
</script>
```

**Step 2: Добавить BreadcrumbList schema**

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    {"@type": "ListItem", "position": 1, "name": "Главная", "item": "https://curtainsfactory.ae/"}
  ]
}
</script>
```

**Step 3: Верификация**

Скопировать JSON-LD и проверить на https://validator.schema.org/ или https://search.google.com/test/rich-results

**Step 4: Commit**
```bash
git add home.html
git commit -m "feat(seo): add Product ItemList and BreadcrumbList structured data"
```

---

### Task 6: Обновить sitemap.xml

**Files:**
- Modify: `sitemap.xml`

**Step 1: Расширить sitemap**

```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
        xmlns:image="http://www.google.com/schemas/sitemap-image/1.1"
        xmlns:xhtml="http://www.w3.org/1999/xhtml">
  <url>
    <loc>https://curtainsfactory.ae/</loc>
    <xhtml:link rel="alternate" hreflang="ru" href="https://curtainsfactory.ae/" />
    <xhtml:link rel="alternate" hreflang="en" href="https://curtainsfactory.ae/en/" />
    <lastmod>2026-02-24</lastmod>
    <changefreq>weekly</changefreq>
    <priority>1.0</priority>
    <image:image>
      <image:loc>https://curtainsfactory.ae/assets/Mask_group.png</image:loc>
      <image:title>Шторы на заказ в Дубае — Curtains World</image:title>
    </image:image>
  </url>
</urlset>
```

Примечание: по мере добавления посадочных страниц (Фаза 4) обновлять sitemap.

**Step 2: Commit**
```bash
git add sitemap.xml
git commit -m "feat(seo): expand sitemap with image and hreflang annotations"
```

---

## Фаза 2: Конверсионные правки

### Task 7: Добавить sticky WhatsApp-кнопку для мобильных

**Files:**
- Modify: `home.html` (добавить перед `</body>`)

**Step 1: Добавить CSS + HTML для sticky кнопки**

Перед закрывающим `</body>` добавить:
```html
<style>
.wa-float{position:fixed;bottom:20px;right:20px;z-index:9999;width:60px;height:60px;border-radius:50%;background:#25D366;display:flex;align-items:center;justify-content:center;box-shadow:0 4px 12px rgba(0,0,0,.25);cursor:pointer;transition:transform .2s}
.wa-float:hover{transform:scale(1.1)}
.wa-float svg{width:32px;height:32px;fill:#fff}
@media(min-width:960px){.wa-float{bottom:30px;right:30px}}
</style>
<a href="https://wa.me/971589408100?text=%D0%97%D0%B4%D1%80%D0%B0%D0%B2%D1%81%D1%82%D0%B2%D1%83%D0%B9%D1%82%D0%B5!%20%D0%A5%D0%BE%D1%87%D1%83%20%D1%83%D0%B7%D0%BD%D0%B0%D1%82%D1%8C%20%D0%BF%D1%80%D0%BE%20%D1%88%D1%82%D0%BE%D1%80%D1%8B" target="_blank" rel="noopener" class="wa-float" aria-label="Написать в WhatsApp">
<svg viewBox="0 0 24 24"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z"/></svg>
</a>
```

URL содержит предзаполненное сообщение: "Здравствуйте! Хочу узнать про шторы"

**Step 2: Верификация**

```bash
python3 -m http.server 8888
```
Открыть http://localhost:8888/home.html на мобильном (или DevTools responsive mode). Убедиться:
- Кнопка видна в правом нижнем углу
- Клик ведёт в WhatsApp

**Step 3: Commit**
```bash
git add home.html
git commit -m "feat(ux): add sticky WhatsApp button for mobile and desktop"
```

---

### Task 8: Добавить click-to-call для телефона

**Files:**
- Modify: `home.html`

**Step 1: Найти все номера телефонов на странице**

```bash
python3 -c "
html = open('home.html').read()
import re
phones = re.findall(r'\+971[\s\-]?\d{2}[\s\-]?\d{3}[\s\-]?\d{4}', html)
print(f'Found {len(phones)} phone numbers')
for p in set(phones):
    print(f'  {p}')
"
```

**Step 2: Обернуть номера в `<a href="tel:">`**

Для каждого найденного номера, если он ещё не обёрнут в ссылку:
```html
<a href="tel:+971589408100" style="color:inherit;text-decoration:none;">+971 58 940 8100</a>
```

**Step 3: Верификация**

Открыть в мобильном браузере, убедиться что клик по номеру открывает дайлер.

**Step 4: Commit**
```bash
git add home.html
git commit -m "feat(ux): wrap phone numbers with click-to-call tel: links"
```

---

### Task 9: Улучшить микрокопирайтинг CTA-кнопок

**Files:**
- Modify: `home.html`

**Step 1: Найти все CTA-кнопки**

```bash
python3 -c "
from bs4 import BeautifulSoup
html = open('home.html').read()
soup = BeautifulSoup(html, 'html.parser')
for btn in soup.find_all(['button', 'a'], class_=lambda c: c and ('t-btn' in c or 't-submit' in c)):
    print(f'{btn.name}: \"{btn.get_text(strip=True)}\" | class={btn.get(\"class\")}')
"
```

**Step 2: Обновить тексты кнопок**

Замены:
- "ЗАБРОНИРОВАТЬ ВСТРЕЧУ" → "ЗАПИСАТЬСЯ НА БЕСПЛАТНЫЙ ЗАМЕР"
- "ЗАПИСАТЬСЯ НА ВИЗИТ" (меню) → "БЕСПЛАТНЫЙ ЗАМЕР"
- Добавить подтекст под форму: "Перезвоним в течение 15 минут"

**Step 3: Верификация**

Открыть `home.html`, проверить визуально что кнопки отображаются корректно.

**Step 4: Commit**
```bash
git add home.html
git commit -m "feat(ux): improve CTA button copy for better conversion"
```

---

## Фаза 3: Оптимизация изображений

### Task 10: Создать скрипт конвертации изображений в WebP

**Files:**
- Create: `optimize_images.py`

**Step 1: Написать скрипт**

```python
#!/usr/bin/env python3
"""Convert PNG/JPG images to WebP format with compression."""
import os
import subprocess
import json

ASSETS_DIR = "assets/images" if os.path.isdir("assets/images") else "assets"
QUALITY = 80

def get_image_files(directory):
    """Find all PNG and JPG files."""
    images = []
    for f in os.listdir(directory):
        if f.lower().endswith(('.png', '.jpg', '.jpeg')) and not f.startswith('.'):
            images.append(os.path.join(directory, f))
    return images

def convert_to_webp(filepath, quality=QUALITY):
    """Convert image to WebP using cwebp or Pillow."""
    webp_path = os.path.splitext(filepath)[0] + '.webp'
    if os.path.exists(webp_path):
        return webp_path

    try:
        from PIL import Image
        img = Image.open(filepath)
        img.save(webp_path, 'WebP', quality=quality)
        original_size = os.path.getsize(filepath)
        webp_size = os.path.getsize(webp_path)
        savings = (1 - webp_size / original_size) * 100
        print(f"  {os.path.basename(filepath)}: {original_size//1024}KB → {webp_size//1024}KB ({savings:.0f}% saved)")
        return webp_path
    except ImportError:
        print("Install Pillow: pip3 install Pillow")
        return None

if __name__ == "__main__":
    images = get_image_files(ASSETS_DIR)
    print(f"Found {len(images)} images to convert")
    total_saved = 0
    for img in sorted(images):
        result = convert_to_webp(img)
    print(f"\nDone! WebP versions created alongside originals.")
```

**Step 2: Установить Pillow и запустить**

```bash
pip3 install Pillow
python3 optimize_images.py
```

**Step 3: Верификация**

Проверить что WebP-файлы созданы и меньше оригиналов:
```bash
ls -la assets/*.webp 2>/dev/null | head -10
```

**Step 4: Commit**
```bash
git add optimize_images.py
git commit -m "feat: add image optimization script (PNG/JPG to WebP)"
```

---

### Task 11: Обновить HTML для использования `<picture>` с WebP

**Files:**
- Modify: `home.html`

**Step 1: Создать скрипт для замены img на picture**

```python
#!/usr/bin/env python3
"""Replace img tags with picture elements for WebP support."""
import re
import os

def add_webp_support(html_path):
    html = open(html_path).read()

    # Find img tags with local assets
    def replace_img(match):
        full_tag = match.group(0)
        src_match = re.search(r'(src|data-original)="(assets/[^"]+\.(png|jpg|jpeg))"', full_tag)
        if not src_match:
            return full_tag

        attr = src_match.group(1)
        src = src_match.group(2)
        webp_src = re.sub(r'\.(png|jpg|jpeg)$', '.webp', src)

        if not os.path.exists(webp_src):
            return full_tag

        # Don't wrap if already in a picture tag
        return full_tag  # Simplified: just update data-original to include webp hint

    # For Tilda's lazy-loading system, add data-webp attribute
    count = 0
    for ext in ['png', 'jpg', 'jpeg']:
        pattern = f'data-original="(assets/[^"]+\\.{ext})"'
        for match in re.finditer(pattern, html):
            src = match.group(1)
            webp = re.sub(f'\\.{ext}$', '.webp', src)
            if os.path.exists(webp):
                count += 1

    print(f"Found {count} images with WebP alternatives available")
    print("Note: Tilda's lazy-loading handles format selection via JS")

if __name__ == "__main__":
    add_webp_support("home.html")
```

Примечание: Tilda использует собственный lazy-loading (tilda-lazyload). Для полной поддержки WebP нужно либо модифицировать JS загрузчик, либо заменить `data-original` пути на .webp напрямую (с PNG fallback через `<noscript>`).

**Step 2: Простая замена — обновить пути на WebP**

Для изображений где WebP существует, заменить расширение:
```bash
python3 -c "
import os, re
p = 'home.html'
c = open(p).read()
count = 0
for ext in ['png', 'jpg', 'jpeg']:
    for m in re.finditer(f'(assets/[^\"\\'\\s]+\\.{ext})', c):
        src = m.group(1)
        webp = re.sub(f'\\.{ext}$', '.webp', src)
        if os.path.exists(webp):
            c = c.replace(src, webp, 1)
            count += 1
open(p, 'w').write(c)
print(f'Replaced {count} image paths with WebP versions')
"
```

**Step 3: Верификация**

```bash
python3 -m http.server 8888
```
Открыть http://localhost:8888/home.html — все изображения должны загружаться.

**Step 4: Commit**
```bash
git add home.html
git commit -m "feat(perf): switch images to WebP format"
```

---

## Фаза 4: Контентное расширение

### Task 12: Создать шаблон посадочной страницы

**Files:**
- Create: `template-landing.html`

**Step 1: Создать шаблон**

Извлечь из `home.html` общие элементы: head (мета, стили, скрипты), навигацию, footer, формы. Создать шаблон с плейсхолдерами:
- `{{PAGE_TITLE}}` — title и H1
- `{{META_DESCRIPTION}}` — мета-описание
- `{{META_KEYWORDS}}` — ключевые слова
- `{{CANONICAL_URL}}` — canonical
- `{{HERO_TITLE}}` — заголовок hero
- `{{HERO_SUBTITLE}}` — подзаголовок
- `{{CONTENT}}` — основной контент
- `{{FAQ_ITEMS}}` — FAQ блок

**Step 2: Создать Python-скрипт генерации страниц**

```python
#!/usr/bin/env python3
"""Generate landing pages from template."""
import json

PAGES = [
    {
        "slug": "blackout-shtory-dubai",
        "title": "Блэкаут шторы на заказ в Дубае | Curtains World",
        "h1": "Блэкаут шторы на заказ в Дубае",
        "description": "Блэкаут шторы в Дубае — полная блокировка света. Натуральные ткани, пошив за 4-5 дней. Бесплатный замер и установка.",
        "keywords": "блэкаут шторы дубай, затемняющие шторы дубай, blackout curtains dubai",
    },
    {
        "slug": "tyul-na-zakaz-dubai",
        "title": "Тюль на заказ в Дубае | Curtains World",
        "h1": "Тюль на заказ в Дубае",
        "description": "Тюль на заказ в Дубае из натуральных тканей — лён и хлопок. Бесплатный замер, установка. Пошив за 4-5 дней.",
        "keywords": "тюль дубай, тюль на заказ дубай, sheer curtains dubai",
    },
    {
        "slug": "motorizirovannye-shtory-dubai",
        "title": "Моторизированные шторы в Дубае | Curtains World",
        "h1": "Моторизированные шторы в Дубае",
        "description": "Электрические шторы с управлением с пульта и смартфона. Установка в Дубае. Бесплатный замер.",
        "keywords": "моторизированные шторы дубай, электрические шторы дубай, motorized curtains dubai",
    },
    {
        "slug": "zhalyuzi-dubai",
        "title": "Жалюзи на заказ в Дубае | Curtains World",
        "h1": "Жалюзи на заказ в Дубае",
        "description": "Жалюзи на заказ в Дубае — вертикальные, горизонтальные, рулонные. Замер и установка бесплатно.",
        "keywords": "жалюзи дубай, жалюзи на заказ дубай, blinds dubai",
    },
    {
        "slug": "karnizy-dubai",
        "title": "Карнизы в Дубае | Curtains World",
        "h1": "Карнизы в Дубае",
        "description": "Карнизы для штор в Дубае — потолочные, настенные, электрические. Установка бесплатно.",
        "keywords": "карнизы дубай, карнизы для штор дубай, curtain rods dubai",
    },
]
```

**Step 3: Генерировать страницы**

Скрипт создаёт HTML-файлы `{slug}.html` из шаблона.

**Step 4: Верификация**

Открыть каждую страницу в браузере, проверить мета-теги через View Source.

**Step 5: Commit**
```bash
git add template-landing.html generate_pages.py *.html
git commit -m "feat: add landing page template and generator for product pages"
```

---

### Task 13: Обновить навигацию и внутреннюю перелинковку

**Files:**
- Modify: `home.html` и все посадочные страницы

**Step 1: Обновить меню навигации**

Заменить существующие пункты меню на локальные ссылки:
- "Блэкаут" → `/blackout-shtory-dubai.html`
- "Тюль" → `/tyul-na-zakaz-dubai.html`
- Добавить: "Моторизированные" → `/motorizirovannye-shtory-dubai.html`
- Добавить: "Жалюзи" → `/zhalyuzi-dubai.html`
- Добавить: "Карнизы" → `/karnizy-dubai.html`

Убрать `target="_blank"` для внутренних ссылок.

**Step 2: Добавить breadcrumb HTML**

На каждой посадочной странице:
```html
<nav aria-label="Breadcrumb" style="padding:10px 20px;font-size:14px;color:#666;">
  <a href="/" style="color:#7a8d7e;">Главная</a> → <span>Блэкаут шторы</span>
</nav>
```

**Step 3: Обновить sitemap.xml**

Добавить все новые страницы в sitemap.

**Step 4: Commit**
```bash
git add home.html sitemap.xml *.html
git commit -m "feat: update navigation with product page links and breadcrumbs"
```

---

### Task 14: Расширить FAQ

**Files:**
- Modify: `home.html` (существующий FAQ блок)
- Modify: каждая посадочная страница

**Step 1: Расширить FAQ на главной**

Добавить вопросы в существующий FAQPage JSON-LD и видимый HTML:
- "Из каких тканей шьёте шторы?" → "Мы используем натуральные ткани: лён, хлопок, бархат. Также доступны смесовые и синтетические варианты."
- "Работаете ли вы по всему Дубаю?" → "Да, бесплатный выезд на замер по всему Дубаю и пригородам."
- "Можно ли увидеть образцы тканей?" → "Да, мастер привозит каталог с образцами на бесплатный замер."

**Step 2: Добавить специфичные FAQ на посадочные**

Для каждой посадочной — 3-4 FAQ по теме + FAQPage schema.

**Step 3: Commit**
```bash
git add home.html *.html
git commit -m "feat(seo): expand FAQ content and add page-specific FAQs"
```

---

## Фаза 5: Техническая оптимизация

### Task 15: Аудит и удаление неиспользуемого JS

**Files:**
- Modify: `home.html`

**Step 1: Определить используемые модули**

```bash
python3 -c "
from bs4 import BeautifulSoup
html = open('home.html').read()
soup = BeautifulSoup(html, 'html.parser')
for script in soup.find_all('script', src=True):
    src = script['src']
    if 'assets/' in src:
        print(src)
"
```

**Step 2: Проверить какие модули реально используются**

Список модулей Tilda и их назначение:
- `tilda-scripts-3.0.min.js` — НУЖЕН (ядро)
- `jquery-1.10.2.min.js` — НУЖЕН (зависимость Tilda)
- `tilda-lazyload-1.0.min.js` — НУЖЕН (lazy-loading)
- `tilda-forms-1.0.min.js` — НУЖЕН (формы)
- `tilda-zero-1.1.min.js` — НУЖЕН (базовые утилиты)
- `tilda-animation-2.0.min.js` — ОПЦИОНАЛЬНО (анимации при скролле)
- `tilda-catalog-1.1.min.js` — ПРОВЕРИТЬ (233KB! нужен ли каталог?)
- `tilda-polyfill-1.0.min.js` — ПРОВЕРИТЬ (181KB, для старых браузеров)
- `tilda-date-picker-1.0.min.js` — НУЖЕН (выбор даты в форме)
- `tilda-zoom-2.0.min.js` — ПРОВЕРИТЬ (зум изображений)

**Step 3: Удалить ненужные скрипты**

Закомментировать или удалить `<script>` теги для модулей, которые не используются. Начать с `tilda-polyfill` (181KB) — если поддержка IE не нужна.

**Step 4: Верификация**

Протестировать сайт после удаления каждого модуля — все функции должны работать.

**Step 5: Commit**
```bash
git add home.html
git commit -m "perf: remove unused Tilda JS modules (~400KB savings)"
```

---

### Task 16: Оптимизировать шрифты

**Files:**
- Modify: `assets/css/fonts.css`
- Possibly delete unused font files

**Step 1: Определить используемые начертания**

```bash
python3 -c "
import re
html = open('home.html').read()
weights = set(re.findall(r'font-weight:\s*(\d+)', html))
families = set(re.findall(r'font-family:\s*[\"\\']?([^\"\\';,]+)', html))
print(f'Font families: {families}')
print(f'Font weights: {weights}')
"
```

**Step 2: Удалить неиспользуемые @font-face из fonts.css**

Оставить только те начертания, которые реально используются в CSS/HTML.

**Step 3: Удалить неиспользуемые файлы шрифтов из assets/fonts/**

**Step 4: Commit**
```bash
git add assets/css/fonts.css
git commit -m "perf: remove unused font weights (29 files → ~10)"
```

---

### Task 17: Добавить Web Vitals мониторинг

**Files:**
- Modify: `home.html` (перед `</body>`)

**Step 1: Добавить inline-скрипт Web Vitals**

```html
<script>
// Web Vitals reporting via GTM
if ('PerformanceObserver' in window) {
  function sendToGTM(name, value) {
    if (window.dataLayer) {
      window.dataLayer.push({event: 'web_vitals', metric_name: name, metric_value: Math.round(value)});
    }
  }
  // LCP
  new PerformanceObserver(function(list) {
    var entries = list.getEntries();
    var last = entries[entries.length - 1];
    sendToGTM('LCP', last.startTime);
  }).observe({type: 'largest-contentful-paint', buffered: true});
  // CLS
  var clsValue = 0;
  new PerformanceObserver(function(list) {
    for (var entry of list.getEntries()) {
      if (!entry.hadRecentInput) clsValue += entry.value;
    }
    sendToGTM('CLS', clsValue * 1000);
  }).observe({type: 'layout-shift', buffered: true});
}
</script>
```

**Step 2: Верификация**

Открыть DevTools → Console, проверить что `dataLayer` содержит события `web_vitals`.

**Step 3: Commit**
```bash
git add home.html
git commit -m "feat: add Web Vitals monitoring via GTM dataLayer"
```

---

## Порядок выполнения

| Task | Фаза | Описание | Зависимости |
|------|-------|----------|-------------|
| 1 | SEO | Canonical + Twitter Cards | — |
| 2 | SEO | robots.txt | — |
| 3 | SEO | Семантические заголовки H1-H3 | — |
| 4 | SEO | Alt-тексты изображений | — |
| 5 | SEO | Structured Data (Product, Breadcrumb) | — |
| 6 | SEO | Обновить sitemap.xml | — |
| 7 | UX | Sticky WhatsApp кнопка | — |
| 8 | UX | Click-to-call телефоны | — |
| 9 | UX | Микрокопирайтинг CTA | — |
| 10 | Perf | Скрипт конвертации WebP | — |
| 11 | Perf | Обновить HTML для WebP | Task 10 |
| 12 | Content | Шаблон посадочной + генератор | Tasks 1-6 |
| 13 | Content | Навигация + перелинковка | Task 12 |
| 14 | Content | Расширение FAQ | Task 12 |
| 15 | Tech | Аудит/удаление JS | — |
| 16 | Tech | Оптимизация шрифтов | — |
| 17 | Tech | Web Vitals мониторинг | — |

**Tasks 1-9, 10, 15-17 можно выполнять параллельно** (нет взаимозависимостей).
**Tasks 11 зависит от 10**, **Tasks 12-14 зависят от фазы 1** (для корректных мета-тегов в шаблоне).
