from PIL import Image, ImageEnhance
import os, math

img_dir = "/root/nobleparc/nobleparc/static/images"
os.makedirs(img_dir, exist_ok=True)

selections = [
    ("mask",    "mask-product-3.jpg",    "mask-hero"),
    ("mask",    "mask-product-8.jpg",    "mask-lifestyle"),
    ("massager","massager-product-2.jpg","massager-hero"),
    ("massager","massager-product-4.jpg","massager-angle"),
]

def warm_tone(img, warmth=0.15, bright=1.08, contrast=1.05):
    if img.mode != 'RGB':
        img = img.convert('RGB')
    img = ImageEnhance.Brightness(img).enhance(bright)
    img = ImageEnhance.Contrast(img).enhance(contrast)
    px = img.load()
    w, h = img.size
    for x in range(w):
        for y in range(h):
            r, g, b = px[x, y]
            r = min(255, int(r * (1 + warmth)))
            g = min(255, int(g * (1 + warmth * 0.4)))
            b = max(0, int(b * (1 - warmth * 0.3)))
            px[x, y] = (r, g, b)
    return img

def warm_vignette(img, strength=0.35):
    w, h = img.size
    cx, cy = w // 2, h // 2
    max_dist = math.sqrt(cx**2 + cy**2)
    px = img.load()
    for x in range(w):
        for y in range(h):
            d = math.sqrt((x - cx)**2 + (y - cy)**2) / max_dist
            f = d * strength
            r, g, b = px[x, y]
            px[x, y] = (min(255, int(r + f*35)), min(255, int(g + f*15)), max(0, int(b - f*15)))
    return img

def crop_square(img):
    s = min(img.size)
    l = (img.width - s) // 2
    t = (img.height - s) // 2
    return img.crop((l, t, l+s, t+s))

print("=" * 60)
print("WARM TONE CORRECTION + MULTI-RES EXPORT")
print("=" * 60)

for prod, src, base in selections:
    path = os.path.join(img_dir, src)
    print(f"\n>>> {prod.upper()}: {src} -> {base}")
    
    with Image.open(path) as img:
        orig_kb = os.path.getsize(path) / 1024
        print(f"  Original: {img.size[0]}x{img.size[1]}px {orig_kb:.0f}KB")
        
        # Warm correction
        img = warm_tone(img, warmth=0.15, bright=1.08, contrast=1.05)
        img = warm_vignette(img, strength=0.35)
        
        # Export at 3 widths
        for w in [480, 768, 1200]:
            sq = crop_square(img)
            sq = sq.resize((w, w), Image.LANCZOS)
            fname = f"{base}-{w}w.webp"
            fpath = os.path.join(img_dir, fname)
            sq.save(fpath, 'WEBP', quality=85)
            kb = os.path.getsize(fpath) / 1024
            print(f"  -> {fname:<40} {kb:.1f}KB")
        
        # Square card version (500x500)
        sq = crop_square(img)
        sq = sq.resize((500, 500), Image.LANCZOS)
        fname = f"{base}-square.webp"
        fpath = os.path.join(img_dir, fname)
        sq.save(fpath, 'WEBP', quality=85)
        kb = os.path.getsize(fpath) / 1024
        print(f"  -> {fname:<40} {kb:.1f}KB (card)")

print("\n" + "=" * 60)
print("DONE")

# List all new WebP filesnew_webps = [f for f in os.listdir(img_dir) if f.endswith('.webp') and not f.endswith('.svg') and f not in ['favicon.svg']]
print(f"\nWebP files created: {len(new_webps)}")
for f in sorted(new_webps):
    sz = os.path.getsize(os.path.join(img_dir, f)) / 1024)
    print(f"  {f:<45}{sz" + " .1f}KB")