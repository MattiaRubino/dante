# LifeOS — Home/Today v16

## Scopo

La v16 è una milestone di stabilizzazione del trascinamento. Non introduce nuove funzioni di prodotto: corregge conflitti tra click, popup, focus contestuale e spostamento, e rende possibile lo spostamento tra giorni della vista continua.

## Interazioni consolidate

### Zone della card

- click sul solo titolo: apre il popup di dettaglio;
- click sul comando sotto-attività: espande/richiude;
- click sul resto della card senza movimento: attiva/disattiva il focus contestuale;
- trascinamento sul resto della card oltre 7 px: avvia il drag;
- il cursore resta normale.

### Stato del drag

Macchina a stati:

```text
idle → pressed → dragging → dropped
                  └──────→ cancelled
```

Durante `pressed` non viene aperto né spostato nulla. Solo il superamento della soglia di 7 px attiva il trascinamento.

### Overlay e segnaposto

- la card originale resta nella posizione iniziale, attenuata;
- una copia `position: fixed` segue il puntatore sopra l'interfaccia;
- forma, dimensione e contenuti restano coerenti;
- appare solo una piccola pillola con giorno e nuovo orario;
- la scritta invasiva `Esc annulla` è stata rimossa;
- `Esc` continua ad annullare silenziosamente.

### Auto-scroll e spostamento tra giorni

- entrando nella fascia di 76 px vicino al bordo alto/basso parte l'auto-scroll;
- la velocità aumenta progressivamente avvicinandosi al bordo;
- durante il drag viene disabilitato lo `scroll-behavior: smooth`, che impediva lo scorrimento continuo;
- vengono resi disponibili i 14 giorni della finestra Today;
- il blocco può essere spostato tra i giorni caricati;
- la categoria non cambia durante lo spostamento;
- durata e snap a 15 minuti restano invariati.

### Drop e annullamento

- drop valido: salva giorno, ora iniziale e ora finale;
- drop non valido: nessuna modifica;
- dopo il drop compare un toast breve con `Annulla`;
- l'undo ripristina giorno e orario precedenti;
- il DOM viene ricostruito una sola volta dopo il drop, mai durante `pointermove`.

## Correzioni tecniche principali

- `timeOverrides` ora supporta `{dateKey, start, end}`;
- gli eventi spostati vengono esclusi dal giorno originale e inclusi nel giorno destinazione;
- aggiunto lookup dell'evento originale per preservarne metadati e categoria;
- `dayMeta` conserva anche il mapper temporale per convertire coordinate verticali in minuti;
- l'auto-scroll usa un timer stabile e velocità dipendente dalla distanza dal bordo;
- click sintetici dopo il drag vengono soppressi per evitare popup/focus involontari.

## Test di regressione eseguiti

- rendering iniziale: 22 blocchi, 4 giorni iniziali;
- nessun errore JavaScript;
- click sul titolo apre il popup;
- click sul corpo attiva e disattiva il focus contestuale;
- drag dal corpo non apre il popup;
- overlay presente durante il drag;
- toast presente dopo il drop;
- auto-scroll attivo vicino al bordo;
- caricamento fino a 14 giorni durante il drag;
- spostamento verificato da Oggi a Domani;
- categoria invariata;
- annullamento da toast preservato.

## Non regressioni da mantenere

- densità dinamica basata su tutti gli eventi del giorno;
- card adattive;
- filtri non devono comprimere la scala temporale;
- riordino gruppi sincronizzato con il layout;
- sotto-attività e popup funzionanti;
- espansione compatta/gruppi invariata;
- percorso dell'omino e asse ambientale invariati.

## Limiti ancora aperti

- il prototipo usa codice standalone; in produzione il drag and drop dovrà essere implementato con una libreria robusta e accessibile;
- resta da progettare l'alternativa completa da tastiera/screen reader;
- collisioni, vincoli di viaggio e conseguenze AI sono fuori da questa milestone;
- il caricamento dei 14 giorni durante il drag è accettabile per il prototipo, ma in produzione servirà virtualizzazione.
