# Nobleparc.com

**Premium wellness devices for home self-care**

Static e-commerce site built with Hugo + Cloudflare Pages. Mobile-first, ultra-fast, PayPal Business Buy Now for checkout, schema.org optimized for Answer Engine Optimization (AEO).

## Tech Stack

| Layer | Choice | Why |
|---|---|---|
| SSG | Hugo (Extended) | ~60ms builds, single binary, zero JS output |
| Hosting | Cloudflare Pages (Free) | Unlimited bandwidth, 330+ PoPs, auto SSL |
| Checkout | PayPal Business (Buy Now) | Zero backend, no subscription fees, US-ready |
| CSS | Single file, mobile-first | ~12KB uncompressed, system fonts |
| JS | Vanilla, ~1KB | Accordion + nav toggle only |
| Costs | **$0 recurring** | No paid plugins, analytics, or subscriptions |

## Project Structure

```
nobleparc.com/
├── hugo.toml                    # Site config
├── content/
│   ├── _index.md                # Homepage
│   ├── products/
│   │   ├── red-light-therapy-mask.md
│   │   └── electric-scalp-massager.md
│   ├── faq/_index.md
│   ├── about/_index.md
│   ├── shipping-returns/_index.md
│   ├── privacy/_index.md
│   ├── terms/_index.md
│   ├── confirmation/_index.md
│   └── 404.md
├── layouts/
│   ├── _default/
│   │   ├── baseof.html
│   │   ├── single.html          # Policy pages, about
│   │   └── list.html            # Products index
│   ├── index.html               # Homepage
│   ├── 404.html
│   ├── products/single.html     # Product detail template
│   └── partials/
│       ├── head/meta.html
│       ├── head/schema.html
│       ├── header.html
│       └── footer.html
├── assets/
│   ├── css/style.css            # Full stylesheet (~12KB)
│   └── js/accordion.js          # Accordion + nav (~1KB)
├── static/
│   ├── _headers                 # Security + caching headers
│   ├── robots.txt
│   └── images/
└── README.md
```

## Quick Start

```bash
# Prerequisites: Hugo Extended
sudo apt install hugo-extended   # Linux
brew install hugo                 # macOS

# Dev server
hugo server -D --disableFastRender

# Production build
hugo --minify

# Deploy to Cloudflare Pages
npx wrangler pages deploy public/ --project-name nobleparc-com
```

Or connect GitHub repo in Cloudflare Dashboard → Pages → Connect Git.

## PayPal Business Setup (Active Checkout)

Stripe is currently blocked. All checkout buttons use **PayPal Business Buy Now** forms.

### To Activate Checkout:

1. Create a **PayPal Business** account at paypal.com/business
2. Verify your business email address
3. In `hugo.toml`, set: `paypalEmail = "your-verified-business@email.com"`
4. Rebuild: `hugo --minify`

The template automatically generates PayPal Buy Now forms on every product page and mobile CTA with:
- Product name, price, USD currency
- Shipping address required (`no_shipping=2`)
- Post-purchase redirect to `/confirmation/`
- Cancel redirect back to homepage
- **No subscription fees, no monthly costs, no platform lock-in**

When `paypalEmail` is empty, product pages show "Coming Soon — Join Waitlist" with no checkout form.

## Cost Policy — Zero Recurring Expenses

**Absolutely no subscriptions** of any kind are authorized:
- ❌ No dropshipping platform subscriptions (CJ Dropshipping = pay-per-order only)
- ❌ No analytics SaaS (use free tier or self-hosted)
- ❌ No email marketing platforms with recurring fees
- ❌ No paid plugins or premium themes
- ✅ Pay-as-you-go only (MOQ 1, no fixed costs)
- ✅ Everything free-tier or $0 recurring

## Copy Rules (⚠️ NO MEDICAL CLAIMS — FTC/FDA COMPLIANCE)

All product copy uses **wellness & cosmetic** language only. **No therapeutic/medical claims ever.**

| ✅ Use | ❌ Never Use |
|---|---|
| "supports skin vitality" | "treats acne" |
| "radiant appearance" | "eliminates wrinkles" |
| "self-care routine" | "cures skin conditions" |
| "helps you unwind" | "medical treatment" |
| "soothing experience" | "hair growth treatment" |
| "appearance of fine lines" | "removes wrinkles" |
| "wellness device" | "medical device" |
| "clinical-grade technology" | "clinically proven" |

**Disclaimer** displayed in footer and FAQ:
> "These products are not intended to diagnose, treat, cure, or prevent any disease."

## Schema.org Coverage

Every page:
- **Organization** — Nobleparc brand, contact
- **Product** (product pages) — name, price ($69/$39), free shipping, 30-day return, SKU
- **FAQPage** — 10-11 questions per product page
- **BreadcrumbList** — navigation path

## Performance Targets

| Metric | Target | Actual |
|---|---|---|
| LCP | <1.5s | — |
| CSS | <50KB | ~12KB |
| JS | <5KB | ~1KB |
| Images | <40KB each | (placeholder) |
| Pages | <100KB total | ~15-17KB each |

## Deployment

1. Push to GitHub: `nobleparc/nobleparc.com`
2. Cloudflare Pages auto-deploys from main branch
3. Custom domain: `nobleparc.com` with Cloudflare DNS proxy

---

*Built August 2026. Maintained by Nobleparc. No subscriptions, no monthly fees.*