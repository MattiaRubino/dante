# LifeOS — Fase 4 Frontend Master Log

> Fonte di verità operativa per il passaggio fra ChatGPT, Claude e sviluppo locale.
> Leggere prima di modificare il frontend e aggiornare dopo ogni giro.

---

## 0. Stato corrente

| Campo | Valore |
|---|---|
| Progetto | LifeOS — Personal Operating System |
| Fase | 4 — prototipazione frontend e validazione UX |
| Milestone | `Home/Today v18` |
| Versione documento | `F4-FE-007` |
| Ultimo aggiornamento | 5 agosto 2026 |
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

---

## 4. Stato funzionale v18

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
- zoom manuale e da mouse/trackpad.

### 4.2 Timeline completa 24 ore

Ogni giornata copre:

```text
00:00 → 24:00
```

Non esiste più il salto serale/notturno. La fascia notturna può contenere lavoro, sonno, viaggi o emergenze e continua direttamente nella giornata successiva.

Per evitare una schermata iniziale vuota:

- oggi si apre circa due ore prima dell'ora corrente;
- un altro giorno si apre circa un'ora prima del primo evento;
- un giorno vuoto si apre intorno alle 08:00.

L'intera giornata resta accessibile tramite scroll.

### 4.3 Mapper temporale v18

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
- il bias di categoria è ridotto e non deve troncare inutilmente le card;
- titolo e orario restano visibili anche nelle card strette.

### 4.5 Precisione temporale

```text
zoom normale              → snap a 5 minuti
zoom >= 175%              → snap a 1 minuto
```

Non vengono stampate etichette per ogni minuto; la precisione riguarda il posizionamento.

### 4.6 Zoom semantico

Il vecchio rapporto proporzionale fra altezze è stato eliminato. Lo zoom salva:

```text
giorno + minuto + posizione nella viewport
```

Dopo il re-render ritrova la stessa ancora.

- pulsanti `− / +`: ancoraggio al centro della viewport;
- Ctrl+rotellina o pinch: ancoraggio sotto il puntatore;
- nessun cambio di giorno;
- smooth scrolling e browser scroll anchoring disattivati durante il reflow;
- nessuna animazione che attraversa giorni diversi.

### 4.7 Filtri

I filtri cambiano soltanto gli elementi visibili. Non cambiano:

- densità;
- altezza della giornata;
- ordine globale;
- larghezza target;
- limite di espansione;
- geometria delle colonne.

### 4.8 Espansione per gruppi

- drag soltanto dalla maniglia visibile;
- pulsante e maniglia condividono lo stesso stato;
- timeline cresce realmente a destra;
- rail resta visibile quando c'è spazio;
- ordine delle colonne segue `GROUP_ORDER`;
- molte tipologie attivano scroll orizzontale;
- filtri non modificano la corsa massima.

---

## 5. Cronologia sintetica

- **v2:** shell, timeline, asse ambientale, card, popup, sotto-attività.
- **v3–v4:** espansione reale e recupero delle tre estensioni.
- **v5:** card compatte, drag solo maniglia, densità multifattore.
- **v6:** timeline compatta ridotta, spazio futuro e rail persistente.
- **v7:** colonne globali stabili e scrollbar condizionale.
- **v10:** onda/capacità inizialmente interpretata male, filtri e zoom.
- **v12–v13:** gruppi globali, focus, collegamenti e primo drag.
- **v14:** percorso dell'omino separato dalla capacità, focus contestuale, riordino gruppi.
- **v15:** categoria invariata nel drag, filtro e card adattive ripristinate.
- **v16:** overlay fixed, auto-scroll, cross-day, undo e macchina a stati del drag.
- **v17:** densità locale, snap 5/1 minuto, filtri indipendenti dalla geometria.
- **v18:** card realmente leggibili, timeline 24h, apertura contestuale e zoom ancorato.

---

## 6. Test e non regressioni obbligatorie

La suite v18 deve verificare almeno:

- [ ] pagina senza errori JavaScript;
- [ ] almeno 12 card renderizzate;
- [ ] titolo giorno corretto;
- [ ] apertura iniziale vicino al contesto, non a mezzanotte;
- [ ] etichette da 00:00 a 24:00;
- [ ] card Promemoria con titolo e orario leggibili;
- [ ] nessuna intersezione fra card;
- [ ] popup solo dal titolo;
- [ ] focus contestuale attivabile e disattivabile;
- [ ] filtro senza variazione dell'altezza;
- [ ] espansione al 100% anche con filtro;
- [ ] zoom manuale con errore ancora < 0.5 minuti;
- [ ] zoom al mouse con errore ancora < 0.75 minuti;
- [ ] drag standard a 5 minuti;
- [ ] zoom elevato con snap a 1 minuto;
- [ ] categoria invariata durante il drag;
- [ ] sotto-attività, rail, percorso e gruppi non rimossi.

Risultati v18:

```text
22 card
0 errori JavaScript
0 collisioni
canvas Today ≈ 2226.52 px
Promemoria ≈ 168 × 68 px
test Playwright: PASS
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
docs/phase-4/today-v18.md
prototypes/today/lifeos-home-oggi-v18.html
tests/prototypes/today-v18-regression.py
prototypes/today/archive/v18/lifeos-v17-to-v18.patch
```

Hash locale del prototipo v18:

```text
SHA-256 b0eb870de16ea862bd707b49fd4fcaf7939151abe3e1b4c2b287a37ee5ef186b
```

---

## 9. Procedura del prossimo giro

1. leggere questo file;
2. partire esplicitamente dalla v18;
3. elencare i vincoli da preservare;
4. modificare soltanto l'ambito richiesto;
5. eseguire la suite v18 più i nuovi test;
6. creare v19 senza sovrascrivere v18;
7. aggiornare master log, documento specifico e Git.

**Aggiornare questo file a ogni giro della Fase 4 frontend.**
