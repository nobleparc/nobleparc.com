from PIL import Image, ImageDraw, ImageEnhance, ImageFilter
import os

DIR = "static/images"

def warm_grade(im, w=1.10, s=1.08, b=1.02):
    im = im.convert('RGB')
    im = ImageEnhance.Color(im).enhance(s)
    im = ImageEnhance.Brightness(im).enhance(b)
    r,g,b = im.split()
    r = r.point(lambda i: min(255,int(i*w)))
    return Image.merge('RGB',(r,g,b))

# mask-purchase: warm marble surface, open book, soft morning light
w,h = 1200,900
bg = Image.new('RGBA', (w,h), (238, 230, 218, 255))
draw = ImageDraw.Draw(bg, 'RGBA')

# Marble surface (lower half)
draw.rectangle([0,420,w,h], fill=(232, 222, 210, 255))
draw.rectangle([0,420,w,435], fill=(235, 225, 215, 255))
for i in range(10):
    x = 50+i*110
    draw.line([(x,425),(x+30,445)], fill=(222,212,200), width=1)

# Window light (top-left)
for r in range(250,0,-8):
    a = max(0,int(14*(1-r/250)))
    draw.ellipse([100-r,50-r,100+r,50+r], fill=(255,235,210,a))

# Open book
draw.rectangle([550,490,820,600], fill=(248,242,230))
draw.rectangle([555,495,815,595], fill=(252,248,238))
draw.rectangle([685,495,690,595], fill=(220,210,195))
# Book page lines
for ly in range(510,585,25):
    draw.line([(565,ly),(680,ly)], fill=(235,228,218), width=1)
    draw.line([(690,ly),(805,ly)], fill=(235,228,218), width=1)

# Tea cup
draw.rectangle([860,440,890,500], fill=(245,240,232))
draw.ellipse([858,435,892,445], fill=(248,245,238))
draw.rectangle([892,455,898,475], fill=(245,240,232))
draw.ellipse([870,445,880,455], fill=(215,160,100,200))

bg = bg.convert('RGB')

# Load and place mask product
mask_img = Image.open(os.path.join(DIR, 'mask-product-3.jpg')).convert('RGBA')
gray_mask = mask_img.convert('L')
mask_alpha = gray_mask.point(lambda x: 0 if x>235 else 255)
mask_alpha = mask_alpha.filter(ImageFilter.SMOOTH_MORE)

prod = mask_img.resize((int(w*0.42), int(h*0.42)), Image.LANCZOS)
alp = mask_alpha.resize((int(w*0.42), int(h*0.42)), Image.LANCZOS)

bg_rgba = bg.convert('RGBA')
bg_rgba.paste(prod, (60, 220), alp)

# Shadow
shadow = Image.new('L', (int(w*0.42), int(h*0.42)), 0)
sd = ImageDraw.Draw(shadow)
sd.ellipse([50, int(h*0.42)-40, int(w*0.42)-50, int(h*0.42)-5], fill=60)
shadow = shadow.filter(ImageFilter.GaussianBlur(10))
sh = Image.new('RGBA', bg.size, (0,0,0,0))
sh.paste((0,0,0,50), (60, 220+int(h*0.42)-25), shadow)
bg_rgba = Image.alpha_composite(bg_rgba, sh)

result = warm_grade(bg_rgba, 1.10, 1.06, 1.02)

# Save
for wsize, suffix in [(1200,''), (768,''), (480,'')]:
    fname = f"mask-purchase{suffix}-{wsize}w.webp"
    if suffix == '':
        fname = f"mask-purchase-{wsize}w.webp"
    sz = wsize if wsize else w
    resized = result.resize((sz, int(sz*0.75)), Image.LANCZOS)
    resized.save(os.path.join(DIR, fname), 'WEBP', quality=92)
    print(f"  ✅ {fname} ({os.path.getsize(os.path.join(DIR,fname))//1024}KB)")

# Card version
card = result.resize((500,500), Image.LANCZOS)
card.save(os.path.join(DIR, 'mask-purchase-card.webp'), 'WEBP', quality=90)
print(f"  ✅ mask-purchase-card.webp ({os.path.getsize(os.path.join(DIR,'mask-purchase-card.webp'))//1024}KB)")