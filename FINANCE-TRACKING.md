# Nobleparc — Finance & Intelligence Agent: Tracciamento Operativo

## Formula Margine (UFFICIALE — invariabile)

```
Margin = Total Paid (N) – PayPal Fee (O) – Supplier Cost (P) – Shipping Cost (Q)

Colonna S = N - O - (P + Q)
```

**Regole:**
- **PayPal Fee (O):** 2.99% + $0.49 per transazione — formula `=N*0.0299+0.49`
- **Product Cost (P):** costo del prodotto da CJ Dropshipping, inserito manualmente dall'operatore
- **Shipping Cost (Q):** costo di spedizione da CJ, **mai dato per scontato**. Verificare su CJ Dropshipping per ogni ordine. Non è sempre incluso nel wholesale price.
- **Total Cost (R):** `=P+Q`
- **Margin (S):** `=N-O-R`

**Esempio con verifica shipping reale:**
```
Mask:
  Selling Price:    $69.00
  PayPal Fee:       -$2.55
  Product Cost:     -$15.00
  Shipping Cost:    -$0.00  (se incluso in CJ)
  Margin:           $51.45  (74.6%)

  Se shipping non incluso:    $69 - $2.55 - $15.00 - $4.50 = $46.95 (68.0%)
```

---

## Ogni ordine genera automaticamente

| Colonna | Dato | Come |
|---------|------|------|
| N | Selling Price | Scritto dal Worker da PayPal |
| O | PayPal Fee | Formula automatica `=N*0.0299+0.49` |
| P | Product Cost | Inserito da operatore dopo ordine CJ |
| Q | Shipping Cost | Inserito da operatore (verificato su CJ) |
| R | Total Cost | Formula `=P+Q` |
| S | Margin | Formula `=N-O-R` |

L'operatore inserisce **solo** P e Q (Product Cost + Shipping Cost).  
Tutto il resto è automatico.

---

## Report Settimanale (15 minuti ogni 7 giorni)

A Giorno 7, 14, 21, 28 l'Agente 6 compila:

```
Nobleparc — Weekly Snapshot (Week N)
─────────────────────────────────────

1. ORDERS
   Orders received:    12
   Orders fulfilled:   10
   Orders refunded:    1
   Refund rate:        8.3%  (target: <5%)

2. REVENUE & MARGINS
   Gross revenue:      $828.00
   PayPal fees:        -$28.73
   CJ costs:           -$276.00
   Net revenue:        $523.27
   Net margin:         63.2%

   Per product:
     Mask:             $69 → $51.45 net (74.6% margin)
     Massager:         $39 → $29.34 net (75.2% margin)

3. BUFFER FISCALE
   Running total:      $1,847.50
   Target:             $4,000.00
   Remaining:          $2,152.50
   Pace:               ~$1,850/week → target in ~2.3 weeks

4. TRAFFIC SOURCES (colonna AB)
   Reddit:             5 (42%)
   Pinterest:          4 (33%)
   Google:             2 (17%)
   Direct:             1 (8%)
   Other:              0 (0%)

5. ISSUES
   Open tickets:       2
   Chargebacks:        0
   Non-mainland:       1 (refunded)
```

---

## Come si ottengono i dati (esattamente)

| Dato | Da dove? | Come? |
|------|----------|-------|
| Orders | Sheet, colonna A | Contare righe con data nella settimana |
| Refund rate | Colonna T = "Rimborsato" | Filtro sul foglio |
| Gross revenue | Colonna N | Somma della settimana |
| PayPal fees | Colonna O | Formula automatica, somma |
| CJ costs | Colonna P | Inserito da operatore, somma |
| Shipping costs | Colonna Q | Inserito da operatore, somma |
| Buffer running total | Somma colonna S di tutte le settimane | Accumulato |
| Traffic sources | Colonna AB | Filtro per valore |
| Open tickets | Email support@nobleparc.com | Contare email non archiviate |

---

## Regole di Decisione (per Hermes CEO)

| Se | Allora |
|----|--------|
| Buffer < $4,000 | Nessuna Partita IVA, nessun collegamento Stripe. PayPal resta. |
| Refund rate > 5% | Revisione della qualità prodotto o del fornitore. |
| Chargeback rate > 1% | Attivare escalation: rimborsare proattivamente tutti i clienti insoddisfatti. |
| Net margin < 35% | Rivedere CJ cost o prezzo di vendita. |
| Shipping cost non verificato | Bloccare l'ordine fino a verifica su CJ. |
| Una fonte di traffico > 60% per 3 settimane | Diversificare: attivare il canale successivo della sequenza. |
| Pinterest < 10% dopo 4 settimane | Rivalutare qualità visiva delle immagini. |

---

## Template Report per Hermes (da inviare ogni 7 giorni)

```
Agente 6 → Hermes (CEO)

Week N report ready.

  Orders:     [N]
  Net:        $[N]
  Buffer:     $[N] / $4,000
  Top source: [Source] ([N]%)
  Issues:     [N] open

Ready for your review.
```