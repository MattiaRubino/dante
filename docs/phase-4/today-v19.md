# LifeOS — Home/Today v19

## Scope

Milestone di rifinitura della barra gruppi e degli elementi informativi della timeline. Nessuna modifica intenzionale a densità, card adattive, timeline 24h, zoom ancorato o drag cross-day.

## Modifiche

### Margini fra impegni

Il calcolo usa cluster temporali globali. Gli eventi sovrapposti vengono uniti fino alla fine più tarda; il margine è misurato verso il cluster successivo. Non vengono più confrontate card appartenenti a corsie arbitrarie.

### Opzioni vista e legenda

Due icone flottanti si trovano dentro il viewport della timeline, in alto a destra:

- opzioni vista e legenda;
- separa/riunisci per gruppi.

Il popover consente di attivare o disattivare margini, percorso, meteo, riferimenti astronomici, ora corrente e milestone. Le preferenze del prototipo usano `localStorage` e non alterano la geometria.

### Barra gruppi

La barra usa questa struttura:

```text
spazio righello | occhio | gruppi
```

L'occhio è il primo controllo dei gruppi e azzera filtri e focus contestuale. Le pillole restano scrollabili e riordinabili.

### Titolo card

Il titolo cambia colore soltanto quando il puntatore o il focus sono direttamente sul titolo. Hover sul corpo e zona drag non simulano l'apertura del dettaglio.

## Test

- zero errori JavaScript;
- 22 card renderizzate;
- zero collisioni;
- timeline 24h preservata;
- cluster parallelo 14:00–15:15 verificato;
- margini disattivabili senza reflow;
- controlli flottanti stabili durante lo scroll;
- occhio allineato dopo il righello;
- hover semantico del titolo;
- split completo e icon-only;
- zoom e drag v18 preservati.
