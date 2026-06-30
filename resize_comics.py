#!/usr/bin/env python3
"""Batch resize comic images for web optimization."""
import os
from pathlib import Path
from PIL import Image

COMIC_DIR = Path("/home/admin/mks-knowledge/comic")
EPISODES = range(1, 9)  # ep1 through ep8
PANELS_PER_EP = 12
WEB_WIDTH = 800
COVER_WIDTH = 300
JPEG_QUALITY = 85

def resize_image(src_path, dst_path, width, quality=JPEG_QUALITY):
    """Resize image to given width, maintaining aspect ratio, save as JPEG."""
    img = Image.open(src_path)
    if img.mode in ('RGBA', 'P', 'LA'):
        img = img.convert('RGB')
    w_percent = width / float(img.size[0])
    h_size = int(float(img.size[1]) * w_percent)
    img = img.resize((width, h_size), Image.LANCZOS)
    img.save(dst_path, 'JPEG', quality=quality)
    orig_size = os.path.getsize(src_path)
    new_size = os.path.getsize(dst_path)
    print(f"  {dst_path.name}: {orig_size//1024}KB -> {new_size//1024}KB "
          f"({img.size[0]}x{img.size[1]})")
    return new_size

def main():
    total_saved = 0
    total_orig = 0

    for ep_num in EPISODES:
        ep_dir = COMIC_DIR / f"ep{ep_num}"
        print(f"\n=== Episode {ep_num} ===")

        # Resize all 12 panels to 800px wide
        for panel in range(1, PANELS_PER_EP + 1):
            src = ep_dir / f"ep{ep_num}-{panel:02d}.jpeg"
            dst = ep_dir / f"ep{ep_num}-{panel:02d}.jpg"
            if src.exists():
                new_size = resize_image(src, dst, WEB_WIDTH)
                total_orig += os.path.getsize(src)
                total_saved += new_size

        # Create cover thumbnail (use panel 01 as the cover image)
        cover_src = ep_dir / f"ep{ep_num}-01.jpeg"
        cover_dst = ep_dir / f"ep{ep_num}-cover.jpg"
        if cover_src.exists():
            cover_size = resize_image(cover_src, cover_dst, COVER_WIDTH)
            total_orig += os.path.getsize(cover_src)
            total_saved += cover_size

        # Count .jpg files created
        jpgs = sorted(ep_dir.glob("*.jpg"))
        print(f"  Created {len(jpgs)} .jpg files in ep{ep_num}/")

    print(f"\n=== Summary ===")
    print(f"Original total: {total_orig//1024}KB ({total_orig/1024/1024:.1f}MB)")
    print(f"Resized total:  {total_saved//1024}KB ({total_saved/1024/1024:.1f}MB)")
    print(f"Reduction:      {(1 - total_saved/total_orig)*100:.0f}%")
    print("Done!")

if __name__ == "__main__":
    main()
