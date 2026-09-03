#!/bin/bash
# Nobleparc — Image Processing Pipeline
# Warm tone correction + multi-resolution WebP export
set -e

IMG_DIR="static/images"

echo "========================================"
echo "  NOBLEPARC IMAGE PROCESSING PIPELINE"
echo "========================================"

# Helper function: process one image into multi-res WebP set
process_image() {
    local src="$1"
    local base="$2"
    
    echo ""
    echo ">>> Processing: $src -> $base"
    echo "  Original: $(identify -format '%wx%h %b' "$IMG_DIR/$src" 2>/dev/null)"
    
    # Step 1: Crop to square (center crop)
    # Step 2: Warm tone: boost reds, reduce blues, increase saturation
    # Step 3: Add warm vignette for wellness ambience
    # Step 4: Resize and export as WebP
    
    for size in 1200 768 480; do
        convert "$IMG_DIR/$src" \
            -gravity center \
            -crop "${size}x${size}+0+0" \
            -resize "${size}x${size}^" \
            -modulate 100,115,100 \
            -colorize 8,3,0 \
            -vignette 0x25 \
            -quality 85 \
            "$IMG_DIR/${base}-${size}w.webp"
        
        kb=$(du -k "$IMG_DIR/${base}-${size}w.webp" | cut -f1)
        echo "  -> ${base}-${size}w.webp  ${kb}KB"
    done
    
    # Square card version (500x500) for homepage cards
    convert "$IMG_DIR/$src" \
        -gravity center \
        -crop "500x500+0+0" \
        -resize "500x500^" \
        -modulate 100,115,100 \
        -colorize 8,3,0 \
        -vignette 0x25 \
        -quality 85 \
        "$IMG_DIR/${base}-square.webp"
    
    kb=$(du -k "$IMG_DIR/${base}-square.webp" | cut -f1)
    echo "  -> ${base}-square.webp  ${kb}KB (card)"
}

# === RED LIGHT THERAPY MASK ===
process_image "mask-product-3.jpg"  "mask-hero"
process_image "mask-product-8.jpg"  "mask-lifestyle"

# === SCALP MASSAGER ===
process_image "massager-product-2.jpg" "massager-hero"
process_image "massager-product-4.jpg" "massager-angle"

echo ""
echo "========================================"
echo "  DONE — WebP files created:"
echo "========================================"
ls -lh "$IMG_DIR"/*.webp 2>/dev/null | grep -v '\.svg' | awk '{print "  " $NF " (" $5 ")"}'
echo ""
echo "Total: $(ls "$IMG_DIR"/*.webp 2>/dev/null | grep -v '\.svg' | wc -l) files"