# Nobleparc — Piano Operativo Completo (Fase 3)

> **Documento di strategia e infrastruttura operativa**  
> Ruolo: Hermes come CEO, coordinamento di 6 sub-agenti  
> Target: Mainland USA · Lingua: American English  
> Budget: $0 ricorrenti · Zero SaaS a pagamento

---

## 1. Architettura Fulfillment + Customer Care a Costo Zero

### Flusso End-to-End dal Click alla Consegna

```
┌──────────────┐     ┌──────────────────┐     ┌───────────────────────┐
│ PayPal IPN   │────▶│ Cloudflare Worker │────▶│ Google Sheet Ordini   │
│ (webhook)    │     │ (verifica: USA    │     │ (staging row: 🟡)     │
│              │     │  continentale)    │     │                       │
└──────────────┘     └──────────────────┘     └───────────────────────┘
                                                         │
                                                         ▼
                                              ┌───────────────────────┐
                                              │ CONTROLLO UMANO       │
                                              │ ✅ Validazione ind.    │
                                              │ ✅ Blind ship note    │
                                              │ 🟡→🟢 → Invia a CJ    │
                                              └───────────────────────┘
                                                         │
                                                         ▼
                                              ┌───────────────────────┐
                                              │ CJ Dropshipping       │
                                              │ (pay-per-order)       │
                                              │ → ottieni tracking # │
                                              └───────────────────────┘
                                                         │
                                                         ▼
                                              ┌───────────────────────┐
                                              │ Tracking # → cliente  │
                                              │ Row 🟢→🔵→⚪         │
                                              └───────────────────────┘
```

### 1.1 PayPal IPN → Cloudflare Worker

Il Worker ascolta le notifiche IPN (Instant Payment Notification) di PayPal.

```javascript
// cloudflare-worker.js — Deploy su Cloudflare Workers (free tier, 100k req/giorno)
// Endpoint: https://nobleparc.app/ipn

addEventListener('fetch', event => {
  event.respondWith(handleIPN(event.request))
})

async function handleIPN(request) {
  if (request.method !== 'POST') return new Response('OK', { status: 200 })
  
  const formData = await request.formData()
  const txnType = formData.get('txn_type')
  const paymentStatus = formData.get('payment_status')
  const receiverEmail = formData.get('receiver_email')
  const itemName = formData.get('item_name')
  const itemAmount = formData.get('mc_gross')
  const currency = formData.get('mc_currency')
  const payerEmail = formData.get('payer_email')
  const payerName = `${formData.get('first_name') || ''} ${formData.get('last_name') || ''}`
  const addressStreet = formData.get('address_street') || ''
  const addressCity = formData.get('address_city') || ''
  const addressState = formData.get('address_state') || ''
  const addressZip = formData.get('address_zip') || ''
  const addressCountry = formData.get('address_country_code') || ''
  const txnId = formData.get('txn_id')
  
  // Solo pagamenti completati e ricevuti da info@nobleparc.com
  if (paymentStatus !== 'Completed') return new Response('OK', { status: 200 })
  if (receiverEmail !== 'info@nobleparc.com') return new Response('OK', { status: 200 })
  
  // Verifica che il paese sia US mainland
  const invalidZones = ['HI', 'AK', 'PR', 'GU', 'VI', 'AS', 'MP']
  const isMainland = addressCountry === 'US' && !invalidZones.includes(addressState)
  
  if (!isMainland) {
    // Rimborso automatico + email di cortesia
    await sendRefund(txnId, 'Ships to US mainland only - refund issued')
    return new Response('OK', { status: 200 })
  }
  
  // Scrivi su Google Sheet via Apps Script Web App
  const row = {
    date: new Date().toISOString().split('T')[0],
    customer_name: payerName,
    customer_email: payerEmail,
    product: itemName,
    price: itemAmount,
    paypal_txn_id: txnId,
    shipping_street: addressStreet,
    shipping_city: addressCity,
    shipping_state: addressState,
    shipping_zip: addressZip,
    status: '🟡 Payment received - pending review',
    blind_shipping_note: '⚠️ APPLY: No invoice, no promo, no Chinese writing. Neutral packaging only.'
  }
  
  await appendToSheet(JSON.stringify(row))
  
  return new Response('OK', { status: 200 })
}

async function appendToSheet(rowJson) {
  // POST al Web App URL di Google Apps Script
  const scriptURL = 'https://script.google.com/macros/s/YOUR_SCRIPT_ID/exec'
  await fetch(scriptURL, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: rowJson
  })
}
```

**Deploy:**  
`npx wrangler deploy cloudflare-worker.js --name nobleparc-ipn`

Poi in PayPal Dashboard:  
**Profile → Notification preferences → IPN → URL:** `https://nobleparc.app/ipn`

### 1.2 Google Sheets — Foglio Ordini Operativo

**Template columns (A–K):**

| A | B | C | D | E | F | G | H | I | J | K | L | M |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Date | Customer | Email | Product | Price | PayPal TXN | Address | State | Status | CJ Order # | Tracking | Customer Notified | Notes |

**Status legend (dropdown validation):**
- 🟡 Payment received – pending review
- 🟢 Address verified – sent to CJ
- 🔵 Tracking received – customer notified
- ⚪ Delivered
- 🔴 Refund issued

**Google Apps Script (Web App) — riceve dal Worker e scrive:**

```javascript
// Google Apps Script — deploy come Web App (execute as me, anyone access)
function doPost(e) {
  const sheet = SpreadsheetApp.openById('YOUR_SHEET_ID').getSheetByName('Orders')
  const data = JSON.parse(e.postData.contents)
  
  sheet.appendRow([
    data.date,
    data.customer_name,
    data.customer_email,
    data.product,
    data.price,
    data.paypal_txn_id,
    `${data.shipping_street}, ${data.shipping_city}, ${data.shipping_state} ${data.shipping_zip}`,
    data.shipping_state,
    data.status,
    '', // CJ Order #
    '', // Tracking
    'NO', // Customer notified
    data.blind_shipping_note
  ])
  
  return ContentService.createTextOutput('OK')
}
```

### 1.3 Protocollo Resi Intelligente

Per prodotti sotto i $150, la logistica inversa Cina—USA è antieconomica. **Politica:**

| Scenario | Azione | Costo |
|---|---|---|
| Cliente insoddisfatto, prodotto usato | **Rimborso parziale (50%)** o sostituzione | $0–39 |
| Prodotto difettoso (arrivato rotto) | **Rimborso totale + sostituzione** | $69 (sostituzione a carico CJ) |
| Cliente educato, buona fede | Rimborso totale, non chiedere reso | $69 (costo di acquisizione reputazione) |
| Cliente aggressivo/chargeback threat | Rimborso immediato + chiudi | $69 (chargeback fee $15-25 peggiore) |

**Regola empirica:** se il costo del prodotto pagato a CJ + shipping di ritorno > $30, meglio rimborsare senza reso. Un chargeback costa $15-25 di fee + perdi il prodotto.

### 1.4 Template di Risposta Customer Care

```email
Subject: Your Nobleparc Order — Quick Update

Hi [Customer Name],

Thank you for reaching out.

Regarding your order of the [Product Name]:
[Insert specific response based on case]

For your reference, your order number is [PayPal TXN].

If there's anything else I can help with, simply reply to this email.
I'm here to make sure you're happy with your purchase.

Best regards,
Nobleparc Support
support@nobleparc.com
```

**Template per refund senza reso:**
```email
Subject: Your Nobleparc Refund — Processed ✔

Hi [Customer Name],

A full refund of $[amount] has been issued to your original payment method.
You should see it reflected within 3-5 business days, depending on your bank.

You do not need to return the item — please keep it or donate it.

I hope we can serve you better next time.

Best regards,
Nobleparc Support
```

---

## 2. Piano Content Studio — Realistico

### 2.1 Recupero Media Reali

**Senza foto reali disponibili nei fornitori in questo momento:**

| Priorità | Azione | Costo | Tempo |
|---|---|---|---|
| 🟢 **Week 1** | Foto stock ULTRA-REALISTICHE AI-generated (product mockups) via strumento gratuito (Bing Image Creator / Playground AI free tier) | $0 | 2 ore |
| 🟢 **Week 1** | Photo editing: GIMP open-source per cropping, lighting, webp export | $0 | 1 ora |
| 🟡 **Week 2-3** | Richiedere foto reali ai fornitori CJ Dropshipping | $0 | Attesa |
| 🔵 **Week 4+** | Review manuali con screenshot reali dei tester | $0 | Continuo |

**Standard visivo:**
- Sfondo: pulito, light, atmosfera spa (non laboratorio)
- Modello: stile lifestyle (routine domestica, non "ospedale")
- Colori: Non alterare le tinte reali del prodotto
- Formato: 1200×1200px minimo, WebP con srcset 480/768/1200

### 2.2 Pipeline Elaborazione (gratuita, CLI)

```bash
# Convert any source image into responsive WebP set
# Prereq: libwebp (apt-get install webp)

INPUT=$1  # e.g. mask-original.jpg
NAME=$2   # e.g. product-mask

for SIZE in 480 768 1200; do
  convert "$INPUT" -resize ${SIZE}x${SIZE}^ -gravity center -extent ${SIZE}x${SIZE} \
    -quality 85 -define webp:method=6 "/root/nobleparc/nobleparc/static/images/${NAME}-${SIZE}.webp"
done

# Square version for homepage cards
convert "$INPUT" -resize 500x500^ -gravity center -extent 500x500 \
  -quality 85 -define webp:method=6 "/root/nobleparc/nobleparc/static/images/${NAME}-square.webp"
```

### 2.3 Evoluzione Visuale

| Fase | Stato | Canale |
|---|---|---|
| Fase 1 | Stock / AI generato → placeholder decorosi | Sito web |
| Fase 2 | Foto reali fornitore → sostituzione stock | Sito web + Pinterest |
| Fase 3 | Foto reali con tester umani (redditor) | Reddit + Pinterest |
| Fase 4 | UGC (user-generated content) da recensioni | Tutti i canali |

---

## 3. SEO & AEO — Linee Guida

### 3.1 Stato Attuale (già implementato)

| Schema | Pagine | Status |
|---|---|---|
| Organization | Tutte | ✅ |
| Product | Mask ($69), Massager ($39) | ✅ |
| FAQPage | Mask (11 Q), Massager (10 Q), /faq/ (24 Q) | ✅ |
| BreadcrumbList | Tutte | ✅ |
| ShippingDetails | Free US, 3-7gg | ✅ |
| MerchantReturnPolicy | 30-day, FreeReturn | ✅ |

### 3.2 Ottimizzazioni Mancanti (da implementare)

- **Meta titles più lunghi e ricchi di keyword:** ogni pagina deve avere title 50-60 caratteri
- **H1 unico per pagina:** già presente ✅
- **Alt text descrittivo:** già presente ✅
- **Internal linking:** aggiungere link tra pagine prodotto nelle FAQ (es. "our Red Light Mask pairs perfectly with the Electric Scalp Massager")
- **Blog/Content hub** (Fase 2): `/blog/` con articoli AEO:
  - "What Is Red Light Therapy? A Complete Guide for Home Use"  
  - "Red Light vs Near-Infrared: Which Wavelength Should You Choose?"
  - "How to Build a 10-Minute Evening Wellness Routine"

### 3.3 AEO — Ottimizzazione per Motori AI

**Principio:** rispondere direttamente alle domande con risposte di 40-60 parole, in formato che Perplexity e ChatGPT Search possano citare.

**Già fatto:** FAQ con 40-60 word answers su ogni prodotto ✅

**Da fare:**
- Aggiungere sezione "Quick Answers" in cima al /faq/ con le 5 domande più frequenti
- Usare le People Also Ask di Google come sorgente per nuove domande FAQ
- Monitorare citazioni su Perplexity (ricerca manuale settimanale)

---

## 4. Strategia Marketing Organico Sequenziale

### Fase 1 — Subito (Day 1–14)

**Canale A: Reddit — Solution-Drop**

| Subreddit | Approccio | Frequenza |
|---|---|---|
| r/SkincareAddiction | Mai link diretto. Rispondi a domande con consigli genuini | 2-3x/settimana |
| r/redlighttherapy | Partecipa a discussioni tecniche. "I use the Nobleparc mask and it helps" | 3-4x/settimana |
| r/30PlusSkinCare | Consigli su routine. Contesto naturale | 2x/settimana |
| r/massage | Per il massager, condividi esperienze d'uso | 1-2x/settimana |

**Regole d'oro:**
1. Account singolo, storico reale, sembrare una persona vera
2. Prima rispondi a 5-10 thread SENZA menzionare Nobleparc (crei credibilità)
3. Menzione solo quando è una risposta genuinamente utile al problema specifico
4. Mai: "check out my store", "use code X", link diretto nei commenti iniziali

**Canale B: Pinterest — Pin Aspirazionali**

- Creare 3 board: "Home Wellness Rituals", "LED Light Therapy at Home", "Self-Care Evening Routine"
- Pin immagini del prodotto in contesto spa domestico
- Descrizioni SEO: "How to build a 10-minute evening wellness routine with red light therapy — free US shipping"
- Frequenza: 3-5 pin/giorno (strumento manuale, niente scheduler a pagamento)

### Fase 2 — Day 15–45

**Canale C: TikTok — Video Brevi**

- 30-60 secondi, tono naturale, non vendita
- Esempi: "My 10-minute red light routine" (ASMR-style), "Scalp massager before bed = game changer"
- Frequenza: 3-4 video/settimana
- Zero ads, zero boost

**Canale D: Instagram — Estetica Premium**

- 3 post/settimana + Stories
- Griglia visiva coerente (toni caldi, minimal)
- Contenuti: routine, unboxing, science explainer (wellness language)

### Fase 3 — Day 45–90

**Canale E: YouTube — Authority**

- Video: "Red Light Therapy at Home: Complete Beginner's Guide" (5-10 min)
- Tono: educativo, non promozionale, link in descrizione
- 1 video/settimana

---

## 5. Sintesi Competitiva e Posizionamento

| Brand | Fascia | Prezzo Mask | Posizionamento | Gap |
|---|---|---|---|---|
| **CurrentBody** | Alta | $399 | Science-heavy, clinic vibes | Prezzo esclude massa |
| **HigherDOSE** | Alta | $349 | Celebrità, lifestyle | Inaccessibile a molti |
| **Omnilux** | Medio-alta | $390 | Clinically-proven | Stesso problema prezzo |
| **Amazon generici** | Bassa | $30-80 | Zero brand, zero fiducia | Qualità inconsistente |
| **Nobleparc** | **Media-premium** | **$69** | **Wellness accessibile** | **Qualità percepita + prezzo onesto** |

**Gap di mercato:**  
Esiste un vuoto enorme tra i brand "premium" ($300-400) e i generici Amazon ($30 con zero fiducia).  
Nobleparc si posiziona qui — $69 è un prezzo che una persona normale paga per un buon paio di scarpe.  
Non serve convincere nessuno che è un "investimento" — è semplicemente un prezzo giusto per un prodotto curato.

**Messaggio chiave:** "Premium wellness devices, without the premium price tag. Same technology, fair pricing."

---

## 6. Struttura dei 6 Sub-Agenti

### Ordine di Attivazione

```
Month 1                          Month 2                  Month 3
┌─────────────────────┐   ┌──────────────┐   ┌──────────────────┐
│ ① Operations        │   │ ③ Content    │   │ ⑤ Organic Growth  │
│ ② Customer Care     │   │ ④ SEO/AEO    │   │ ⑥ Finance/Intel    │
└─────────────────────┘   └──────────────┘   └──────────────────┘
        │                        │                      │
        ▼                        ▼                      ▼
   Giornaliero             Settimanale           Quindicinale
```

> **Agente 0 — Hermes (CEO):** supervisione, decisioni, approvazione spese, controllo qualità

### Agente 1 — Operations & Fulfillment (Attivazione: Day 1)

| Compito | Dettaglio | Output |
|---|---|---|
| PayPal IPN → Sheet | Verificare che il Worker Cloudflare scriva righe sul foglio | Sheet popolato ogni giorno |
| Validazione indirizzi | Controllare che stato/cap siano mainland US | Row 🟢 o 🔴 |
| Ordini CJ | Inviare ordine a CJ Dropshipping con Blind Ship Note | CJ Order # nella riga |
| Tracking | Inserire tracking number e notificare cliente | Row 🔵 |
| Archiviazione | Righe ⚪ dopo 14 giorni dalla consegna | Sheet pulito |

**Interazione con Agente 2:** se cliente apre un ticket, Operations segnala la riga con note.

### Agente 2 — Customer Care & Returns (Attivazione: Day 1)

| Compito | Dettaglio | Output |
|---|---|---|
| Risposta ticket | Template per casi comuni in <24 ore | Customer satisfied |
| Valutazione resi | Applicare la politica intelligente (rimborso vs sostituzione) | Decisione + azione |
| Rimborsi manuali | Per casi fuori politica, escalare a CEO (Hermes) | Approvazione |
| Chargeback prevention | Rimborso proattivo per clienti insoddisfatti prima che aprano dispute | Zero chargeback |
| Feedback loop | Segnalare ad Operations prodotti con difetti ricorrenti | Report mensile |

### Agente 3 — Content & Visual Studio (Attivazione: Day 8)

| Compito | Dettaglio |
|---|---|
| Recuperare foto reali fornitore CJ | Richiedere immagini raw |
| Elaborare immagini | Pipeline WebP con srcset |
| Mantenere coerenza visiva | Sfondo pulito, atmosfera spa, niente alterazioni prodotto |
| Pinterest pins | 3-5/giorno con descrizioni SEO |
| Template social | Foto pronte per Reddit e TikTok |

### Agente 4 — SEO & AEO (Attivazione: Day 8)

| Compito | Dettaglio |
|---|---|
| Audit meta esistenti | Tutti i title/description delle pagine |
| FAQ aggiornamento | Aggiungere nuove domande da People Also Ask |
| Blog/content hub | Pianificare articoli authority (1x/settimana da Day 15) |
| Schema monitoring | Validare JSON-LD su validator.schema.org settimanalmente |
| Perplexity monitoring | Ricerca manuale "best red light therapy mask" — siamo citati? |

### Agente 5 — Organic Growth (Attivazione: Day 15)

| Compito | Dettaglio |
|---|---|
| Reddit solution-drop | 3-4 commenti/settimana con valore reale |
| Pinterest | Pin giornalieri, mantenere 3 board |
| TikTok (Fase 2) | 3 video/settimana da Day 30 |
| Report traffico | Fonti di traffico via Cloudflare Analytics (gratis) |

**Interazione con Agente 4:** SEO/AEO prepara keyword → Organic Growth le usa nei post

### Agente 6 — Finance & Intelligence (Attivazione: Day 30)

| Compito | Dettaglio |
|---|---|
| Tracciamento incassi | Sheet + PayPal report mensile |
| Buffer fiscale | Monitorare somma verso target $4,000-5,000 |
| Margini unitari | Prezzo - CJ cost - PayPal fee(2.99%+$0.49) = Netto |
| Fonti di traffico | Attribuzione da Cloudflare Analytics |
| Competitor watch | Prezzi CurrentBody/Omnilux — cambi mensili |

**Formula margine:**
```
Netto = (Prezzo × 0.9701 - 0.49) - CostoCJ
Mask:   ($69 × 0.9701 - 0.49) - $15 = $66.94 - $15 = $51.94 (75% margin) ✓
Massager: ($39 × 0.9701 - 0.49) - $8 = $37.34 - $8 = $29.34 (75% margin) ✓
```

---

## 7. Piano Primi 30 Giorni — Priorità Operative

```
Settimana 1 (Day 1-7)                    Settimana 2 (Day 8-14)
┌─────────────────────────────┐         ┌─────────────────────────────┐
│ ████████████████████░░░░░░░ │         │ ██████████████████████░░░░░ │
│                             │         │                             │
│ ✅ Deploy Cloudflare Worker │         │ ✅ Pinterest board setup    │
│ ✅ Google Sheet operativo   │         │ ✅ Pinterest pin schedule   │
│ ✅ Template email customer  │         │ ✅ Recupero foto fornitore  │
│ ✅ Protocollo resi          │         │ ✅ Pipeline elaborazione    │
│ ✅ Politica rimborso intell.│         │ ✅ Reddit attivo (valore)   │
│ ✅ PayPal IPN configurato   │         │ ✅ SEO audit completato     │
│                             │         │                             │
└─────────────────────────────┘         └─────────────────────────────┘

Settimana 3 (Day 15-21)                 Settimana 4 (Day 22-30)
┌─────────────────────────────┐         ┌─────────────────────────────┐
│ ██████████████████████████░ │         │ ███████████████████████████ │
│                             │         │                             │
│ ✅ Primi ordini reali evasi │         │ ✅ Buffer fiscale tracciato │
│ ✅ Blog post #1 pubblicato  │         │ ✅ Report prime 4 settimane │
│ ✅ Reddit settimana 2 attiva│         │ ✅ Decisione Fase 2/TikTok  │
│ ✅ Foto sostituite su sito  │         │ ✅ Aggiustamenti su dati    │
│ ✅ Margini unitari calcolati│         │     reali di vendita        │
│                             │         │                             │
└─────────────────────────────┘         └─────────────────────────────┘
```

### Day-by-Day Checklist

| Day | Task | Chi |
|---|---|---|
| 1 | Deploy Cloudflare Worker IPN (codice pronto sopra) | Hermes |
| 1 | Creare Google Sheet "Orders" con template colonne | Hermes |
| 1 | Deploy Google Apps Script Web App | Hermes |
| 1 | Configurare PayPal IPN → URL Worker | Hermes |
| 2 | Preparare folder template email customer care | Agente 2 |
| 2 | Scrivere politica resi intelligente | Agente 2 → CEO approva |
| 3 | Test end-to-end: ordine PayPal → Worker → Sheet → operatore vede riga | Hermes |
| 4 | Correggere eventuali bug nel flusso | Hermes |
| 5 | Primo giro di commenti Reddit (valore puro, no link) | Agente 5 |
| 5-7 | Monitorare che non arrivino ordini da zone non mainland | Agente 1 |
| 8 | Creare 3 board Pinterest | Agente 5 |
| 8-14 | 3-5 pin/giorno manuali | Agente 5 |
| 8-14 | Richiedere foto CJ Dropshipping | Agente 3 |
| 10 | Audit SEO completo di tutte le pagine | Agente 4 |
| 12 | Scrivere e pubblicare blog post #1 | Agente 4 |
| 15 | Primo report vendite (quanti ordini, da dove) | Agente 6 |
| 15-21 | Continuare Reddit + Pinterest (diventa routine) | Agente 5 |
| 22 | Calcolare margini reali vs stimati | Agente 6 |
| 22 | Aggiornare buffer fiscale (quanto manca ai $4k?) | Agente 6 |
| 28-30 | Report 30 giorni a CEO (Hermes) con decisioni Fase 2 | Tutti |

---

## 8. Monitoraggio Finanziario e Fonti di Traffico

### 8.1 Google Sheet — Finance Tracker

Secondo foglio nello stesso Google Sheet, tab "Finance":

| A | B | C | D | E | F | G | H | I |
|---|---|---|---|---|---|---|---|---|
| Week | Revenue | PayPal Fees (2.99%+$0.49) | CJ Cost | Shipping Cost | Net | Buffer Running Total | Source Attribution | Notes |

**Source Attribution** (colonna H) — compilata manualmente ogni settimana chiedendo ai clienti via email:
> "Quick question — where did you first hear about Nobleparc?"  
> (Reddit / Pinterest / Google / Friend / Other)

Oppure Cloudflare Analytics mostra il referrer header per ogni acquisto (sezione Analytics → Web Analytics, gratis).

### 8.2 Dashboard Sintetico (Hermes visualizza ogni 7 giorni)

```
Nobleparc — Weekly Snapshot (Week N)
─────────────────────────────────────
Orders:        12
Revenue:       $828
PayPal Fees:   $28.73
CJ Costs:      $276
Net Revenue:   $523.27
Buffer Total:  $1,847.50  (target: $4,000-5,000)

Source Mix:
  Reddit:      5 (42%)
  Pinterest:   4 (33%)
  Google:      2 (17%)
  Direct:      1 (8%)

Margins:
  Mask:        74.3%
  Massager:    73.1%
```

### 8.3 Regole per Hermes CEO

- **Se buffer < $4,000:** nessuna Partita IVA, nessun collegamento Stripe. PayPal continua.
- **Se chargeback rate > 1%:** attivare revisione indirizzi di spedizione e triggerare escalation.
- **Se margine netto < 35%:** rivedere CJ cost o prezzo di vendita.
- **Se traffico Reddit > 60% per 3 settimane consecutive:** attivare Pinterest come priority #1 (diversificazione).
- **Se Pinterest porta < 10% del traffico dopo 4 settimane:** rivalutare strategia visuale (foto non abbastanza aspirazionali).

---

## Appendice: Codice Pronto per Cloudflare Worker

```javascript
// File: cloudflare-worker.js
// Deploy: npx wrangler deploy cloudflare-worker.js --name nobleparc-ipn

const SHEET_SCRIPT_URL = 'https://script.google.com/macros/s/YOUR_SCRIPT_ID/exec'
const PAYPAL_BUSINESS_EMAIL = 'info@nobleparc.com'
const INVALID_STATES = ['HI', 'AK', 'PR', 'GU', 'VI', 'AS', 'MP']

export default {
  async fetch(request) {
    if (request.method !== 'POST') return new Response('OK', { status: 200 })
    
    try {
      const formData = await request.formData()
      const status = formData.get('payment_status')
      const receiver = formData.get('receiver_email')
      
      if (status !== 'Completed' || receiver !== PAYPAL_BUSINESS_EMAIL) {
        return new Response('OK', { status: 200 })
      }
      
      const state = formData.get('address_state') || ''
      const isMainland = !INVALID_STATES.includes(state)
      
      if (!isMainland) {
        // Non rimborsiamo automaticamente; segnaliamo per review umana
        // ma registriamo lo stesso sul sheet con flag
      }
      
      const order = {
        date: new Date().toISOString().split('T')[0],
        customer_name: `${formData.get('first_name') || ''} ${formData.get('last_name') || ''}`.trim(),
        customer_email: formData.get('payer_email'),
        product: formData.get('item_name'),
        price: formData.get('mc_gross'),
        paypal_txn: formData.get('txn_id'),
        shipping: `${formData.get('address_street') || ''}, ${formData.get('address_city') || ''}, ${state} ${formData.get('address_zip') || ''}`,
        state: state,
        status: isMainland ? '🟡 Payment received' : '🟡 NON-MAINLAND - review',
        notes: isMainland ? '' : '⚠️ Outside continental US — manual review required'
      }
      
      await fetch(SHEET_SCRIPT_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(order)
      })
      
      return new Response('OK', { status: 200 })
    } catch (err) {
      // Log to Cloudflare dashboard
      console.error('IPN error:', err)
      return new Response('OK', { status: 200 })
    }
  }
}
```

---

*Documento operativo — Nobleparc Operations Playbook*  
*Hermes (CEO) · Target: $6k+/mo organic revenue · Zero fixed costs*