#!/usr/bin/env python3
"""Nobleparc — Lifestyle Scene Generator v2
Creates 10 unique warm ambient composite scenes with products naturally placed in context.
Cinematic, aspirational, no white backgrounds.
"""
from PIL import Image, ImageEnhance, ImageFilter, ImageDraw
import os, math

IMG_DIR = "static/images"
OUT_W, OUT_H = 1200, 900  # 4:3 base

os.makedirs(IMG_DIR, exist_ok=True)

# ── helpers ──────────────────────────────────────────────────────

def extract_product(src_file, threshold=235):
    """Load product, create mask from white bg, return (product_rgba, mask)."""
    path = os.path.join(IMG_DIR, src_file)
    if not os.path.exists(path):
        return None, None
    img = Image.open(path).convert("RGBA")
    gray = img.convert("L")
    mask = gray.point(lambda x: 0 if x > threshold else 255)
    mask = mask.filter(ImageFilter.SMOOTH_MORE)
    return img, mask


def place_product(bg, product, mask, x_ratio=0.5, y_ratio=0.5, scale=1.0):
    """Place product onto bg at position, return composited image."""
    if product is None:
        return bg
    bg = bg.convert('RGBA').copy()
    # Scale product to fit bg
    prod_w = int(product.width * scale)
    prod_h = int(product.height * scale)
    product_resized = product.resize((prod_w, prod_h), Image.LANCZOS)
    mask_resized = mask.resize((prod_w, prod_h), Image.LANCZOS)
    
    x = int((bg.width - prod_w) * x_ratio)
    y = int((bg.height - prod_h) * y_ratio)
    
    bg.paste(product_resized, (x, y), mask_resized)
    
    # Soft shadow under product
    shadow = Image.new('L', (prod_w, prod_h), 0)
    shadow_draw = ImageDraw.Draw(shadow)
    shadow_draw.ellipse([prod_w*0.15, prod_h*0.82, prod_w*0.85, prod_h*0.98], fill=80)
    shadow = shadow.filter(ImageFilter.GaussianBlur(radius=12))
    bg_shadow = Image.new('RGBA', bg.size, (0,0,0,0))
    bg_shadow.paste((0,0,0,60), (x, y+prod_h-25), shadow)
    bg = Image.alpha_composite(bg, bg_shadow)
    
    return bg


def warm_grade(im, warmth_val=1.10, sat=1.08, bright=1.02):
    """Apply warm color grade."""
    im = im.convert('RGB')
    im = ImageEnhance.Color(im).enhance(sat)
    im = ImageEnhance.Brightness(im).enhance(bright)
    # Warm tone via red channel boost using point
    r, g, b = im.split()
    r = r.point(lambda i: min(255, int(i * warmth_val)))
    return Image.merge('RGB', (r, g, b))


def save_responsive(im, basename):
    """Save as WebP at 480, 768, 1200w + card (500x500)."""
    files = {}
    for w in [1200, 768, 480]:
        h = int(w * 0.75)
        resized = im.resize((w, h), Image.LANCZOS)
        fname = f"{basename}-{w}w.webp"
        path = os.path.join(IMG_DIR, fname)
        resized.save(path, 'WEBP', quality=92)
        files[w] = (fname, os.path.getsize(path) // 1024)
    
    # Card version
    card = im.resize((500, 500), Image.LANCZOS)
    fname_card = f"{basename}-card.webp"
    path_card = os.path.join(IMG_DIR, fname_card)
    card.save(path_card, 'WEBP', quality=90)
    files['card'] = (fname_card, os.path.getsize(path_card) // 1024)
    
    for k, (n, sz) in files.items():
        print(f"    ✅ {n} ({sz}KB)")


def create_bg(w, h, base_color, accent_color, light_color, shape='gradient'):
    """Create a warm gradient background with subtle shapes."""
    bg = Image.new('RGBA', (w, h), base_color + (255,))
    draw = ImageDraw.Draw(bg, 'RGBA')
    
    # Radial glow from center-right
    cx, cy = int(w*0.65), int(h*0.4)
    for r in range(max(w,h), 0, -10):
        alpha = max(0, int(20 * (1 - r/max(w,h))))
        draw.ellipse([cx-r, cy-r, cx+r, cy+r], fill=accent_color + (alpha,))
    
    # Subtle warm glow from left
    cx2, cy2 = int(w*0.15), int(h*0.7)
    for r in range(int(max(w,h)*0.6), 0, -10):
        alpha = max(0, int(12 * (1 - r/(max(w,h)*0.6))))
        draw.ellipse([cx2-r, cy2-r, cx2+r, cy2+r], fill=light_color + (alpha,))
    
    return bg.convert('RGB')


# ── SCENE DEFINITIONS ────────────────────────────────────────────

scenes = []

# ═══ MASK — Bedroom Repose ═══
def scene_mask_bedroom():
    """Warm bedroom, linen sheets, lamp glow, mask on pillow."""
    w, h = OUT_W, OUT_H
    bg = create_bg(w, h, (232, 218, 200), (220, 195, 170), (245, 230, 215))
    draw = ImageDraw.Draw(bg)
    # Pillow rectangle (lower-left)
    draw.rectangle([20, 480, 580, 880], fill=(245, 238, 228), outline=(230, 218, 200), width=2)
    # Pillow shadow
    draw.rectangle([15, 475, 585, 885], fill=(215, 198, 180))
    # Pillow top shape
    draw.ellipse([20, 450, 580, 520], fill=(248, 240, 230))
    # Linen sheet suggestion
    draw.rectangle([0, 780, 600, 900], fill=(240, 228, 215))
    # Warm lamp glow (top-right circle)
    for r in range(150, 0, -5):
        alpha = max(0, int(25 * (1 - r/150)))
        draw.ellipse([850-r, 50-r, 850+r, 50+r], fill=(255, 220, 180, alpha))
        bg_w = bg.copy().convert('RGBA')
    # Lamp base suggestion
    draw.rectangle([835, 180, 865, 250], fill=(180, 155, 130))
    draw.ellipse([820, 170, 880, 200], fill=(200, 175, 150))
    # Warm ambient light streak
    for i in range(3):
        y = 100 + i*60
        draw.rectangle([760, y, 840, y+30], fill=(255, 225, 190, 40))
    # Side table suggestion
    draw.rectangle([770, 480, 900, 580], fill=(185, 165, 140))
    draw.rectangle([780, 480, 890, 500], fill=(200, 178, 152))
    
    product, mask = extract_product("mask-product-3.jpg")
    result = place_product(bg, product, mask, 0.25, 0.40, 0.45)
    result = warm_grade(result, 1.12, 1.06, 1.02)
    return result

scenes.append(("mask-bedroom", scene_mask_bedroom))

# ═══ MASK — Sofa Sanctuary ═══
def scene_mask_sofa():
    """Écru sofa with velvet cushions, mask resting on throw."""
    w, h = OUT_W, OUT_H
    bg = create_bg(w, h, (240, 232, 220), (225, 210, 195), (250, 242, 232))
    draw = ImageDraw.Draw(bg)
    # Sofa back cushion
    draw.rectangle([40, 200, 560, 450], fill=(235, 225, 212), outline=(215, 200, 185), width=1)
    draw.rectangle([45, 205, 555, 445], fill=(242, 234, 222))
    # Seat cushion
    draw.rectangle([30, 440, 570, 650], fill=(238, 228, 215))
    # Velvet throw pillow (right side)
    draw.rectangle([400, 320, 550, 450], fill=(210, 190, 175))
    draw.rectangle([405, 325, 545, 445], fill=(220, 200, 182))
    # Fabric fold lines
    for x in [100, 250, 400]:
        draw.line([(x, 440), (x+20, 650)], fill=(228, 215, 200), width=1)
    
    product, mask = extract_product("mask-product-3.jpg")
    result = place_product(bg, product, mask, 0.40, 0.40, 0.40)
    result = warm_grade(result, 1.08, 1.05, 1.01)
    return result

scenes.append(("mask-sofa", scene_mask_sofa))

# ═══ MASK — Bathroom Ritual ═══
def scene_mask_bathroom():
    """Travertine marble counter, natural oils, eucalyptus, mask."""
    w, h = OUT_W, OUT_H
    bg = create_bg(w, h, (228, 218, 208), (215, 200, 190), (238, 230, 220))
    draw = ImageDraw.Draw(bg)
    # Marble counter surface
    for y_rel in [500, 530, 560]:
        draw.rectangle([0, 480, w, h], fill=(232-y_rel%50//5, 222-y_rel%50//5, 210-y_rel%50//5))
    draw.rectangle([0, 480, w, 500], fill=(235, 225, 215))
    draw.rectangle([0, 500, w, 510], fill=(230, 220, 210))
    # Marble veining
    for i in range(8):
        vx = 80 + i * 120
        draw.line([(vx, 485), (vx+40, 510)], fill=(215, 205, 195), width=1)
        draw.line([(vx+20, 510), (vx+60, 530)], fill=(220, 210, 200), width=1)
    # Tile background
    for i in range(4):
        for j in range(6):
            tx = j * 95
            ty = i * 110
            draw.rectangle([tx, ty, tx+85, ty+100], fill=(240, 232, 222), outline=(230, 220, 210), width=1)
    # Glass bottle (essential oil)
    bx, by = 780, 350
    draw.rectangle([bx-10, by+30, bx+10, by+100], fill=(200, 175, 140))
    draw.ellipse([bx-12, by+90, bx+12, by+100], fill=(190, 165, 130))
    draw.polygon([(bx-8, by+30), (bx, by-20), (bx+8, by+30)], fill=(210, 190, 160))
    # Eucalyptus stem
    draw.line([(bx-5, by-30), (bx-15, by-80)], fill=(140, 165, 130), width=3)
    draw.ellipse([bx-25, by-95, bx-12, by-75], fill=(150, 175, 140))
    
    product, mask = extract_product("mask-product-3.jpg")
    result = place_product(bg, product, mask, 0.30, 0.35, 0.42)
    result = warm_grade(result, 1.06, 1.04, 1.02)
    return result

scenes.append(("mask-bathroom", scene_mask_bathroom))

# ═══ MASK — Golden Hour Glow ═══
def scene_mask_golden():
    """Warm amber light, side table, candle, book — mask as centerpiece."""
    w, h = OUT_W, OUT_H
    bg = create_bg(w, h, (240, 218, 195), (230, 200, 175), (250, 230, 210))
    draw = ImageDraw.Draw(bg)
    # Strong golden hour glow from top-right
    for r in range(350, 0, -5):
        alpha = max(0, int(18 * (1 - r/350)))
        draw.ellipse([w-r, -r, w+r, r], fill=(255, 215, 160, alpha))
    # Side table
    draw.rectangle([680, 350, 900, 370], fill=(175, 155, 130))
    draw.rectangle([690, 370, 710, 500], fill=(160, 140, 115))
    draw.rectangle([870, 370, 890, 500], fill=(160, 140, 115))
    # Candle
    cx, cy = 780, 280
    draw.rectangle([cx-10, cy, cx+10, cy+80], fill=(228, 215, 195))
    draw.ellipse([cx-8, cy-5, cx+8, cy+5], fill=(255, 200, 100))  # flame
    draw.ellipse([cx-4, cy-10, cx+4, cy], fill=(255, 220, 150))    # flame glow
    
    product, mask = extract_product("mask-product-3.jpg")
    result = place_product(bg, product, mask, 0.20, 0.45, 0.50)
    result = warm_grade(result, 1.15, 1.10, 1.03)
    return result

scenes.append(("mask-golden", scene_mask_golden))

# ═══ MASK — Close-up Detail ═══
def scene_mask_detail():
    """Tight crop on mask LED panel, soft focus edges, warm studio."""
    w, h = OUT_W, OUT_H
    bg = create_bg(w, h, (238, 228, 218), (225, 212, 200), (248, 240, 232))
    
    product, mask = extract_product("mask-product-8.jpg", threshold=240)
    # Tight crop — zoom in on mask detail
    if product:
        product = product.resize((int(w*0.85), int(h*0.85)), Image.LANCZOS)
        mask = mask.resize((int(w*0.85), int(h*0.85)), Image.LANCZOS)
        bg.paste(product, (90, 60), mask)
    
    result = warm_grade(bg, 1.05, 1.03, 1.01)
    # Vignette for focus
    draw = ImageDraw.Draw(result)
    for r in range(500, 0, -15):
        alpha = max(0, int(8 * (1 - r/500)))
        draw.ellipse([w//2-r, h//2-r, w//2+r, h//2+r], fill=(0,0,0,alpha))
    return result

scenes.append(("mask-detail", scene_mask_detail))


# ═══ MASSAGER — Bathtub Edge ═══
def scene_massager_bathtub():
    """Stone bathtub edge, candles, bath salts, massager resting."""
    w, h = OUT_W, OUT_H
    bg = create_bg(w, h, (225, 218, 208), (210, 200, 190), (238, 232, 222))
    draw = ImageDraw.Draw(bg)
    # Bathtub edge (left side, diagonal)
    draw.polygon([(0, 200), (300, 400), (280, 500), (0, 350)], fill=(210, 200, 188))
    draw.polygon([(0, 195), (300, 395), (280, 405), (0, 205)], fill=(220, 212, 200))
    # Stone texture
    for i in range(10):
        sx = 50 + i * 25
        sy = 250 + i * 12
        draw.ellipse([sx, sy, sx+8, sy+5], fill=(200, 190, 178))
    # Candle group
    for ci, (cx, cy) in enumerate([(450, 350), (520, 370), (580, 390)]):
        draw.rectangle([cx-8, cy, cx+8, cy+60], fill=(240, 228, 210))
        draw.ellipse([cx-7, cy-4, cx+7, cy+4], fill=(255, 210, 110) if ci == 0 else (255, 200, 100))
    # Bath salts jar
    draw.rectangle([700, 380, 750, 500], fill=(200, 195, 188))
    draw.rectangle([705, 390, 745, 470], fill=(230, 220, 210))
    draw.rectangle([700, 380, 750, 395], fill=(210, 205, 198))
    
    product, mask = extract_product("massager-product-2.jpg")
    result = place_product(bg, product, mask, 0.25, 0.45, 0.35)
    result = warm_grade(result, 1.08, 1.05, 1.02)
    return result

scenes.append(("massager-bathtub", scene_massager_bathtub))

# ═══ MASSAGER — Wood Shelf ═══
def scene_massager_shelf():
    """Light oak shelf, amber oil bottle, candle, massager displayed."""
    w, h = OUT_W, OUT_H
    bg = create_bg(w, h, (232, 222, 208), (218, 205, 190), (245, 235, 222))
    draw = ImageDraw.Draw(bg)
    # Wood plank shelf
    draw.rectangle([30, 380, w-30, 400], fill=(195, 170, 140))
    draw.rectangle([30, 400, w-30, 415], fill=(185, 160, 130))
    # Wood grain
    for gx in range(50, w-50, 30):
        draw.line([(gx, 385), (gx+15, 395)], fill=(175, 150, 120), width=1)
    # Shelf bracket
    draw.rectangle([150, 415, 165, 500], fill=(165, 140, 110))
    draw.rectangle([w-165, 415, w-150, 500], fill=(165, 140, 110))
    # Amber oil bottle
    bx, by = 780, 270
    draw.rectangle([bx-12, by+20, bx+12, by+110], fill=(210, 175, 120, 200))
    draw.ellipse([bx-10, by+100, bx+10, by+110], fill=(195, 160, 105))
    draw.rectangle([bx-8, by-5, bx+8, by+20], fill=(170, 140, 90))
    # Small candle
    draw.rectangle([640, 290, 660, 380], fill=(245, 235, 220))
    draw.ellipse([638, 285, 662, 295], fill=(255, 210, 100))
    
    product, mask = extract_product("massager-product-2.jpg")
    result = place_product(bg, product, mask, 0.25, 0.30, 0.38)
    result = warm_grade(result, 1.10, 1.06, 1.02)
    return result

scenes.append(("massager-shelf", scene_massager_shelf))

# ═══ MASSAGER — Reading Corner ═══
def scene_massager_chair():
    """Deep leather chair, warm lamp, book, massager on side table."""
    w, h = OUT_W, OUT_H
    bg = create_bg(w, h, (218, 205, 190), (200, 185, 170), (235, 222, 208))
    draw = ImageDraw.Draw(bg)
    # Leather chair back (right side)
    draw.rectangle([500, 80, 780, 550], fill=(140, 110, 90))
    draw.rectangle([510, 90, 770, 540], fill=(155, 125, 100))
    # Chair seat
    draw.rectangle([480, 500, 800, 650], fill=(145, 115, 92))
    # Chair arm
    draw.rectangle([460, 250, 500, 600], fill=(130, 100, 80))
    # Side table
    draw.rectangle([160, 380, 380, 395], fill=(180, 160, 135))
    draw.ellipse([155, 375, 385, 385], fill=(185, 165, 140))
    draw.rectangle([280, 395, 300, 550], fill=(165, 145, 120))
    # Book on table
    draw.rectangle([200, 310, 340, 380], fill=(200, 185, 165))
    draw.rectangle([205, 315, 335, 375], fill=(175, 160, 140))
    draw.line([(210, 340), (330, 340)], fill=(155, 140, 120), width=1)
    draw.line([(210, 355), (330, 355)], fill=(155, 140, 120), width=1)
    
    product, mask = extract_product("massager-product-4.jpg")
    result = place_product(bg, product, mask, 0.60, 0.45, 0.35)
    result = warm_grade(result, 1.10, 1.05, 1.02)
    return result

scenes.append(("massager-chair", scene_massager_chair))

# ═══ MASSAGER — Desk Decompress ═══
def scene_massager_desk():
    """Clean desk workspace, monitor silhouette, coffee, massager."""
    w, h = OUT_W, OUT_H
    bg = create_bg(w, h, (235, 225, 215), (220, 208, 195), (248, 240, 232))
    draw = ImageDraw.Draw(bg)
    # Desk surface
    draw.rectangle([0, 450, w, h], fill=(200, 185, 165))
    draw.rectangle([0, 445, w, 455], fill=(210, 195, 175))
    # Monitor silhouette (right)
    draw.rectangle([700, 120, 900, 380], fill=(100, 100, 105))
    draw.rectangle([710, 130, 890, 370], fill=(120, 120, 125))
    draw.rectangle([780, 380, 820, 440], fill=(90, 90, 95))
    # Monitor base
    draw.rectangle([710, 390, 890, 395], fill=(110, 110, 115))
    # Coffee cup
    draw.rectangle([140, 370, 170, 440], fill=(240, 235, 228))
    draw.ellipse([138, 365, 172, 375], fill=(245, 240, 233))
    draw.rectangle([168, 385, 175, 415], fill=(240, 235, 228))
    # Notebook
    draw.rectangle([250, 380, 400, 445], fill=(248, 242, 232))
    draw.rectangle([255, 385, 395, 440], fill=(255, 250, 242))
    draw.line([(260, 415), (390, 415)], fill=(200, 195, 188), width=1)
    draw.line([(260, 425), (390, 425)], fill=(200, 195, 188), width=1)
    
    product, mask = extract_product("massager-product-2.jpg")
    result = place_product(bg, product, mask, 0.35, 0.35, 0.32)
    result = warm_grade(result, 1.07, 1.04, 1.01)
    return result

scenes.append(("massager-desk", scene_massager_desk))

# ═══ MASSAGER — Detail Close-up ═══
def scene_massager_detail():
    """Tight crop on massager handle, bamboo texture background."""
    w, h = OUT_W, OUT_H
    bg = create_bg(w, h, (225, 215, 200), (212, 200, 185), (238, 230, 218))
    # Bamboo-like vertical lines
    draw = ImageDraw.Draw(bg)
    for i in range(15):
        lx = 30 + i * 72
        draw.line([(lx, 0), (lx+8, h)], fill=(210, 198, 182), width=1)
        draw.line([(lx-2, 0), (lx+6, h)], fill=(218, 206, 190), width=1)
        # Bamboo node
        ny = 100 + i * 180
        while ny < h:
            draw.rectangle([lx-5, ny-3, lx+13, ny+3], fill=(200, 188, 172))
            ny += 200
    
    product, mask = extract_product("massager-product-4.jpg", threshold=238)
    if product:
        product = product.resize((int(w*0.75), int(h*0.75)), Image.LANCZOS)
        mask = mask.resize((int(w*0.75), int(h*0.75)), Image.LANCZOS)
        bg.paste(product, (int(w*0.15), int(h*0.15)), mask)
    
    result = warm_grade(bg, 1.05, 1.03, 1.01)
    return result

scenes.append(("massager-detail", scene_massager_detail))


# ── RUN ──────────────────────────────────────────────────────────

print("=" * 55)
print("  NOBLEPARC — Lifestyle Scene Generator")
print("=" * 55)

for name, scene_fn in scenes:
    print(f"\n🎬 Generating: {name}")
    try:
        im = scene_fn()
        im = im.convert('RGB')
        save_responsive(im, name)
    except Exception as e:
        print(f"  ❌ ERROR: {e}")
        import traceback
        traceback.print_exc()

print(f"\n{'='*55}")
print("  ✅ All 10 scenes generated!")
print(f"{'='*55}")