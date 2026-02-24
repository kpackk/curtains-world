import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import mimetypes

BASE_URL = "https://curtainsfactory.ae/curtains-dubai-ru"
OUTPUT_FILE = "home-ru.html"
ASSETS_DIR = "assets"

def get_filename(url, content_type=None):
    parsed = urlparse(url)
    path = parsed.path
    filename = os.path.basename(path)
    
    if not filename or filename == 'css2': 
        # Handle cases like /css2 or empty filename
        if 'css2' in path:
            return "fonts.css"
        return "resource" 

    if '?' in filename:
        filename = filename.split('?')[0]
    
    # Add extension if missing and we know the content type
    if not os.path.splitext(filename)[1] and content_type:
        ext = mimetypes.guess_extension(content_type)
        if ext:
            filename += ext
    
    return filename

def download_file(url, local_path):
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        with open(local_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        return True
    except Exception as e:
        print(f"Failed to download {url}: {e}")
        return False

def main():
    if not os.path.exists(ASSETS_DIR):
        os.makedirs(ASSETS_DIR)

    print(f"Fetching {BASE_URL}...")
    try:
        response = requests.get(BASE_URL)
        response.raise_for_status()
    except Exception as e:
        print(f"Failed to fetch page: {e}")
        return

    soup = BeautifulSoup(response.content, 'html.parser')

    # Helper to process attributes
    def process_attribute(tag, attr):
        if not tag.has_attr(attr): return
        url = tag[attr]
        if not url: return

        full_url = urljoin(BASE_URL, url)
        
        # skip data URIs
        if full_url.startswith('data:'): return

        filename = get_filename(full_url)
        local_path = os.path.join(ASSETS_DIR, filename)
        
        # Download if not exists (or specific files)
        if not os.path.exists(local_path) or filename == "fonts.css":
            print(f"Downloading {filename} from {full_url}...")
            download_file(full_url, local_path)
        
        tag[attr] = f"{ASSETS_DIR}/{filename}"

    # 1. Scripts with src
    for tag in soup.find_all('script', src=True):
        process_attribute(tag, 'src')

    # 2. Images with src
    for tag in soup.find_all('img', src=True):
        process_attribute(tag, 'src')

    # 3. Images with data-original (Lazy loading) mechanism often used in Tilda
    # Also generic elements with data-original (backgrounds)
    for tag in soup.find_all(attrs={"data-original": True}):
        process_attribute(tag, 'data-original')

    # 4. Link stylesheets
    for tag in soup.find_all('link', rel='stylesheet', href=True):
        # Specific handling for google fonts css2
        url = tag['href']
        if 'css2' in url:
             # Force name for css2
             full_url = urljoin(BASE_URL, url)
             local_path = os.path.join(ASSETS_DIR, "fonts.css")
             print(f"Downloading fonts.css...")
             download_file(full_url, local_path)
             tag['href'] = f"{ASSETS_DIR}/fonts.css"
        else:
            process_attribute(tag, 'href')

    # 5. Icons
    for tag in soup.find_all('link', rel='shortcut icon', href=True):
        process_attribute(tag, 'href')

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(str(soup))
    
    print(f"Saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
