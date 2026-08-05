# LifeOS Home/Today v18 — leggibilità, 24h e zoom ancorato

## Obiettivo

Stabilizzare la timeline dopo v17 senza introdurre nuove funzioni.

## Modifiche

### Card adattive

- titolo e orario sempre prioritari;
- metadati secondari nascosti solo se manca spazio;
- uso fino al 94% della larghezza compatta per corsie sovrapposte;
- vincolo minimo di altezza incorporato nel mapper temporale;
- maggiore dilatazione locale per eventi brevi e fasce dense;
- nessuna collisione rettangolare nei test.

### Timeline 24 ore

- giornata completa `00:00–24:00`;
- nessuna fascia notturna rimossa;
- continuità diretta con la giornata successiva;
- apertura contestuale vicino all'ora corrente o al primo evento, evitando una schermata iniziale vuota.

### Zoom

- pulsanti zoom ancorati al centro della viewport;
- Ctrl+rotellina / pinch ancorati al punto del mouse;
- conservazione di giorno e minuto durante il reflow;
- disattivazione temporanea di smooth scrolling e browser scroll anchoring;
- nessun salto involontario di giorno.

## Test

La suite `today-v18-regression.py` verifica:

- rendering e assenza errori;
- etichette 00:00–24:00;
- leggibilità della card promemoria;
- assenza collisioni;
- popup, focus contestuale e filtri;
- espansione dopo filtro;
- zoom manuale e zoom al mouse;
- drag a 5 minuti;
- precisione di 1 minuto a zoom elevato.

Risultato: `PASS`.
