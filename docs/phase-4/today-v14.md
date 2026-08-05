# LifeOS — Home/Today v14

## Stato

Milestone frontend interattiva successiva a v13. Il file eseguibile completo resta nell'artefatto locale `LifeOS_Home_Oggi_v14_canvas_verified.html`; questa nota registra le decisioni e i test del giro.

## Modifiche

- percorso dell'omino separato dalla capacità/energia;
- tratto futuro più luminoso, tratto già percorso attenuato;
- curva fissa, regolare, bianca e tratteggiata;
- piccole milestone dimostrative sul percorso;
- capacità rimossa dalla vista Today normale e rinviata a pianificazione/drag/analisi dedicate;
- collegamento attività → obiettivo rimosso;
- focus contestuale introdotto: selezionato pieno, stesso gruppo attenuato, altri gruppi grigi;
- pulsante occhio azzera filtri e focus;
- drag avviato solo dalla zona libera del blocco;
- clone reale lasciato nella posizione originale;
- blocco reale segue il puntatore in verticale e orizzontale;
- snap temporale a 15 minuti;
- in vista compatta il movimento orizzontale non cambia gruppo;
- in vista espansa il drop può cambiare gruppo/colonna;
- riordino dei chip globali sincronizzato con l'ordine delle colonne espanse;
- titolo giorno nel formato `Oggi — Martedì 4 agosto`.

## Test

- rendering senza errori JavaScript;
- 22 blocchi e 6 gruppi caricati;
- focus contestuale e reset verificati;
- espansione verificata;
- riordino `Salute` prima di `Focus` verificato;
- clone reale e movimento bidimensionale verificati;
- snap a 15 minuti verificato.

## Limiti aperti

- nessun drag cross-day;
- nessuna collision preview completa;
- nessuna persistenza backend/local storage;
- milestone ancora dimostrative;
- capacità documentata ma non mostrata in Today.
