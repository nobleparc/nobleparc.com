# Nobleparc — Mainland USA Filter (Logica Tecnica)

## Livello 1: Cloudflare Worker (automatico, real-time)

Il Worker PayPal IPN riceve il parametro `address_state_code` dalla notifica PayPal.  
Esegue questo controllo prima ancora di scrivere sul foglio:

```javascript
const INVALID_STATES = ['HI', 'AK', 'PR', 'GU', 'VI', 'AS', 'MP']
const ALLOWED_COUNTRY = 'US'

const isMainland = (country === ALLOWED_COUNTRY && !INVALID_STATES.includes(state))
```

**Risultato sulla riga del foglio:**
- Colonna L (Mainland Check): `OK` o `BLOCKED`
- Colonna AC (Notes): se BLOCKED, aggiunge testo `"⚠️ Outside continental US — manual review required"`

**Nessun rimborso automatico.** Il Worker segnala ma non agisce — la decisione finale è sempre umana.

## Livello 2: Condizionale nel foglio (visivo, per l'operatore)

Nella colonna **S (Margin)**, se L = `BLOCKED`, la cella si colora automaticamente di rosso (conditional formatting).  
L'operatore vede immediatamente: "fermo, da gestire".

## Livello 3: Protocollo umano (quando L = BLOCKED)

1. L'operatore legge la riga e controlla l'indirizzo
2. Se è un errore di PayPal (es. HI ma ZIP è CA) → override manuale, L → OK
3. Se è veramente fuori mainland (es. AK, PR) → due opzioni:
   - **Opzione A (default):** Rimborso. Template "Refund — ships to US mainland only".  
     Colonna T → "Rimborsato", colonna U → "Approved", nota il motivo.
   - **Opzione B (eccezione, solo con approvazione CEO):** Spedire lo stesso, il cliente paga la differenza di shipping.

## Livello 4: Aggiunta frontend (Fase 2, non urgente)

Aggiungere un avviso nel checkout PayPal prima del pagamento.  
PayPal permette di configurare un **messaggio di avviso** nella pagina di pagamento tramite le impostazioni del pulsante o dell'IPN.  
Per ora, la politica è già scritta in:
- Pagina Shipping & Returns
- FAQ
- Confirmation page

Questo copre il 99% dei casi prima che qualcuno provi ad acquistare da una zona non coperta.