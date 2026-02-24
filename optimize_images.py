#!/usr/bin/env python3
"""Convert PNG/JPG images to WebP format with compression."""
import os
import sys

QUALITY = 80

def get_image_files(directory):
    """Find all PNG and JPG files recursively."""
    images = []
    for root, dirs, files in os.walk(directory):
        for f in files:
            if f.lower().endswith(('.png', '.jpg', '.jpeg')) and not f.startswith('.'):
                images.append(os.path.join(root, f))
    return images

def convert_to_webp(filepath, quality=QUALITY):
    """Convert image to WebP using Pillow."""
    webp_path = os.path.splitext(filepath)[0] + '.webp'
    if os.path.exists(webp_path):
        print(f"  SKIP {os.path.basename(filepath)} (WebP already exists)")
        return 0

    try:
        from PIL import Image
        img = Image.open(filepath)
        if img.mode in ('RGBA', 'LA', 'P'):
            img = img.convert('RGBA')
        else:
            img = img.convert('RGB')
        img.save(webp_path, 'WebP', quality=quality)
        original_size = os.path.getsize(filepath)
        webp_size = os.path.getsize(webp_path)
        savings = original_size - webp_size
        pct = (savings / original_size) * 100 if original_size > 0 else 0
        print(f"  {os.path.basename(filepath)}: {original_size//1024}KB -> {webp_size//1024}KB ({pct:.0f}% saved)")
        return savings
    except ImportError:
        print("ERROR: Pillow not installed. Run: pip3 install Pillow")
        sys.exit(1)
    except Exception as e:
        print(f"  ERROR {os.path.basename(filepath)}: {e}")
        return 0

if __name__ == "__main__":
    assets_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")
    images = get_image_files(assets_dir)
    print(f"Found {len(images)} images to convert\n")

    total_saved = 0
    for img in sorted(images):
        total_saved += convert_to_webp(img)

    print(f"\nTotal saved: {total_saved // 1024}KB ({total_saved // (1024*1024)}MB)")
    print("WebP versions created alongside originals.")
