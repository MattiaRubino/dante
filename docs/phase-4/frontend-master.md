# LifeOS — Fase 4 Frontend Master Log

> Documento operativo unico per continuità tra ChatGPT, Claude e sviluppo locale.
>
> Questo file è la fonte di verità della Fase 4 frontend: descrive ciò che esiste, perché è stato fatto, quali vincoli devono essere preservati, cosa è ancora provvisorio e come documentare ogni modifica successiva.

---

## 0. Metadati

| Campo | Valore |
|---|---|
| Progetto | LifeOS — Personal Operating System |
| Fase | 4 — Prototipazione frontend e validazione UX |
| Stato | Home/Today desktop in iterazione |
| Versione documento | `F4-FE-001` |
| Milestone corrente | `Today v7` |
| Ultimo aggiornamento | 4 agosto 2026 |
| Repository | `MattiaRubino/lifeos` |
| Branch | `prototype/phase-4-today-home` |
| Pull request | Draft PR `#2` |
| Prototipo | `prototypes/today/lifeos-home-oggi-v7.html` |
| Documento specifico | `docs/ux/today-home-v7.md` |
| Responsabile Git | ChatGPT, su richiesta dell'utente |
| Operatore implementazione | Claude o ChatGPT |

Il prototipo corrente è HTML/CSS/JavaScript standalone con dati simulati. Serve a validare UX e comportamento; non è ancora codice di produzione React/Next.js.

---

## 1. Scopo e regola obbligatoria

Questo documento deve permettere di passare da ChatGPT a Claude, o viceversa, senza perdere:

- stato reale del frontend;
- funzioni già introdotte;
- ragioni delle scelte;
- vincoli da non rompere;
- bug conosciuti;
- file e versioni;
- test eseguiti;
- prossima attività.

Una modifica frontend non è chiusa finché non sono registrati:

1. richiesta o problema;
2. decisione;
3. file modificati;
4. implementazione;
5. motivazione;
6. test;
7. regressioni o limiti;
8. versione e commit/PR.

Ogni giro della Fase 4 deve aggiornare questo file.

---

## 2. Collaborazione ChatGPT / Claude

### ChatGPT

- guida tecnica e UX;
- revisione delle modifiche;
- custodia del contesto;
- aggiornamento di questo master log;
- operazioni Git;
- controllo di coerenza tra codice e documentazione.

### Claude

- implementazione pratica;
- modifica dei file;
- prove nel proprio ambiente;
- report di diff, errori e limiti;
- nessuna decisione architetturale autonoma non segnalata.

### Handoff obbligatorio di Claude

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

ChatGPT usa questo report per aggiornare il master log e GitHub.

---

## 3. Versionamento

### Documento

```text
F4-FE-NNN
```

### Prototipi

```text
lifeos-<area>-vN.html
```

### Decisioni, problemi e modifiche

```text
FE-DEC-NNN
FE-ISS-NNN
FE-CHG-NNN
```

Non sovrascrivere una milestone importante. Quando cambia il comportamento, creare una nuova versione.

---

## 4. Obiettivo della Fase 4

La Fase 4 trasforma le decisioni della Fase 3 in prototipi interattivi per:

- validare Home/Today;
- validare navigazione e gerarchia;
- testare giornate leggere e dense;
- verificare progressive disclosure;
- gestire sovrapposizioni;
- definire le interazioni desktop;
- preparare la futura conversione React e l'adattamento mobile.

Non serve ancora chiudere backend, API, database, autenticazione, responsive, palette o design system definitivo.

---

## 5. Decisioni frontend consolidate

### FE-DEC-001 — Today è il cuore operativo

La Home/Today deve permettere di capire la giornata, agire sugli elementi e reagire ai cambiamenti senza aprire continuamente pagine separate.

### FE-DEC-002 — Timeline unica e trasformabile

Vista compatta e vista per gruppi sono due stati della stessa timeline, non due schermate.

### FE-DEC-003 — Tre livelli di approfondimento

1. sotto-attività espandibili nella card;
2. popup/pannello di dettaglio;
3. espansione orizzontale per gruppi.

### FE-DEC-004 — Il tempo resta il riferimento comune

Anche separando gli elementi in colonne, la posizione verticale resta legata all'orario.

### FE-DEC-005 — Niente spazio riempito senza motivo

La timeline compatta e le card non devono occupare tutta la larghezza arbitrariamente. Deve restare spazio per rail, moduli futuri ed espansione.

### FE-DEC-006 — Densità dinamica

La scala verticale si adatta alla densità della giornata. Un singolo evento breve non deve ingrandire tutta la timeline.

### FE-DEC-007 — Colonne globali stabili

Ordine e struttura delle colonne dipendono dall'insieme globale delle tipologie, non solo dal giorno corrente.

### FE-DEC-008 — Scroll orizzontale condizionale

La scrollbar appare solo se le colonne non entrano. L'asse orario resta fermo.

### FE-DEC-009 — Colore nel dettaglio

Il pallino colore non appare nelle card della timeline. Il colore si modifica nel popup o nel form completo.

### FE-DEC-010 — Documentazione e Git fanno parte della modifica

Ogni milestone deve avere prototipo, documentazione, motivazione e commit identificabile.

---

## 6. Stato corrente Home/Today v7

### 6.1 Struttura

- sidebar;
- saluto e data;
- ricerca/comando globale;
- azioni rapide;
- tema chiaro/scuro;
- striscia settimanale;
- timeline;
- asse ambientale;
- rail obiettivi/priorità;
- sotto-attività;
- popup dettaglio;
- AI contestuale dimostrativa;
- espansione per gruppi;
- scroll orizzontale condizionale;
- caricamento progressivo delle giornate.

### 6.2 Striscia settimanale

- click sul giorno aggiorna la timeline;
- il giorno selezionato si evidenzia;
- oggi mantiene un indicatore;
- gli indicatori anticipano il carico;
- durante lo scroll tra giornate la selezione si aggiorna.

### 6.3 Asse orario ambientale

Può mostrare:

- notte;
- alba;
- giorno;
- tramonto;
- sera;
- temperatura;
- fase lunare.

Razionale:

- identità distinta da un calendario generico;
- contesto utile a fotografia, sport, viaggi e attività legate a luce/meteo.

Vincoli:

- asse fisso durante lo scroll orizzontale;
- linea dell'ora corrente solo su oggi;
- meteo e luna disattivabili in futuro;
- contrasto degli orari sempre leggibile.

### 6.4 Blocchi temporali

- posizione verticale secondo inizio/fine;
- corsie per sovrapposizioni;
- larghezza adattiva con limite massimo;
- nessuna card full-width senza motivo;
- titolo con wrapping controllato;
- metadati nascosti se manca spazio;
- altezza minima locale per eventi brevi;
- nessun pallino colore sulla card;
- click sul titolo apre il dettaglio.

### 6.5 Sovrapposizioni

In vista compatta gli elementi intrecciati vengono distribuiti in corsie senza coprirsi.

In vista per gruppi, due elementi dello stesso gruppo che si sovrappongono usano sotto-corsie interne alla colonna.

### 6.6 Densità dinamica

La scala deve considerare:

- numero elementi;
- concentrazione per fascia oraria;
- overlap;
- frammentazione;
- quantità di eventi brevi;
- spazio minimo di leggibilità.

Comportamento:

- giornata leggera: scala compatta;
- giornata densa: timeline più alta e più scroll;
- evento breve: altezza minima locale;
- quantità estreme: futura virtualizzazione.

Errore da non reintrodurre:

```text
Non calcolare lo zoom globale soltanto dalla durata dell'evento più breve.
```

### 6.7 Sotto-attività

La parte bassa della card può mostrare una scritta esplicita come:

```text
3 sotto-attività · espandi
```

Le sotto-attività:

- sono cliccabili;
- possono avere orario e durata;
- possono appartenere a un'altra categoria;
- possono avere stato proprio;
- aprono il proprio dettaglio.

L'espansione deve mantenere coerenti blocco, griglia e riferimento temporale.

### 6.8 Popup di dettaglio

Deve contenere:

- titolo;
- tipo;
- orario;
- durata;
- area/calendario;
- metadati;
- sotto-attività;
- colore;
- collegamenti;
- azioni;
- campo AI contestuale.

L'AI propone cambiamenti relativi all'elemento aperto; l'utente decide.

### 6.9 Espansione orizzontale

- drag attivo solo sulla maniglia visibile;
- la timeline cresce realmente a destra;
- il rail rimane visibile quando c'è spazio;
- il rail si riduce solo se necessario;
- asse orario fisso;
- posizione verticale invariata;
- trasformazione continua durante il drag;
- sotto soglia torna compatta;
- oltre soglia completa l'apertura;
- pulsante e drag usano lo stesso stato.

### 6.10 Colonne globali

- ordine stabile;
- larghezza non dipendente dal singolo giorno;
- colonne senza elementi attenuate;
- passare da un giorno all'altro non cambia struttura;
- tassonomia concreta ancora provvisoria.

### 6.11 Scroll orizzontale

- appare solo nella vista espansa;
- compare solo se necessario;
- sposta intestazioni e contenuti;
- non sposta l'asse temporale;
- scompare tornando alla vista compatta.

### 6.12 Rail destro

Contiene obiettivi attivi, progress ring e priorità.

Regole:

- rimane visibile quando lo spazio lo consente;
- non scompare automaticamente in modalità gruppi;
- può ridursi o spostarsi solo se l'espansione richiede spazio;
- potrà ospitare altri moduli contestuali.

### 6.13 Scroll tra giornate

Direzione:

- caricamento progressivo;
- pochi giorni iniziali;
- caricamento vicino al fondo;
- limite iniziale Today: 14 giorni;
- aggiornamento del giorno principale visibile;
- collegamento al Calendario dopo il limite.

Devono aggiornarsi data, settimana, riepilogo, priorità, stato Oggi/Domani/data e linea dell'ora corrente.

### 6.14 Colori

Nessuna associazione definitiva tra tipo e colore.

Priorità prevista:

1. override del singolo elemento;
2. colore area/calendario;
3. default configurato;
4. trattamento neutro LifeOS.

Chiaro/scuro e colore d'accento sono dimensioni separate. Successo, warning, errore, info e AI restano ruoli semantici distinti.

---

## 7. Direzione visuale provvisoria

LifeOS deve essere premium, personale, calmo, moderno, leggermente futuristico e distinto da un comune calendario.

Profondità su tre livelli:

1. struttura;
2. componente interattivo;
3. pannello flottante.

Usare superfici, bordi sottili, ombre morbide e luce interna minima. Evitare glow continuo, neon aggressivo, glassmorphism pesante e gradienti su ogni card.

Font esplorati:

- Manrope per UI;
- Space Grotesk per titoli e metriche grandi.

Questa scelta non è ancora definitiva.

---

## 8. Cronologia delle iterazioni

### v2 — base

Introdotti shell, timeline, asse ambientale, card, popup, sotto-attività, prima espansione e rail.

Problemi: espansione non reale, rail fisso, blocchi deformati, scala alterata dall'evento più breve, card troppo grandi.

### v3/v4 — correzioni strutturali

Obiettivo: espansione reale, conservazione delle tre estensioni e scroll tra giornate.

Le regressioni hanno fissato una regola: non rimuovere funzioni esistenti durante correzioni locali.

### v5 — card e densità

- card adattive;
- timeline più compatta;
- pallino colore rimosso;
- drag limitato alla maniglia;
- densità basata su più fattori.

### v6 — larghezza e rail

- timeline compatta ristretta;
- spazio libero a destra;
- rail persistente;
- espansione più controllata.

### v7 — colonne globali

- struttura basata sulle tipologie globali;
- ordine stabile;
- colonne vuote attenuate;
- scrollbar condizionale;
- asse orario fisso.

---

## 9. Registro modifiche consolidate

### FE-CHG-001 — Asse ambientale

Rende la timeline riconoscibile e offre contesto utile. Mantenere; dati reali rimandati.

### FE-CHG-002 — Corsie per overlap

Evita che eventi simultanei si coprano. Mantenere.

### FE-CHG-003 — Sotto-attività

Permette progressive disclosure senza lasciare la timeline. Mantenere; reflow da validare.

### FE-CHG-004 — Dettaglio e AI contestuale

Separa scansione rapida e controllo profondo. Mantenere.

### FE-CHG-005 — Timeline trasformabile

Caratteristica centrale: vista unica che si separa in colonne mantenendo il tempo comune.

### FE-CHG-006 — Drag solo dalla maniglia

Evita interazioni involontarie. Mantenere.

### FE-CHG-007 — Card compatte

Riduce spazio sprecato e lascia margine all'espansione. Mantenere.

### FE-CHG-008 — Densità dinamica

Evita la compressione delle giornate dense. Principio approvato; formula aperta.

### FE-CHG-009 — Rail persistente

Obiettivi e priorità restano parte della lettura della giornata.

### FE-CHG-010 — Colonne globali stabili

Evita salti di layout e conserva memoria spaziale.

### FE-CHG-011 — Scroll orizzontale condizionale

Gestisce molte tipologie senza comprimere tutto.

### FE-CHG-012 — Colore nel popup

Riduce rumore visivo nella timeline.

---

## 10. Problemi aperti

### FE-ISS-001 — Formula densità

Definire formula controllabile con numero elementi, overlap, distribuzione, durata, frammentazione e altezza minima.

### FE-ISS-002 — Tassonomia gruppi

Decidere se le colonne rappresentano tipo, area, categoria, progetto o raggruppamento scelto dall'utente.

### FE-ISS-003 — Colonne vuote

Valutare se mantenerle attenuate, comprimerle o riallineare le presenti senza perdere l'ordine globale.

### FE-ISS-004 — Rail intermedio

Definire larghezza minima, compressione, spostamento e moduli prioritari.

### FE-ISS-005 — Sotto-attività complesse

Verificare collisioni, aperture multiple, limite e comportamento touch.

### FE-ISS-006 — Scroll multigiorno

Completare caricamento progressivo, IntersectionObserver, conservazione scroll e virtualizzazione.

### FE-ISS-007 — Accessibilità

Tastiera, screen reader, drag accessibile, focus, reduced motion, contrasto e target touch.

### FE-ISS-008 — Mobile

La home mobile richiede progettazione dedicata, non compressione della desktop.

### FE-ISS-009 — Conversione React

Definire componenti, stato, algoritmo layout, separazione dati/presentazione, test e design tokens.

---

## 11. Criteri di non regressione

- [ ] asse orario coerente;
- [ ] posizione temporale corretta;
- [ ] overlap senza copertura;
- [ ] card non full-width senza motivo;
- [ ] wrapping controllato;
- [ ] nessun pallino colore sulle card;
- [ ] sotto-attività espandibili e cliccabili;
- [ ] popup funzionante;
- [ ] AI contestuale presente;
- [ ] drag solo sulla maniglia;
- [ ] pulsante e drag sincronizzati;
- [ ] asse fermo in vista gruppi;
- [ ] posizione verticale invariata;
- [ ] rail visibile quando c'è spazio;
- [ ] colonne stabili tra giornate;
- [ ] scrollbar solo quando serve;
- [ ] densità maggiore nelle giornate dense;
- [ ] un evento breve non altera da solo la scala;
- [ ] tema chiaro/scuro funzionante;
- [ ] selezione giorno funzionante;
- [ ] nessun errore JavaScript bloccante.

---

## 12. Procedura per ogni giro

### Prima

1. leggere questo file;
2. leggere il documento specifico;
3. identificare la versione;
4. elencare i vincoli;
5. non rimuovere funzioni senza autorizzazione.

### Durante

1. modificare solo l'ambito richiesto;
2. evitare refactor inutili;
3. conservare dati utili ai test;
4. non cambiare estetica globale se non richiesto;
5. mantenere note tecniche.

### Dopo

1. creare una nuova versione se cambia il comportamento;
2. testare la checklist;
3. produrre preview;
4. aggiornare questo file;
5. aggiornare il documento della schermata;
6. salvare su Git;
7. annotare commit/PR;
8. dichiarare i punti aperti.

---

## 13. Template aggiornamento

```markdown
### FE-CHG-NNN — Titolo

- Data:
- Operatore:
- Versione iniziale:
- Versione risultante:
- File modificati:
- Commit/PR:

#### Richiesta o problema
...

#### Decisione
...

#### Implementazione
...

#### Perché
...

#### Test
- [ ] ...

#### Regressioni o limiti
...

#### Prossimo passo
...
```

---

## 14. Artefatti

```text
docs/phase-4/frontend-master.md
docs/ux/today-home-v7.md
prototypes/today/archive/README.md
prototypes/today/archive/lifeos-home-oggi-v7.html.gz.b64.part01
prototypes/today/archive/lifeos-home-oggi-v7.html.gz.b64.part02
prototypes/today/archive/lifeos-home-oggi-v7.html.gz.b64.part03
prototypes/today/archive/lifeos-home-oggi-v7.html.gz.b64.part04
prototypes/today/archive/restore_prototype.py
```

Ripristino:

```bash
python prototypes/today/archive/restore_prototype.py
```

---

## 15. Git workflow

- branch: `prototype/phase-4-today-home`;
- PR: draft `#2`;
- la PR resta draft finché Today è in iterazione;
- ChatGPT gestisce Git;
- Claude consegna file/diff/report;
- le milestone non vengono cancellate;
- prima del merge si controllano documentazione, prototipo e non regressione.

Commit consigliati:

```text
docs: update Phase 4 frontend master log
feat: iterate Today timeline prototype
fix: preserve grouped timeline layout
chore: archive Today prototype milestone
```

---

## 16. Changelog master

### F4-FE-001 — 4 agosto 2026

- creato il master log frontend;
- consolidato lo stato Today v7;
- registrati principi, cronologia, modifiche e problemi aperti;
- definito il protocollo ChatGPT/Claude;
- definita la procedura obbligatoria di aggiornamento e Git.

---

**Aggiornare questo file a ogni giro della Fase 4 frontend.**
