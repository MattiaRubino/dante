# B14 + B07 — consolidamento prodotto e UI guidato dall'uso

- **Stato:** ATTIVO — direzione e priorità fornite dall'utente durante l'uso dell'app
- **Avvio:** 2026-09-30
- **Branch:** `feature/timeline-temporal-operational`
- **Base:** B00–B13 e B12 chiusi; frontiera di persistenza `20260929_93`
- **Fonte della lista viva:** questo documento, Roadmap, Map e Handoff
- **CI:** non usata; i test locali sono eseguiti dall'utente

## Obiettivo

Rendere Home e Timeline utilizzabili come prodotto: creare, trovare, capire e gestire ogni capacità già implementata senza dover conoscere il lessico interno, copiare identificativi o ricostruire passaggi nascosti.

Il lavoro include la completezza del Create di B14 e il consolidamento UI/UX di B07 nello stesso ciclo. B07 resta un identificatore storico: non attende più una seconda fase dopo B14.

## Metodo di lavoro

L'utente fornisce decisioni concrete durante l'uso: cosa mantenere, rimuovere, aggiungere, spostare, raggruppare o far funzionare in modo diverso. Ogni decisione viene trattata come una voce della lista viva, senza creare sottoblocchi artificiali.

Per ogni voce:

1. registrare il comportamento attuale e quello desiderato;
2. controllare il confine Domain, persistence, API e frontend che la voce tocca;
3. modificare UI, comportamento e regole necessarie come un'unica consegna;
4. aggiornare test mirati e documentazione coinvolta;
5. segnare l'esito qui e pubblicare il checkpoint sul branch.

Le voci possono essere lavorate singolarmente oppure in un gruppo quando condividono la stessa schermata, modello o flusso. La scelta avviene in base a ciò che l'utente decide mentre usa il prodotto.

## Regole permanenti

- Nessun controllo editabile resta visibile se il suo valore non è salvato e applicato, è chiaramente di sola lettura, oppure indirizza a un flusso che lo possiede davvero.
- La UI può cambiare completamente; le distinzioni canoniche restano esplicite: Activity, Event, Routine, Recurrence, Occurrence, Schedule, Session, Actual, Outcome, Confirmation, Plan, Step e Dependency non vengono fuse per comodità visiva.
- Uno spostamento di Schedule, una proposta e un fatto avvenuto restano azioni diverse anche quando sono presentate nello stesso spazio dell'interfaccia.
- Quando una scelta richiede una nuova regola o persistenza, la si implementa nel livello proprietario e si aggiorna API, client e test se esposti pubblicamente.
- Le migrazioni pubblicate restano immutabili; una correzione dati è sempre forward-only.

## Lista viva

| Voce | Decisione dell'utente | Stato | Evidenza / note |
|---|---|---|---|
| U0 | Inventario delle capacità create e gestibili preparato; l'utente definisce ora flussi e collocazione della UI. | pronto | inventario discusso il 2026-09-30 |
| U1 | Rivedere l'ingresso `+`: chiusura senza bozza, posizione e forma del pannello di Create, rapporto con il calendario e necessità di un comando Crea separato. | in discussione | stato attuale: pannello fisso in alto a sinistra, click esterno non gestito, ancoraggio del punto d'ingresso non usato |

La prima decisione dell'utente apre la voce `U1`. Le righe successive descrivono la scelta concreta, i file o confini coinvolti e il test locale richiesto prima di dichiararla conclusa.

## Chiusura

B14/B07 chiude quando l'utente considera coerenti i flussi principali e l'inventario non contiene più comandi inutili, nascosti dietro passaggi tecnici o privi di comportamento reale. B15 conserva il controllo verticale finale su persistenza, catalogo, API, client, frontend e regressioni.

