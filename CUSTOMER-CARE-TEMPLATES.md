# Nobleparc — Customer Care Templates

**Lingua:** American English  
**Tono:** Empatico, professionale, trasparente  
**Tempo di risposta target:** < 24 ore

---

## 2a — Order Confirmation

**Trigger:** PayPal payment completed, order validated by human

```email
Subject: Your Nobleparc Order Is Confirmed — #NP-2026XXXXX

Hi [Customer Name],

Thank you for your order.

Here's a quick summary:

  Product:     [Product Name]
  Amount:      $[Selling Price]
  Order ID:    NP-2026XXXXX
  Ships to:    [Address Line 1], [City], [State] [ZIP]
  Delivery:    3–7 business days within the continental US

You'll receive a separate email with your tracking number as soon as your order is on its way.

If you have any questions before then, simply reply to this email. I'm here to help.

Best regards,
Nobleparc Support
support@nobleparc.com
```

---

## 2b — Shipping Delay

**Trigger:** Carrier tracking shows no movement after 7+ business days, or CJ notifies supply delay

```email
Subject: Update on Your Nobleparc Order — #NP-2026XXXXX

Hi [Customer Name],

I wanted to give you a quick update on your order.

Your package is currently experiencing a delay with the carrier. Your tracking number is [Tracking Number], and here's the latest status:

  [Current carrier status]

I've checked and the package is still moving through the system. Most delays resolve within 2-3 business days. If it doesn't update by [Date + 3 days], please reply to this email and I'll make sure we take care of it.

I'm sorry for the inconvenience and appreciate your patience.

Best regards,
Nobleparc Support
support@nobleparc.com
```

---

## 2c — Product Damaged / Defective

**Trigger:** Customer reports broken, non-functional, or visibly damaged item

```email
Subject: Your Nobleparc Order — Let's Make This Right (#NP-2026XXXXX)

Hi [Customer Name],

I'm sorry to hear that your [Product Name] arrived damaged. That's not the experience we want you to have, and I'm going to make it right.

Here's what I've done:

  A full refund of $[Selling Price] has been issued to your original payment method. You should see it reflected within 3-5 business days.

You don't need to return the item. Please keep it or dispose of it responsibly.

If you'd like a replacement instead of a refund, just reply to this email and I'll send one out at no additional cost.

Again, I'm sorry this happened. We're here to make sure you're happy with your purchase.

Best regards,
Nobleparc Support
support@nobleparc.com
```

---

## 2d — Refund / Return Request

**Trigger:** Customer asks for refund or return (any reason — 30-day guarantee applies)

### Variant A — Customer is polite, product is used or opened

```email
Subject: Your Nobleparc Refund Has Been Processed — #NP-2026XXXXX

Hi [Customer Name],

Thank you for reaching out.

We stand behind our products, so I've processed a full refund of $[Selling Price] to your original payment method. It should appear within 3-5 business days.

You do not need to return the item. Please keep it or donate it if you'd like.

I hope we can serve you better next time. If there's anything else I can help with, just reply.

Best regards,
Nobleparc Support
support@nobleparc.com
```

### Variant B — Customer is dissatisfied, product is in good condition (customer wants to return)

```email
Subject: Your Nobleparc Return — Here's What to Expect (#NP-2026XXXXX)

Hi [Customer Name],

Thank you for contacting us. I'm sorry to hear the [Product Name] didn't meet your expectations.

Since you'd like to return it, here's how it works:

1. Reply to this email with your order number to confirm.
2. You'll receive a prepaid return shipping label within 24 hours.
3. Drop the package at any [USPS / UPS] location.
4. Once we receive it, we'll process your refund within 3-5 business days.

Alternatively, if you'd prefer a faster resolution, I can process a refund now and you can keep the item — no need to send it back. Just let me know.

Whichever option you prefer, I'm here to help.

Best regards,
Nobleparc Support
support@nobleparc.com
```

### Variant C — Customer is aggressive or threatens chargeback

```email
Subject: Your Nobleparc Order — Refund Issued (#NP-2026XXXXX)

Hi [Customer Name],

I understand you're unhappy with your purchase. I've processed a full refund of $[Selling Price] to your original payment method. It should appear within 3-5 business days.

You do not need to return the item.

If you have any questions, please reply to this email. I'm here to help.

Best regards,
Nobleparc Support
support@nobleparc.com
```

---

## Template — Blind Shipping Note (per ordini CJ — non per il cliente)

Copia questo testo nel campo note dell'ordine CJ Dropshipping, **OBLIGATORIO** per ogni ordine:

```
⚠️ BLIND SHIPPING — CRITICAL INSTRUCTIONS:

1. No invoice, no receipt, no price tag inside the package
2. No promotional material, no flyers, no coupons, no QR codes
3. No Chinese writing or non-English text on the package or inside
4. No supplier branding, logos, or company name visible anywhere
5. Neutral unbranded packaging only — plain box or poly mailer
6. Return address must be generic (no Chinese characters)

FAILURE TO COMPLY WILL RESULT IN IMMEDIATE CANCELLATION OF ALL FUTURE ORDERS.
```

## Template — Traffic Source Question (da inviare 3 giorni dopo la consegna)

```email
Subject: Quick question about your Nobleparc order

Hi [Customer Name],

Hope you're enjoying your [Product Name]!

We're trying to understand where our customers find us — just for our own records. If you have a moment, could you reply with one word?

Where did you first hear about Nobleparc? (Reddit / Pinterest / Google / Friend / Other)

Thanks so much — it really helps us out.

Best regards,
Nobleparc Support
support@nobleparc.com
```