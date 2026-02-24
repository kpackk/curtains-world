import requests, re, os
from bs4 import BeautifulSoup

BASE_DIR = "/Users/rus/Desktop/FENESTRA/сайт 1 рус дубай"
ASSETS = os.path.join(BASE_DIR, "assets")
HTML_FILE = os.path.join(BASE_DIR, "home.html")

os.chdir(BASE_DIR)

print("Fetching original page...")
resp = requests.get("https://curtainsfactory.ae/curtains-dubai-ru", timeout=30)
html = resp.text
print("Page size:", len(html))

# Find all tildacdn URLs
all_cdn_urls = set()
for m in re.finditer(r'https://(?:static|thb|neo)\.tildacdn\.com/[^"\s<>)+;]+', html):
    url = m.group(0).rstrip("');,")
    all_cdn_urls.add(url)

print("Found", len(all_cdn_urls), "unique CDN URLs")

# Map URL -> (unique_local_name, download_url)
url_map = {}
for url in all_cdn_urls:
    if "thb.tildacdn.com" in url:
        m = re.match(r'https://thb\.tildacdn\.com/(tild[^/]+)/.*?/([^/]+)$', url)
        if m:
            hp, fn = m.group(1), m.group(2)
            ln = hp[4:12] + "_" + fn
            du = "https://static.tildacdn.com/" + hp + "/" + fn
            url_map[url] = (ln, du)
    elif "/css/" in url or "/js/" in url:
        fn = url.split("/")[-1].split("?")[0]
        url_map[url] = (fn, url)
    elif "/ws/" in url:
        fn = url.split("/")[-1].split("?")[0]
        url_map[url] = (fn, url)
    elif "static.tildacdn.com" in url:
        m = re.match(r'https://static\.tildacdn\.com/(tild[^/]+)/([^?]+)', url)
        if m:
            hp, fn = m.group(1), m.group(2)
            ln = hp[4:12] + "_" + fn
            url_map[url] = (ln, url)
    elif "neo.tildacdn.com" in url:
        fn = url.split("/")[-1].split("?")[0]
        url_map[url] = (fn, url)

print("Mapped", len(url_map), "URLs")

# Download all files
os.makedirs(ASSETS, exist_ok=True)
downloaded = 0
skipped = 0
failed = 0
for url, (ln, du) in url_map.items():
    lp = os.path.join(ASSETS, ln)
    if os.path.exists(lp) and os.path.getsize(lp) > 5000:
        skipped += 1
        continue
    try:
        r = requests.get(du, timeout=30)
        r.raise_for_status()
        with open(lp, "wb") as f:
            f.write(r.content)
        print("  Got:", ln, len(r.content) // 1024, "KB")
        downloaded += 1
    except Exception as e:
        print("  FAIL:", ln, str(e)[:80])
        failed += 1

print("Downloaded:", downloaded, "Skipped:", skipped, "Failed:", failed)

# Replace all CDN URLs in HTML with local paths
new_html = html
for url in sorted(url_map.keys(), key=len, reverse=True):
    ln = url_map[url][0]
    new_html = new_html.replace(url, "assets/" + ln)

# Replace Google Fonts CSS
new_html = re.sub(r'https://fonts\.googleapis\.com/css2[^"\s]+', "assets/fonts.css", new_html)

# Fix lazy loading - set full images directly
soup = BeautifulSoup(new_html, "html.parser")
fixed = 0
for tag in soup.find_all(attrs={"data-original": True}):
    do_val = tag.get("data-original", "")
    st = tag.get("style", "")
    if not do_val:
        continue
    if tag.name == "img":
        tag["src"] = do_val
        fixed += 1
    if "background-image" in st:
        ns = re.sub(r'background-image:\s*url\([^)]+\)', "background-image:url(" + do_val + ")", st)
        tag["style"] = ns
        fixed += 1
    elif tag.name == "div":
        es = tag.get("style", "")
        tag["style"] = "background-image:url(" + do_val + "); background-size:cover; background-position:center; " + es
        fixed += 1

print("Fixed", fixed, "lazy elements")

with open(HTML_FILE, "w", encoding="utf-8") as f:
    f.write(str(soup))

print("Done! Saved", HTML_FILE)
