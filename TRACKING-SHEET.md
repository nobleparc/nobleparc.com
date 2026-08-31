# Nobleparc — Orders Control Sheet

**Nome foglio:** `Nobleparc – Orders Control`  
**Link:** `https://docs.google.com/spreadsheets/d/YOUR_SHEET_ID/edit`

## Colonne (A–AD, esatte dalla specifica)

| Col | Nome colonna | Tipo | Esempio / Formula |
|-----|-------------|------|-------------------|
| A | Order ID | Testo | NP-20260901-001 |
| B | Date | Testo (YYYY-MM-DD HH:MM) | 2026-09-01 14:23 |
| C | PayPal Transaction ID | Testo | 9PA12345ABCD67890 |
| D | Customer Name | Testo | Jessica Thompson |
| E | Email | Testo | jessica@example.com |
| F | Phone | Testo | +1 555 123 4567 |
| G | Address Line 1 | Testo | 742 Evergreen Terrace |
| H | Address Line 2 | Testo (opzionale) | Apt 4B |
| I | City | Testo | Portland |
| J | State | Testo (2 lettere) | OR |
| K | ZIP | Testo (5-9 digit) | 97201 |
| L | Mainland Check | `OK` / `BLOCKED` | OK |
| M | Product | Testo | Red Light Mask |
| N | Selling Price | Numero (USD) | 69.00 |
| O | PayPal Fee | Formula | `=N2*0.0299+0.49` |
| P | Product Cost | Numero (USD) | 15.00 |
| Q | Shipping Cost | Numero (USD) | 0.00 |
| R | Total Cost | Formula | `=P2+Q2` |
| S | Margin | Formula | `=N2-O2-R2` |
| T | Status | Dropdown | Bozza |
| U | Human Validation | Dropdown | Pending |
| V | Validated By | Testo | (operatore) |
| W | Validation Date | Data | 2026-09-01 |
| X | CJ Order ID | Testo | CJ-98765 |
| Y | Tracking Number | Testo | 1Z999AA10123456784 |
| Z | Carrier | Testo | USPS |
| AA | Blind Note Added | `Yes` / `No` | Yes |
| AB | Traffic Source | Dropdown | Reddit |
| AC | Notes | Testo | Cliente ha chiesto... |
| AD | Last Update | Formula | `=IF(B2<>"",NOW(),"")` |

## Dropdown Validation

| Colonna | Valori |
|---------|--------|
| L (Mainland Check) | `OK`, `BLOCKED` |
| T (Status) | `Bozza`, `Validato`, `Ordinato su CJ`, `Spedito`, `Consegnato`, `Rimborsato`, `Problema` |
| U (Human Validation) | `Pending`, `Approved`, `Rejected` |
| AA (Blind Note Added) | `Yes`, `No` |
| AB (Traffic Source) | `Reddit`, `Pinterest`, `Google`, `Direct`, `Other` |

## Formula Margine (ufficiale, invariabile)

```
Margin = Selling Price – PayPal Fee – (Product Cost + Shipping Cost)

Colonna S = N - O - R
dove R = P + Q
```

PayPal Fee = 2.99% + $0.49 per transazione USA.  
I costi di spedizione CJ non sono mai dati per scontati — vanno verificati su CJ Dropshipping per ogni ordine e inseriti manualmente in colonna Q.

## Istruzioni Creazione (5 minuti)

1. **https://sheets.new** → rinomina in `Nobleparc – Orders Control`
2. Copia la riga intestazione in **fila 1** (A–AD)
3. **View → Freeze → 1 row**
4. Imposta le formule:
   - O2: `=N2*0.0299+0.49`
   - R2: `=P2+Q2`
   - S2: `=N2-O2-R2`
   - AD2: `=IF(B2<>"",NOW(),"")`
   — Poi seleziona O2:R2, tira giù per tutta la colonna
5. **Data → Data validation** per colonne L, T, U, AA, AB
6. **Format → Conditional formatting** per colonna S:
   - S > 0 → sfondo verde
   - S < 0 → sfondo rosso