# LifeOS — Fase 4 Frontend Master Log

> Fonte di verità operativa per il passaggio fra ChatGPT, Claude e sviluppo locale.
> Leggere prima di modificare il frontend e aggiornare dopo ogni giro.

---

## 0. Stato corrente

| Campo | Valore |
|---|---|
| Progetto | LifeOS — Personal Operating System |
| Fase | 4 — prototipazione frontend e validazione UX |
| Milestone | `Home/Today v21` |
| Versione documento | `F4-FE-010` |
| Ultimo aggiornamento | 6 agosto 2026 |
| Branch | `prototype/phase-4-today-home` |
| Pull request | Draft PR `#2` |
| Implementazione | HTML/CSS/JavaScript standalone con dati simulati |
| Stato produzione | Non ancora React/Next.js; prototipo di validazione |
| Responsabile Git | ChatGPT |
| Operatore codice | ChatGPT o Claude |

## 1. Regola obbligatoria per ogni modifica

Una modifica non è chiusa finché non sono registrati:

1. richiesta o bug;
2. decisione UX/tecnica;
3. file e versione iniziale;
4. implementazione;
5. motivazione;
6. test eseguiti;
7. regressioni o limiti;
8. versione risultante e commit/PR.

Claude deve restituire sempre:

```text
VERSIONE / FILE DI PARTENZA:
RICHIESTA RICEVUTA:
FILE MODIFICATI:
MODIFICHE EFFETTUATE:
MOTIVAZIONE TECNICA:
TEST ESEGUITI:
BUG O LIMITI RESIDUI:
PUNTI CHE RICHIEDONO DECISIONE:
```

Non rimuovere o sostituire una funzione esistente durante una correzione locale senza autorizzazione esplicita.

---

## 2. Obiettivo della schermata Home/Today

Today è il cuore operativo di LifeOS. Deve consentire di:

- leggere la giornata rapidamente;
- comprendere orari, sovrapposizioni e margini;
- espandere il dettaglio senza perdere contesto;
- spostare elementi in modo fluido e annullabile;
- separare la giornata per gruppi mantenendo il tempo come asse comune;
- scorrere giorni consecutivi;
- mostrare un contesto ambientale utile senza diventare un calendario generico.

La vista compatta e la vista per gruppi sono due stati della stessa timeline, non due schermate separate.

---

## 3. Decisioni consolidate

### FE-DEC-001 — Tre livelli di approfondimento

1. sotto-attività espandibili nella card;
2. popup/pannello completo cliccando il titolo;
3. espansione orizzontale per gruppi tramite maniglia o pulsante.

### FE-DEC-002 — Tempo comune

La posizione verticale resta sempre legata all'orario, anche in vista per gruppi.

### FE-DEC-003 — Densità dinamica

Le fasce dense ricevono più spazio verticale. Un singolo evento breve non deve ingrandire indiscriminatamente tutta la giornata, ma una fascia realmente affollata deve dilatarsi quanto serve per rendere le card leggibili.

### FE-DEC-004 — Card adattive

- niente card full-width senza motivo;
- niente card microscopiche quando esiste spazio utile;
- titolo e orario sono dati primari;
- metadati secondari possono sparire soltanto se manca davvero spazio;
- sovrapposizioni in corsie senza intersezioni.

### FE-DEC-005 — Colonne globali stabili

Ordine e struttura delle colonne dipendono dalle tipologie globali, non dalle sole tipologie presenti nel giorno corrente. Il riordino dei gruppi superiori aggiorna anche la geometria sottostante.

### FE-DEC-006 — Scroll orizzontale condizionale

Compare soltanto quando le colonne non entrano. L'asse orario resta fermo.

### FE-DEC-007 — Colore nel dettaglio

Il selettore colore non appare nelle card della timeline; resta nel popup/form completo.

### FE-DEC-008 — Percorso dell'omino

È una strada visiva fissa, bianca e tratteggiata. Non rappresenta energia o capacità. Il tratto futuro è più luminoso, quello passato attenuato. Può ospitare bandierine/milestone.

### FE-DEC-009 — Capacità/energia fuori dalla vista normale

La stima di capacità non viene mostrata stabilmente nella timeline. Potrà comparire in futuro durante pianificazione, trascinamento o analisi dedicate.

### FE-DEC-010 — Focus contestuale

Clic sul corpo libero della card:

- card selezionata al 100%;
- altre card dello stesso gruppo ancora leggibili;
- altri gruppi attenuati;
- secondo clic o clic sul vuoto ripristina la vista.

### FE-DEC-011 — Drag come sottosistema isolato

- titolo: apre popup;
- comando sotto-attività: espande;
- resto della card: drag;
- soglia di attivazione 7 px;
- overlay fixed indipendente dal contenitore;
- card originale attenuata;
- auto-scroll ai bordi;
- spostamento fra giorni caricati;
- categoria invariata;
- Esc annulla silenziosamente;
- toast post-drop con Annulla.

### FE-DEC-012 — Opzioni visuali progressive

Gli elementi informativi secondari non devono diventare una fila di pulsanti permanenti. Sono raccolti in un popover `Vista e legenda`, aperto da un'icona flottante dentro la timeline.

### FE-DEC-013 — Margini calcolati per cluster

I margini fra impegni descrivono l'occupazione temporale complessiva, non la distanza fra due card scelte in base alla corsia visiva.

### FE-DEC-014 — Modifica manuale dell’orario

L’orario nella card è un controllo dedicato, separato da titolo, focus e drag.

- l’orario resta sempre su una riga propria sotto il titolo;
- clic singolo sul solo orario: apre un time picker ancorato, esterno alla card;
- il picker viene renderizzato a livello `body` e non modifica la geometria della card;
- inizio e fine usano segmenti separati per ore e minuti;
- frecce, tastiera, rotella e digitazione diretta convivono nello stesso controllo;
- modificando soltanto l’inizio, la durata viene preservata automaticamente;
- modificando anche la fine, la durata può cambiare;
- inserimento manuale con precisione al minuto, indipendente dallo snap del drag;
- `Enter` conferma, `Esc` e click esterno annullano;
- input invalido non modifica l’evento;
- la conferma ricalcola posizione, corsie, margini e densità con un solo render;
- toast con `Annulla` ripristina lo stato precedente.

---

## 4. Stato funzionale v21

### 4.1 Struttura

- sidebar;
- saluto, data, ricerca e azioni rapide;
- tema chiaro/scuro;
- striscia settimanale;
- titolo contestuale `Oggi — Martedì 4 agosto`;
- barra globale dei gruppi riordinabile e filtrabile;
- timeline continua;
- asse ambientale;
- obiettivi e priorità nel rail destro;
- popup dettaglio con AI contestuale dimostrativa;
- sotto-attività;
- drag cross-day;
- vista gruppi;
- scroll progressivo fino a 14 giorni;
- zoom manuale e da mouse/trackpad;
- opzioni vista e legenda persistenti;
- modifica manuale dell’orario tramite time picker ancorato alla card.

### 4.2 Timeline completa 24 ore

Ogni giornata copre:

```text
00:00 → 24:00
```

Non esiste salto serale/notturno. Per evitare una schermata iniziale vuota:

- oggi si apre circa due ore prima dell'ora corrente;
- un altro giorno si apre circa un'ora prima del primo evento;
- un giorno vuoto si apre intorno alle 08:00.

L'intera giornata resta accessibile tramite scroll.

### 4.3 Mapper temporale

Il mapper combina:

- quantità di eventi;
- sovrapposizioni;
- inizi ravvicinati;
- attività brevi;
- vincolo minimo di leggibilità della card.

Altezze minime indicative:

```text
1–5 minuti   → 50 px
6–15 minuti  → 68 px
16–30 minuti → 78 px
31–45 minuti → 84 px
46–60 minuti → 90 px
oltre 60 min → 96 px
con sotto-attività → almeno 98 px
```

La dilatazione viene incorporata nella funzione del tempo: griglia, orari, card, margini e linea dell'ora corrente restano coerenti.

### 4.4 Larghezza card

- gli overlap usano fino al 94% della larghezza utile della timeline compatta;
- le corsie dividono lo spazio senza sovrapporsi;
- una card singola usa una larghezza calcolata da titolo, metadati e spazio disponibile;
- titolo e orario restano visibili anche nelle card strette.

### 4.5 Precisione temporale

```text
zoom normale              → snap a 5 minuti
zoom >= 175%              → snap a 1 minuto
```

### 4.6 Zoom semantico

Lo zoom salva:

```text
giorno + minuto + posizione nella viewport
```

- pulsanti `− / +`: ancoraggio al centro della viewport;
- Ctrl+rotellina o pinch: ancoraggio sotto il puntatore;
- nessun cambio di giorno;
- nessuna animazione che attraversa giorni diversi.

### 4.7 Filtri

I filtri cambiano soltanto gli elementi visibili. Non cambiano densità, altezza della giornata, ordine globale, larghezza target, limite di espansione o geometria delle colonne.

### 4.8 Espansione per gruppi

- drag soltanto dalla maniglia visibile;
- pulsante e maniglia condividono lo stesso stato;
- timeline cresce realmente a destra;
- rail resta visibile quando c'è spazio;
- ordine delle colonne segue `GROUP_ORDER`;
- molte tipologie attivano scroll orizzontale;
- filtri non modificano la corsa massima.

### 4.9 Margini globali fra cluster temporali

Per ogni giorno:

1. gli eventi visibili vengono ordinati;
2. gli eventi sovrapposti vengono uniti in un cluster;
3. il cluster termina alla fine dell'evento che termina più tardi;
4. il margine è misurato verso il cluster successivo.

Gli eventi che si toccano restano cluster distinti, così `0 min` rimane visibile.

```text
A 14:00–15:00
B 14:30–15:15
C 14:45–15:00
D 15:15–16:30

Cluster A+B+C: 14:00–15:15
Margine verso D: 0 min
```

Nascondere i margini non modifica altezza, densità o geometria.

### 4.10 Vista e legenda

Due icone sono flottanti dentro l'angolo superiore destro del viewport della timeline:

- `Opzioni vista e legenda`;
- `Separa per gruppi / Riunisci nella timeline`.

Restano fisse durante lo scroll verticale e non scorrono con le colonne.

Il popover contiene switch persistenti per:

- margini tra gli impegni;
- percorso della giornata;
- meteo e temperatura;
- alba, tramonto e luna;
- linea dell'ora corrente;
- milestone sul percorso.

Contiene inoltre legenda e `Ripristina vista predefinita`. Nel prototipo le preferenze sono conservate in `localStorage`.

### 4.11 Barra gruppi

Struttura:

```text
spazio del righello | occhio | gruppi scrollabili e riordinabili
```

L'occhio è all'inizio dei gruppi, allineato al bordo del canvas e non sopra l'asse orario. Ripristina gruppi e focus contestuale. Un piccolo indicatore segnala uno stato da azzerare.

### 4.12 Hover semantico del titolo

- hover sul corpo: titolo invariato;
- hover/focus sul titolo: titolo violetto;
- click sul titolo: popup;
- drag sul resto: spostamento.

### 4.13 Time picker ancorato per inizio e fine

L’etichetta oraria non viene più sostituita dentro la card. Cliccandola si apre un popover ancorato:

```text
Inizio   [ 14 : 45 ] ▲/▼
Fine     [ 15 : 00 ] ▲/▼
Durata       15 min
                 ×  ✓
```

Regole:

- orario sempre sotto il titolo, mai affiancato o spinto a destra;
- popover a livello `body`, senza reflow della card;
- posizione intelligente sopra/sotto e contenimento nel viewport della timeline;
- segmenti ore/minuti selezionabili;
- frecce e `↑/↓`: incremento del segmento attivo;
- ore: passo 1 ora;
- minuti: passo 5 minuti;
- `Alt + ↑/↓`: passo 1 minuto;
- `Page Up/Page Down`: salto maggiore;
- digitazione diretta disponibile;
- il blocco si sposta soltanto dopo la conferma.

Vincoli:

- inizio fra `00:00` e `23:59`;
- fine fra `00:01` e `24:00`;
- fine successiva all’inizio nella stessa giornata;
- durata minima 1 minuto.

Un singolo evento che attraversa la mezzanotte non viene ancora interpretato implicitamente: richiede una rappresentazione multi-day separata.

---

## 5. Cronologia sintetica

- **v2:** shell, timeline, asse ambientale, card, popup, sotto-attività.
- **v3–v4:** espansione reale e recupero delle tre estensioni.
- **v5:** card compatte, drag solo maniglia, densità multifattore.
- **v6:** timeline compatta ridotta, spazio futuro e rail persistente.
- **v7:** colonne globali stabili e scrollbar condizionale.
- **v10:** onda/capacità inizialmente interpretata male, filtri e zoom.
- **v12–v13:** gruppi globali, focus, collegamenti e primo drag.
- **v14:** percorso separato dalla capacità, focus contestuale, riordino gruppi.
- **v15:** categoria invariata nel drag, filtro e card adattive ripristinate.
- **v16:** overlay fixed, auto-scroll, cross-day, undo e macchina a stati del drag.
- **v17:** densità locale, snap 5/1 minuto, filtri indipendenti dalla geometria.
- **v18:** card leggibili, timeline 24h, apertura contestuale e zoom ancorato.
- **v19:** margini per cluster, pannello Vista e legenda, controlli flottanti e hover semantico.
- **v20:** prima modifica inline di inizio/fine, durata collegata, validazione e undo.
- **v21:** time picker ancorato, spinbutton segmentati e correzione definitiva dell’orario sotto il titolo.

---

## 6. Test e non regressioni obbligatorie

- [ ] pagina senza errori JavaScript;
- [ ] almeno 12 card renderizzate;
- [ ] titolo giorno corretto;
- [ ] apertura iniziale vicino al contesto;
- [ ] etichette da 00:00 a 24:00;
- [ ] card Promemoria con titolo e orario leggibili;
- [ ] nessuna intersezione fra card;
- [ ] popup solo dal titolo;
- [ ] focus contestuale attivabile e disattivabile;
- [ ] filtro senza variazione dell'altezza;
- [ ] espansione al 100% anche con filtro;
- [ ] zoom manuale e al mouse ancorati;
- [ ] drag standard a 5 minuti;
- [ ] zoom elevato con snap a 1 minuto;
- [ ] categoria invariata durante il drag;
- [ ] sotto-attività, rail, percorso e gruppi non rimossi;
- [ ] occhio allineato dopo il righello e prima dei gruppi;
- [ ] controlli vista flottanti e stabili durante lo scroll;
- [ ] cluster 14:00–15:15 calcolato come unico blocco occupato;
- [ ] toggle margini senza variazione dell'altezza;
- [ ] hover del titolo attivo solo sul titolo;
- [ ] split icon-only con tooltip e stato semantico.
- [ ] clic sul solo orario apre il time picker ancorato;
- [ ] picker esterno alla card, senza reflow, popup dettaglio, focus o drag involontari;
- [ ] orario sempre su una riga propria sotto il titolo;
- [ ] campi segmentati ore/minuti e frecce visibili sul campo attivo;
- [ ] cambio del solo inizio preserva la durata;
- [ ] cambio esplicito della fine modifica la durata;
- [ ] precisione manuale al minuto anche a zoom normale;
- [ ] input invalido resta aperto e non salva;
- [ ] `Enter` conferma ed `Esc` annulla;
- [ ] il blocco viene riposizionato correttamente;
- [ ] toast `Annulla` ripristina l’orario precedente.

Risultati v21:

```text
22 card
0 errori JavaScript
0 collisioni
margini cluster: verificati
controlli flottanti: stabili
orario sotto il titolo: verificato
popover esterno senza reflow: verificato
spinbutton, digitazione, Enter/Esc e undo: PASS
suite Playwright v21: PASS
```

---

## 7. Problemi ancora aperti

- accessibilità completa del drag tramite tastiera e screen reader;
- virtualizzazione dei 14 giorni in produzione;
- formula finale della densità da validare con dataset realistici;
- comportamento mobile da progettare separatamente;
- conversione in componenti React/Next.js;
- gestione reale di conflitti, viaggi e suggerimenti AI;
- tassonomia definitiva dei gruppi;
- dati reali meteo, luce e fase lunare.

---

## 8. Artefatti correnti

```text
docs/phase-4/frontend-master.md
docs/phase-4/today-v21.md
tests/prototypes/today-v21-regression.py
prototypes/today/archive/v21/README.md
prototypes/today/archive/v21/lifeos-v20-to-v21.patch.gz.b64
prototypes/today/archive/v21/restore_v21.py
```

Hash locale del prototipo v21:

```text
SHA-256 86b5bc051520fa1d7ce5415ea2940c3bd1832b3735a4d0232745ed84b15bb0fb
```

---

## 9. Procedura del prossimo giro

1. leggere questo file;
2. partire esplicitamente dalla v21;
3. elencare i vincoli da preservare;
4. modificare soltanto l'ambito richiesto;
5. eseguire la suite v21 più i nuovi test;
6. creare v22 senza sovrascrivere v21;
7. aggiornare master log, documento specifico e Git.

**Aggiornare questo file a ogni giro della Fase 4 frontend.**
