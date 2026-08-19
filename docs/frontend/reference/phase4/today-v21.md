# LifeOS Home/Today v21 — time picker ancorato

## Obiettivo

Correggere il reflow introdotto dalla modifica inline dell’orario in v20 e adottare un controllo più coerente con i pattern dei prodotti maturi.

## Decisione

L’orario resta sempre su una riga dedicata sotto il titolo della card. Cliccando l’orario, la card non cambia struttura: viene aperto un popover ancorato, renderizzato a livello `body` e posizionato sopra o sotto in base allo spazio disponibile.

## Time picker

Il popover contiene:

- campo `Inizio` segmentato in ore e minuti;
- campo `Fine` segmentato in ore e minuti;
- frecce incremento/decremento visibili sul campo attivo;
- durata aggiornata in anteprima;
- conferma con spunta verde;
- annullamento neutro, con feedback rosso soltanto in hover;
- messaggio di validazione inline.

## Interazioni

- click sull’orario: apre il picker;
- click su ore o minuti: seleziona il segmento;
- frecce laterali o `↑/↓`: modificano il segmento selezionato;
- minuti: passo standard 5 minuti;
- ore: passo standard 1 ora;
- `Page Up/Page Down`: salto maggiore;
- `Alt + ↑/↓`: precisione di 1 minuto;
- digitazione diretta ancora disponibile per variazioni ampie o precise;
- modificando solo l’inizio, la durata originale viene preservata;
- modificando la fine, la durata può cambiare;
- `Enter` conferma;
- `Esc` o click esterno annullano.

## Geometria

- il picker è esterno alla card;
- aprirlo non modifica larghezza, altezza o posizione della card;
- viene contenuto nel viewport visibile della timeline;
- segue l’ancora durante piccoli scroll;
- si chiude se la card esce dalla parte visibile;
- il blocco viene riposizionato soltanto dopo la conferma.

## Correzione layout

L’orario usa sempre una riga propria sotto il titolo. È vietato il layout in cui titolo e orario finiscono sulla stessa linea o l’orario viene spinto a destra.

## Test

La suite `today-v21-regression.py` verifica:

- assenza di errori JavaScript;
- timeline 24 ore e zero collisioni;
- orario sotto il titolo su card larghe e strette;
- popover figlio diretto di `body`;
- card invariata mentre il picker è aperto;
- campi segmentati e frecce sul campo attivo;
- incremento a 5 minuti e durata collegata;
- digitazione al minuto;
- validazione, `Enter`, `Esc` e undo;
- posizionamento dentro il viewport della timeline;
- zoom, drag, gruppi e margini non regrediti.

Risultato: `PASS`.
