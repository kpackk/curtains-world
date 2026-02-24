import requests
import re
import os

font_css_url = "https://fonts.googleapis.com/css2?family=Ubuntu:wght@300;400;500;600;700&family=Montserrat:wght@100..900&subset=latin,cyrillic"
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

print(f"Fetching CSS from {font_css_url}...")
r = requests.get(font_css_url, headers=headers)
css_content = r.text

# Find all font URLs
# url(https://fonts.gstatic.com/s/ubuntu/v20/4iCv6KVjbNBYlgoCjC3jsGyN.woff2)
font_urls = re.findall(r'url\((https://[^)]+)\)', css_content)
unique_font_urls = list(set(font_urls))

print(f"Found {len(unique_font_urls)} font files.")

os.makedirs('assets/fonts', exist_ok=True)
os.makedirs('assets/css', exist_ok=True)

local_css_content = css_content

for url in unique_font_urls:
    filename = url.split('/')[-1]
    local_path = f'assets/fonts/{filename}'
    
    # Download font
    print(f"Downloading {filename}...")
    try:
        fr = requests.get(url, headers=headers)
        with open(local_path, 'wb') as f:
            f.write(fr.content)
            
        # Replace in CSS
        # We want relative path from assets/css/fonts.css to assets/fonts/filename
        # which is ../fonts/filename
        local_css_content = local_css_content.replace(url, f'../fonts/{filename}')
        
    except Exception as e:
        print(f"Failed to download {filename}: {e}")

# Save local CSS
with open('assets/css/fonts.css', 'w', encoding='utf-8') as f:
    f.write(local_css_content)

print("Created assets/css/fonts.css")
