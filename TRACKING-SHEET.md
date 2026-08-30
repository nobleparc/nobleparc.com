# Nobleparc — Order Tracking Sheet (Google Sheets)

**Zero cost. Controllo umano obbligatorio. Mainland USA only.**

---

## Setup

1. Vai su https://sheets.new
2. Crea due tab: `Orders` e `Finance`
3. Copia la riga intestazione qui sotto nel tab **Orders**
4. Apri **Extensions → Apps Script**, incolla il codice da `cloudflare-worker/AppsScript.gs`
5. Deploy → Web App → Execute as: Me → Who has access: **Anyone**
6. Copia l'URL Web App → incollalo in `cloudflare-worker/index.js` come `SHEET_SCRIPT_URL`
7. Deploy il Worker: `npx wrangler deploy`

## Orders Sheet — Intestazione Colonne (fila 1)

| A | B | C | D | E | F | G | H | I | J | K | L | M | N | O | P | Q | R | S |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Timestamp | Date | Customer Name | Customer Email | Phone | Product | Price | Currency | PayPal TXN | Shipping Address | State | Country | Mainland USA | Status | CJ Order # | Tracking # | Customer Notified | Blind Shipping Note | Notes |

## Finance Sheet — Intestazione Colonne (fila 1)

| A | B | C | D | E | F | G | H | I | J |
|---|---|---|---|---|---|---|---|---|---|
| Date | PayPal TXN | Product | Gross ($) | PayPal Fee ($) | Net ($) | CJ Cost ($) | Net After CJ ($) | Customer Email | State |

## Status Legend

| Status | Significato | Azione Richiesta |
|---|---|---|
| 🟡 Payment received — pending review | PayPal ha notificato, ordine in attesa | **Validare indirizzo + mainland USA** |
| 🟢 Address verified — sent to CJ | Indirizzo OK, ordine inviato a CJ | Inserire CJ Order # in colonna O |
| 🔵 Tracking received — customer notified | CJ ha fornito tracking | **Inviare tracking al cliente**, colonna Q → YES |
| ⚪ Delivered | Consegna completata | Archiviare dopo 14 giorni |
| 🔴 Refund issued | Rimborso erogato | Note: motivo del rimborso |

## Operational Flow (obbligatorio — ogni ordine)

```
1. PayPal IPN → Cloudflare Worker → Google Sheet (riga 🟡 automatica)
   ↓
2. CONTROLLO UMANO (obbligatorio — non negoziabile):
   ✅ Indirizzo in mainland USA (Stato non in HI, AK, PR, GU, VI, AS, MP)
   ✅ Nome cliente valido, non generico
   ✅ Prodotto disponibile presso CJ Dropshipping
   ↓
3. Se NON mainland USA: contatta CEO per decisione (rimborso o eccezione)
   ↓
4. Se ✅ mainland USA: invia ordine a CJ Dropshipping
   ↓
5. BLIND SHIPPING NOTE — copia questa nota in ogni ordine CJ:
   "No invoice, no promotional material, no Chinese writing. 
    Neutral packaging only. Do not include any supplier branding or documents."
   ↓
6. Inserisci CJ Order # in colonna O → status 🟢
   ↓
7. Quando CJ fornisce tracking → colonna P → status 🔵
   ↓
8. INVIA EMAIL AL CLIENTE con tracking number
   ↓
9. Colonna Q → YES → status 🔵
   ↓
10. Dopo 14 giorni dalla consegna → status ⚪
```

## Blind Dropshipping Note (TESTUALE — da copiare in ogni ordine)

```
⚠️ BLIND SHIPPING REQUIREMENT — CRITICAL:
- No invoice, no receipt, no price tag inside the package
- No promotional material, no flyers, no coupons
- No Chinese writing or supplier branding anywhere on the package or contents
- Neutral unbranded packaging only
- Return address must be generic or US-based if possible
- Any violation will result in immediate cancellation of future orders
```

## Data Validation (da impostare su colonna N)

```
🟡 Payment received — pending review
🟢 Address verified — sent to CJ
🔵 Tracking received — customer notified
⚪ Delivered
🔴 Refund issued
```

## Margini Automatici (Finance Sheet)

Il Google Apps Script calcola automaticamente:

```
PayPal Fee   = Gross × 0.0299 + 0.49
Net          = Gross - PayPal Fee
CJ Cost      = (da inserire manualmente dopo l'ordine)
Net After CJ = Net - CJ Cost
```

**Esempio:**
```
Mask:     $69.00 - $2.55 (fee) = $66.94 - $15 (CJ) = $51.94 net (75% margin)
Massager: $39.00 - $1.66 (fee) = $37.34 - $8 (CJ)  = $29.34 net (75% margin)
```

## URL Template

```
Orders:  https://docs.google.com/spreadsheets/d/YOUR_SHEET_ID/edit#gid=0
Finance: https://docs.google.com/spreadsheets/d/YOUR_SHEET_ID/edit#gid=1
```

Replace `YOUR_SHEET_ID` with the actual ID from your Google Sheet URL.