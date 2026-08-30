# Nobleparc — Order Tracking Sheet (Google Sheets)

Create a Google Sheet (free, no subscription) with the following columns and operational flow.

## Columns

| A | B | C | D | E | F | G | H | I | J |
|---|---|---|---|---|---|---|---|---|---|
| # | Date | Customer Name | Customer Email | Product | Price ($) | PayPal Transaction ID | Shipping Address | CJ Order # | Tracking # |
| 1 | 2026-09-01 | Jessica T. | jessica@example.com | Red Light Therapy Face Mask | 69 | 9PA12345ABCD | 123 Main St, NY, 10001 | CJ-98765 | 1Z999AA10123456784 |
| — | — | — | — | — | — | — | — | — | — |

## Operational Flow (obbligatorio)

```
1. PayPal notification email received
   ↓
2. IMMEDIATELY update row in tracking sheet (columns A–G)
   ↓
3. Place order on CJ Dropshipping platform with same customer data
   ↓
4. Copy CJ order number → column H
   ↓
5. When CJ provides tracking number → column I
   ↓
6. EMAIL customer the tracking link (via regular email — no paid email service)
   ↓
7. Mark row green/complete
```

## Color Coding

- 🟡 **Yellow** — Payment received, order not yet placed on CJ
- 🟢 **Green** — Order placed on CJ, awaiting tracking
- 🔵 **Blue** — Tracking received, customer notified
- ⚪ **White** — Delivered, complete

## Key Rules

- **No paid tools.** Use standard Google Sheets (free tier).
- **No subscriptions.** CJ Dropshipping = pay-per-order only.
- **Every row** must have at minimum: date, customer name, product, PayPal ID, shipping address.
- **Tracking number** is mandatory before closing the loop.

## URL Template

```
https://docs.google.com/spreadsheets/d/YOUR_SHEET_ID/edit
```

Replace `YOUR_SHEET_ID` with the actual ID from your Google Sheet.