# LifeOS — Fase 4: prototipo Home/Today v7

- **Stato:** prototipo frontend interattivo
- **Data di riferimento:** 4 agosto 2026
- **Branch:** `prototype/phase-4-today-home`
- **Artefatto principale:** `prototypes/today/lifeos-home-oggi-v7.html`
- **Scopo:** validare la superficie principale `Today` prima di trasformarla in componenti React/Next.js

## 1. Ruolo della Home/Today

La Home/Today è il cuore operativo di LifeOS. Deve permettere all’utente di:

- capire rapidamente la giornata;
- vedere eventi, attività, routine e passi di programma;
- gestire sovrapposizioni e giornate molto dense;
- approfondire un elemento senza perdere il contesto temporale;
- passare da una vista unificata a una distribuzione per gruppi;
- reagire ai cambiamenti e consultare suggerimenti contestuali;
- scorrere nei giorni successivi senza aprire subito il calendario completo.

Il prototipo non deve essere letto come codice di produzione. È una superficie di validazione UX con dati simulati.

## 2. Struttura della schermata

La versione v7 comprende:

1. sidebar principale;
2. header con saluto, data, ricerca/comando globale e azioni rapide;
3. striscia settimanale cliccabile;
4. timeline centrale;
5. asse orario con contesto ambientale;
6. rail destro con obiettivi e priorità;
7. dettaglio elemento in popup;
8. espansione locale delle sotto-attività;
9. espansione orizzontale per gruppi;
10. scorrimento progressivo tra giornate.

### Vincolo di layout

La timeline compatta non deve occupare tutta la larghezza disponibile senza motivo. Deve lasciare una riserva a destra per:

- rail attuale;
- moduli futuri;
- espansione orizzontale;
- contenuti contestuali aggiuntivi.

Il rail destro rimane visibile quando lo spazio lo consente e si riduce soltanto se l’espansione richiede realmente larghezza aggiuntiva.

## 3. Asse orario e contesto ambientale

L’asse orario può integrare:

- notte;
- alba;
- giorno;
- tramonto;
- sera;
- temperatura;
- fase lunare.

Questa scelta ha due obiettivi:

- rendere la timeline più riconoscibile e meno simile a un calendario generico;
- offrire contesto utile a fotografia, sport, viaggi e attività dipendenti dalla luce o dal meteo.

### Regole

- l’asse resta fisso durante lo scorrimento orizzontale;
- la linea dell’ora corrente appare soltanto nel giorno reale di oggi;
- meteo e fase lunare sono informazioni complementari e disattivabili;
- il contesto ambientale non deve compromettere contrasto o leggibilità.

## 4. Blocchi temporali

Gli eventi e le attività:

- sono posizionati verticalmente in base all’orario;
- possono sovrapporsi;
- devono essere distribuiti in corsie senza coprirsi;
- non riempiono automaticamente tutta la riga;
- usano una larghezza adattiva con limite massimo;
- possono mandare il titolo a capo entro limiti controllati;
- mantengono metadati secondari soltanto quando lo spazio lo consente.

Il pallino di selezione colore non compare direttamente nella card temporale. La modifica del colore avviene nel popup di dettaglio o nella creazione/modifica completa dell’elemento.

## 5. Densità dinamica e zoom verticale

La timeline non utilizza una scala verticale rigida identica per tutte le giornate.

La densità deve tenere conto di:

- numero totale di elementi;
- concentrazione degli elementi nella stessa fascia oraria;
- sovrapposizioni;
- frammentazione;
- quantità di attività brevi;
- spazio minimo necessario per mantenere leggibilità.

### Comportamento

- giornata leggera: scala più compatta;
- giornata densa: maggiore altezza verticale e più scorrimento;
- evento molto breve: altezza minima locale;
- un singolo evento breve non deve ingrandire arbitrariamente tutta la giornata.

Per quantità estreme di elementi, l’implementazione reale dovrà usare virtualizzazione e caricamento progressivo.

## 6. Tre livelli di estensione

### 6.1 Sotto-attività nel blocco

La parte inferiore di un evento o attività può espandersi per mostrare sotto-elementi pertinenti.

Le sotto-attività:

- sono elementi reali e cliccabili;
- possono avere orario e durata;
- possono appartenere a una categoria diversa dal genitore;
- possono avere uno stato proprio;
- aprono a loro volta il dettaglio contestuale.

L’espansione locale deve dilatare coerentemente il blocco e la griglia senza perdere il riferimento temporale.

### 6.2 Dettaglio in primo piano

Cliccando il titolo dell’elemento si apre un popup o pannello completo con:

- titolo;
- tipo;
- orario;
- durata;
- area/calendario;
- metadati;
- sotto-attività;
- colore;
- collegamenti;
- campo AI contestuale.

Il campo AI riguarda esclusivamente l’elemento aperto, per esempio:

- spostamento;
- riduzione della durata;
- sostituzione;
- applicazione soltanto alla singola occorrenza;
- modifica anche del programma futuro.

### 6.3 Espansione orizzontale per gruppi

La vista compatta e la vista per gruppi sono due stati della stessa timeline.

Trascinando la maniglia a destra:

- la timeline si allarga realmente;
- l’asse orario resta fermo;
- gli elementi mantengono la posizione verticale;
- gli elementi si distribuiscono in colonne;
- il rilascio prima della soglia torna alla vista compatta;
- il rilascio oltre la soglia completa l’espansione.

Il pulsante `Espandi per gruppo / Torna alla vista oraria` deve usare la stessa identica logica del drag.

### Maniglia

Il drag è attivo soltanto sulla maniglia visibile. Il resto del bordo destro della scheda non deve essere trascinabile.

## 7. Colonne e tipologie globali

La larghezza dell’espansione e la struttura delle colonne dipendono dall’insieme globale delle tipologie configurate, non soltanto da quelle presenti nel giorno corrente.

Questo evita che:

- la scheda cambi larghezza passando da un giorno all’altro;
- le colonne cambino ordine;
- l’utente perda il riferimento spaziale.

### Regole

- ordine delle tipologie stabile;
- colonne assenti nel giorno corrente attenuate;
- eventi presenti riallineati senza rompere la stabilità generale;
- sovrapposizioni interne alla stessa tipologia distribuite in sotto-corsie.

La tassonomia concreta delle tipologie non è ancora definitiva.

## 8. Scorrimento orizzontale condizionale

Se tutte le colonne entrano nello spazio disponibile, la barra orizzontale non compare.

Se le tipologie sono troppe:

- compare una barra di scorrimento orizzontale;
- la barra sposta intestazioni e contenuti;
- l’asse orario resta fisso;
- la barra compare soltanto nella vista espansa;
- tornando alla vista compatta, la barra scompare.

## 9. Scorrimento verticale tra giornate

La vista Today può continuare nelle giornate successive.

### Comportamento previsto

- caricamento progressivo;
- finestra iniziale di pochi giorni;
- aggiunta di nuovi giorni avvicinandosi al fondo;
- limite progettuale iniziale di 14 giorni;
- mantenimento della posizione di scroll;
- aggiornamento del giorno principale visibile.

Durante lo scroll si aggiornano:

- data;
- striscia settimanale;
- riepilogo delle ore;
- priorità contestuali;
- linea dell’ora corrente;
- stato `Oggi`, `Domani` o data completa.

Dopo il quattordicesimo giorno compare un collegamento al Calendario completo.

## 10. Colori e personalizzazione

Non sono fissate associazioni definitive tra tipo di elemento e colore.

La regola funzionale è:

1. override manuale sul singolo elemento;
2. colore ereditato da area o calendario;
3. default configurato;
4. trattamento neutro LifeOS.

### Personalizzazione

- il singolo elemento può cambiare colore dal popup;
- le impostazioni avanzate potranno modificare accento, default e colori delle aree;
- modalità chiaro/scuro e colore di accento sono concetti separati;
- successo, attenzione, errore, informazione e AI restano ruoli semantici distinti.

## 11. Stato tecnico del prototipo v7

Il prototipo è un singolo file HTML con CSS e JavaScript inclusi.

### Funzioni dimostrate

- tema chiaro/scuro;
- selezione del giorno;
- settimana cliccabile;
- timeline oraria;
- gradienti ambientali;
- meteo e fase lunare simulati;
- linea dell’ora corrente;
- elementi sovrapposti;
- densità dinamica;
- sotto-attività;
- popup dettaglio;
- richiesta AI dimostrativa;
- obiettivi e priorità;
- espansione orizzontale;
- colonne globali stabili;
- scrollbar orizzontale condizionale;
- scorrimento progressivo tra giorni.

### Non incluso

- backend;
- autenticazione;
- API;
- persistenza reale;
- sincronizzazione esterna;
- database;
- gestione produzione degli eventi;
- algoritmo definitivo di densità;
- design system definitivo;
- responsive mobile definitivo.

## 12. Decisioni consolidate

Le seguenti regole devono essere preservate nelle prossime iterazioni:

- la Home/Today è la superficie operativa principale;
- la timeline è una vista unica trasformabile, non due pagine separate;
- l’espansione locale, il dettaglio e l’espansione per gruppi sono tre livelli diversi;
- il drag avviene solo dalla maniglia;
- la timeline compatta non usa tutta la larghezza senza motivo;
- i blocchi sono adattivi e non diventano righe piene arbitrarie;
- la densità della giornata influenza lo zoom verticale;
- la struttura globale delle tipologie resta stabile;
- la scrollbar orizzontale appare solo quando serve;
- il colore del singolo elemento si modifica nel popup;
- le giornate vengono caricate progressivamente fino al limite della vista Today.

## 13. Aspetti ancora aperti

- formula definitiva della densità;
- numero e nomenclatura finale dei gruppi;
- riallineamento delle colonne vuote;
- comportamento esatto del rail a larghezze intermedie;
- responsive tablet e mobile;
- accessibilità completa del drag e dello scroll;
- virtualizzazione;
- interazioni touch;
- palette definitiva;
- design system condiviso;
- conversione del prototipo in componenti React;
- test con dati reali e scenari estremi.

## 14. Artefatti

- `prototypes/today/lifeos-home-oggi-v7.html`
- `prototypes/today/assets/lifeos-home-oggi-v7-compact.png`
- `prototypes/today/assets/lifeos-home-oggi-v7-expanded.png`
- `prototypes/today/assets/lifeos-home-oggi-v7-expanded-scroll.png`
- `docs/recaps/LifeOS_recap_totale_fase_3_e_avanzamento_fase_4_Today_v7.docx`

## 15. Regola di conservazione

Le milestone del prototipo non devono essere sovrascritte senza motivo.

Ogni versione significativa deve conservare:

- file interattivo;
- documentazione;
- snapshot visuali;
- commit identificabile;
- problemi noti;
- decisioni consolidate;
- aspetti ancora aperti.

Questo permette di confrontare le iterazioni, recuperare comportamenti eliminati per errore e impedire che decisioni importanti vadano perse.
