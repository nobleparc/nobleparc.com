# Nobleparc — Finance & Intelligence Agent: Tracciamento Operativo

## Come funziona nella pratica (non teoria)

### Ogni ordine genera automaticamente:

```
Colonna N (Selling Price):  $69.00  ← lo scrive il Worker da PayPal
Colonna O (PayPal Fee):      $2.55  ← =N2*0.0299+0.49 (formula)
Colonna P (Product Cost):    $15.00 ← lo inserisce l'operatore quando ordina da CJ
Colonna Q (Shipping Cost):   $0.00  ← lo inserisce l'operatore
Colonna R (Total Cost):      $15.00 ← =P2+Q2 (formula)
Colonna S (Margin):          $51.45 ← =N2-O2-R2 (formula)
```

**L'operatore** inserisce solo P e Q (CJ cost + shipping) dopo aver ordinato da CJ.  
Tutto il resto è automatico o dropdown.

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
| Buffer running total | Foglio Finance separato | Somma Net di tutte le settimane |
| Traffic sources | Colonna AB | Filtro per valore |
| Open tickets | Email support@nobleparc.com | Contare email non archiviate |

---

## Foglio Finance (secondo tab nello stesso Sheet)

Oltre al tab `Nobleparc – Orders Control`, esiste un tab **Finance** con:

| A | B | C | D | E | F | G | H |
|---|---|---|---|---|---|---|---|
| Week | Orders | Gross Revenue | PayPal Fees | CJ Costs | Net Revenue | Net Margin % | Buffer Running Total |

Questo tab viene aggiornato **ogni 7 giorni** dall'Agente 6 con i dati aggregati.  
Una riga per settimana. Alla fine del mese, 4 righe.

---

## Regole di Decisione (per Hermes CEO)

| Se | Allora |
|----|--------|
| Buffer < $4,000 | Nessuna Partita IVA, nessun collegamento Stripe. PayPal resta. |
| Refund rate > 5% | Revisione della qualità prodotto o del fornitore. |
| Chargeback rate > 1% | Attivare escalation: rimborsare proattivamente tutti i clienti insoddisfatti. |
| Net margin < 35% | Rivedere CJ cost o prezzo di vendita. |
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