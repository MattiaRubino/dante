# LifeOS — Today v15

## Scopo

Correzione delle regressioni emerse dopo Today v14 nella timeline principale.

## Correzioni

### Drag temporale

- Il drag non modifica più automaticamente il gruppo/categoria in base alla posizione orizzontale di rilascio.
- Il gesto aggiorna soltanto l'orario, con snap a 15 minuti e durata invariata.
- Il movimento orizzontale rimane una risposta visiva durante il trascinamento, ma non viene persistito.
- Ghost e annullamento restano disponibili.

### Riordino gruppi

- Il riordino della barra superiore aggiorna le colonne nella vista espansa.
- Lo stesso ordine influenza ora anche l'ancoraggio orizzontale delle card nella vista compatta.
- La compatta usa un bias controllato: non diventa una griglia rigida e le card restano leggibili.

### Focus contestuale

- Secondo clic sullo stesso blocco: focus annullato.
- Clic nello spazio vuoto della timeline: focus annullato.
- Il comportamento funziona anche sui blocchi piccoli.
- Titolo e controllo sotto-attività conservano le proprie azioni dedicate.

### Densità

- La scala verticale viene calcolata su tutti gli elementi del giorno, non soltanto su quelli rimasti visibili dopo un filtro.
- Attivare un filtro non comprime più la timeline.
- Una giornata densa mantiene la stessa leggibilità prima e dopo il filtro.

### Card adattive

- Aumentata la larghezza minima delle colonne espanse.
- Contenuti semplificati soltanto quando la card è davvero stretta.
- Con un solo gruppo filtrato, gli elementi usano lo spazio disponibile invece di restare compressi nella vecchia colonna globale.
- La scrollbar orizzontale resta il meccanismo previsto quando più gruppi superano lo spazio.

## Test

- Nessun errore JavaScript runtime.
- 22 blocchi renderizzati.
- Altezza della giornata invariata prima/dopo filtro.
- Filtro singolo in vista espansa: card larghe.
- Focus selezionabile e deselezionabile.
- Reset tramite area vuota.
- Riordino gruppi visibile anche in compatta.
- Drag con categoria invariata.

## Artefatti locali

- `LifeOS_Home_Oggi_v15_canvas.html`
- `LifeOS_Fase_4_frontend_master_v15.md`

## Limiti residui

- Il drag resta confinato allo stesso giorno.
- Il movimento orizzontale non viene salvato come posizione libera.
- Ordine gruppi e spostamenti non sono ancora persistiti su backend/local storage.
- La formula finale della densità dovrà essere estratta dal prototipo e testata con dataset più estremi.
