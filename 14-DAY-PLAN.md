# Nobleparc — Primi 14 Giorni: Piano Operativo Dettagliato

**Responsabilità:** Hermes (CEO) supervisiona tutto. Ogni task ha un responsabile unico.

---

## Giorno 1 — Fondamenta

| Task | Chi | Output | Durata |
|------|-----|--------|--------|
| Creare Google Sheet con colonne esatte (A–AD) | Hermes | Sheet `Nobleparc – Orders Control` pronto | 15 min |
| Deploy Cloudflare Worker (npx wrangler deploy) | Hermes | Worker live su `nobleparc-ipn.*.workers.dev` | 10 min |
| Deploy Google Apps Script (Web App) | Hermes | Endpoint HTTPS che scrive sul Sheet | 10 min |
| Configurare PayPal IPN → URL Worker | Hermes | PayPal Dashboard → Notifications → IPN | 5 min |
| Testare il flusso con un ordine PayPal sandbox | Hermes | Riga 🟡 "Bozza" compare sul foglio | 15 min |
| Scrivere template email customer care | Agente 2 | 4 template + 1 traffic source | 20 min |

**Totale giorno 1:** ~75 minuti

---

## Giorno 2 — Validazione e Controllo

| Task | Chi | Output |
|------|-----|--------|
| Verificare che il filtro mainland (L) funzioni | Agente 1 | Test con ZIP di HI e AK → L = BLOCKED |
| Impostare conditional formatting sul foglio | Agente 1 | Colonna S: verde se >0, rosso se <0 |
| Impostare dropdown validation (T, U, L, AA, AB) | Agente 1 | Tutte le colonne con scelte chiuse |
| Preparare cartella Gmail con etichette "Nobleparc Orders" | Agente 2 | Filtro automatico per email da PayPal |
| Verificare che tutti i link del sito funzionino | Agente 4 | Audit rapido: homepage → prodotti → checkout |

---

## Giorno 3 — Primo Ordine Reale

| Task | Chi | Output |
|------|-----|--------|
| Eseguire un ordine di prova reale ($1 su PayPal) | Hermes | Riga completa sul foglio |
| Seguire il flusso end-to-end: Sheet → CJ → Tracking | Agente 1 | Processo documentato e testato |
| Inviare il primo template di conferma a un'email di test | Agente 2 | Template funzionante |
| Verificare che il tracking arrivi al cliente | Agente 1 | Chiusura del ciclo |

---

## Giorno 4 — Reddit: Primi Commenti

| Task | Chi | Output |
|------|-----|--------|
| Leggere 10 thread su r/redlighttherapy | Agente 5 | Capire tono e domande frequenti |
| Rispondere a 3 thread con valore, senza menzionare Nobleparc | Agente 5 | Credibilità costruita |
| Segnare su Notes personali quali domande si ripetono | Agente 5 | Input per nuove FAQ |

---

## Giorno 5 — Pinterest: Setup

| Task | Chi | Output |
|------|-----|--------|
| Creare 3 board: "Home Wellness Rituals", "LED Light Therapy at Home", "Self-Care Evening Routine" | Agente 5 | Board pronte |
| Caricare 5 pin con immagini prodotto (o placeholder decorosi) | Agente 5 | Prime 5 schede |
| Scrivere descrizioni SEO per ogni pin (con keyword) | Agente 5 | Testo ottimizzato |

**Regola Pinterest:** 3-5 pin/giorno, manuali, niente scheduler a pagamento.

---

## Giorno 6 — Customer Care: Primo Contatto

| Task | Chi | Output |
|------|-----|--------|
| Inviare l'email "Traffic Source" a tutti i clienti esistenti | Agente 2 | Prime risposte raccolte |
| Preparare template per risposte rapide (frasi pronte) | Agente 2 | Velocità di risposta < 4 ore |

---

## Giorno 7 — Revisione Settimanale #1

| Task | Chi | Output |
|------|-----|--------|
| Quanti ordini? | Agente 6 | Report 1 riga |
| Quanto margine netto? | Agente 6 | Selling Price - PayPal Fee - CJ Cost |
| Da dove arriva il traffico? | Agente 6 | AB (Traffic Source) compilata |
| Problemi emersi? | Tutti | Lista priorità per settimana 2 |

---

## Giorno 8 — Foto Prodotti

| Task | Chi | Output |
|------|-----|--------|
| Cercare foto stock royalty-free (Unsplash, Pexels) | Agente 3 | 2-3 foto per prodotto |
| Oppure: generare immagini AI realistiche (Bing Image Creator, free) | Agente 3 | 2-3 foto per prodotto |
| Oppure: richiedere foto reali al fornitore CJ | Agente 3 | (attesa — può richiedere giorni) |
| Convertire foto in WebP srcset con pipeline CLI | Agente 3 | `convert` + `libwebp` |
| Sostituire placeholder SVG sul sito | Agente 3 | Commit + push |

---

## Giorno 9 — SEO Audit Completo

| Task | Chi | Output |
|------|-----|--------|
| Verificare ogni pagina title (50-60 char) | Agente 4 | Lista correzioni |
| Verificare ogni meta description (120-160 char) | Agente 4 | Lista correzioni |
| Verificare H1 unico per pagina | Agente 4 | ✅ già presente |
| Verificare immagini alt text | Agente 4 | ✅ già presente |
| Testare schema JSON-LD su validator.schema.org | Agente 4 | Report |
| Aggiungere internal link tra pagine prodotto nelle FAQ | Agente 4 | "Pairs well with..." |

---

## Giorno 10 — Reddit: Solution-Drop

| Task | Chi | Output |
|------|-----|--------|
| Rispondere a 5 thread su r/redlighttherapy e r/30PlusSkinCare | Agente 5 | Valore, non spam |
| In 1-2 risposte, menzionare "I use a Nobleparc mask" se contestuale | Agente 5 | Prima menzione brand |
| Mai: link diretto, "use code", "check out my store" | Agente 5 | Zero violazioni |

---

## Giorno 11 — Pinterest: Mantenere

| Task | Chi | Output |
|------|-----|--------|
| 5 nuovi pin (3 su board esistenti, 2 nuovi) | Agente 5 | Board in crescita |
| Interagire con altri pin simili (repin) | Agente 5 | Visibilità |

---

## Giorno 12 — Blog Post #1

| Task | Chi | Output |
|------|-----|--------|
| Scrivere: "What Is Red Light Therapy? A Beginner's Guide for Home Wellness" | Agente 4 | 800-1000 parole |
| Includere: cos'è, come funziona, 3 benefici (wellness language), come usarlo a casa | Agente 4 | Nessun claim medico |
| Pubblicare su `/blog/` (creare struttura Hugo) | Agente 4 | Nuova pagina |
| Aggiornare sitemap.xml | Agente 4 | Automatico con Hugo |

---

## Giorno 13 — Finance Review

| Task | Chi | Output |
|------|-----|--------|
| Inserire tutti i costi CJ reali nel foglio (colonne P, Q) | Agente 6 | Margini reali visibili |
| Calcolare PayPal fee reali (colonna O) | Agente 6 | Automatico con formula |
| Compilare AB (Traffic Source) per ogni ordine | Agente 6 | Prima attribuzione |
| Verificare che il buffer fiscale sia tracciato | Agente 6 | Quanto manca ai $4k? |

---

## Giorno 14 — Report 2 Settimane a CEO

| Task | Chi | Output |
|------|-----|--------|
| Quanti ordini ricevuti? | Agente 6 | Numero |
| Quanto margine netto generato? | Agente 6 | $$ |
| Quanto buffer accumulato? | Agente 6 | $$ (target $4k) |
| Da dove arriva il traffico? (top 3 fonti) | Agente 6 | % |
| Problemi aperti? | Tutti | Lista |
| Decisioni per settimana 3-4 | Hermes | GO / NO GO su TikTok, Instagram, Blog |

---

## Riepilogo: Chi Fa Cosa (Giorni 1-14)

| Agente | Giorni attivi | Compiti principali |
|--------|---------------|-------------------|
| **Hermes (CEO)** | 1-14 | Supervisione, decisioni, deploy Worker/Sheet, approvazione spese |
| **Agente 1 (Operations)** | 1-14 | Foglio, validazione ordini, CJ, tracking, conditional formatting |
| **Agente 2 (Customer Care)** | 2-14 | Template email, risposte clienti, traffic source email |
| **Agente 3 (Content Studio)** | 8-14 | Foto stock/AI, pipeline WebP, sostituzione placeholder |
| **Agente 4 (SEO/AEO)** | 2-14 | Audit SEO, blog post #1, schema validation, internal links |
| **Agente 5 (Organic Growth)** | 4-14 | Reddit (solution-drop), Pinterest (3-5 pin/giorno) |
| **Agente 6 (Finance/Intel)** | 7-14 | Margini, fee, buffer, report settimanale |