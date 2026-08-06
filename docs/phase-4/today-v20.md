# LifeOS Home/Today v20 — modifica manuale dell’orario

## Obiettivo

Aggiungere un’alternativa precisa al drag per cambiare inizio e fine direttamente dalla card, senza aprire il popup completo e senza rompere le interazioni consolidate.

## Interazione

Un clic sul solo orario trasforma la riga temporale in:

```text
[inizio] – [fine] [conferma] [annulla]
```

La scelta è il clic singolo sul target esatto, non il doppio clic: il doppio clic è poco scopribile, più difficile da usare da tastiera/touch e non necessario perché il dato temporale è una zona dedicata.

## Comportamento

- cambiando soltanto l’inizio, la fine segue automaticamente e conserva la durata;
- quando l’utente modifica la fine, i due campi diventano indipendenti;
- precisione al minuto anche quando il drag usa snap di 5 minuti;
- `Enter` conferma;
- `Esc` e pulsante rosso annullano;
- clic fuori annulla la modifica non confermata;
- un solo editor può essere aperto alla volta;
- la conferma ricalcola posizione, densità, overlap, margini e gruppi;
- compare un toast con `Annulla`.

## Formati accettati

- `14:47`
- `1447`
- `14.47`
- `9` → `09:00`

La fine può essere `24:00`; l’inizio no. La fine deve essere successiva all’inizio nella stessa giornata.

## Non incluso

Un singolo evento che attraversa la mezzanotte non viene ancora creato implicitamente inserendo una fine inferiore all’inizio. Questo richiede la rappresentazione multi-day dell’evento e viene mantenuto separato per non introdurre ambiguità.

## Test

`today-v20-regression.py` verifica:

- apertura esclusivamente dal dato temporale;
- nessun popup o focus involontario;
- durata preservata;
- durata modificabile;
- precisione al minuto;
- validazione;
- Enter/Esc;
- riposizionamento reale;
- undo;
- tutte le regressioni v19.

Risultato: `PASS`.
