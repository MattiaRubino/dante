# Editor delle registrazioni delle Sessioni

**Stato:** candidate sul branch Timeline; E2E con PostgreSQL superato,
revisione visiva locale ancora aperta. Regole di dominio:
[`activity-session-operational-lifecycle-v2.md`](../../domain/decisions/activity-session-operational-lifecycle-v2.md).

L'Inspector di un'Attività mostra l'azione «Registrazioni delle Sessioni»
accanto alle altre azioni solo quando esiste la principale, una secondaria
configurata o almeno un tentativo storico. Il pannello separato riusa il nome
dell'Attività, il fuso di visualizzazione della Timeline e il linguaggio
grafico degli editor Dante. La testata e il titolo dell'Attività restano fissi:
**solo il corpo delle registrazioni scorre** in un'area dedicata. Anche il
footer con «Salva registrazioni» ed eventuali errori rimane sempre visibile,
fuori dallo scorrimento; date, orari, menu e pulsanti mantengono gli stessi
controlli interattivi.
I popup di calendario e orario vicini al fondo della regione scorrono
automaticamente in vista, senza portare via dal footer il tasto Salva.
 Su schermi stretti i campi inizio/fine sono impilati.

La presenza dell'azione deriva dalla struttura Activity (`/children`) e dalle
Sessioni già presenti (`/sessions`), anche se una delle due letture non è
disponibile. La lettura specifica dell'editor (`/sessions/editor`) avviene
soltanto quando si apre il pannello; un suo errore viene mostrato lì, senza
nascondere preventivamente l'azione nell'Inspector. Il database persistente
deve comunque avere la migrazione dell'editor applicata per leggere e salvare
le registrazioni; lo stack E2E usa un database temporaneo migrato.

Ogni tentativo conserva il proprio identificativo. La riga vuota offre
«Registra»; dopo la lettura canonica del salvataggio offre «Correggi» sulla
stessa Sessione. Un tentativo ancora aperto è visibile ma non editabile qui:
Play/Pausa/Riprendi/Stop restano nei controlli live. L'editor consente di
specificare gli intervalli **attivi** con la stessa riga data/ora di Crea e
Modifica, fino a 100 intervalli per registrazione. Lo spazio tra la fine di
un intervallo e l'inizio del successivo è una pausa: non esiste un modulo
separato «+ Pausa». Il salvataggio converte queste lacune nelle `pause_ranges`
fattuali già previste dall'API. La barra distingue tempo attivo e pause.
Il campo non rappresenta l'orario pianificato della Sessione interna.

Il pannello usa gli stessi selettori data e ora di Crea/Modifica, con il fuso
dell'Attività fisso. Quando è presente la Sessione attività, l'editor usa due livelli:
ogni intervallo attivo della principale è un padre, sotto il quale l'azione
«Registra sessione» sceglie una Sessione secondaria già configurata.
La scelta non crea una nuova definizione. La principale e le secondarie
ancora da registrare sono configurabili nella stessa bozza, senza dover
salvare prima la principale. Se una Sessione già scelta per l'intervallo 1
riprende nell'intervallo 2, il menu offre **«Nome · Riprendi»**:
aggiunge un altro intervallo attivo **alla stessa registrazione**, non
crea un nuovo tentativo. Ogni tratto della secondaria è presentato sotto
il relativo intervallo attivo padre, con la propria riga data/ora.
La pausa fra due tratti secondari include necessariamente la pausa della
principale. La secondaria conserva una sola SessionRef, un'unica bozza e
un'unica scrittura, anche se appare in più intervalli padre. Una
registrazione già conclusa può essere ripresa retroattivamente tramite
correzione della stessa SessionRef e nuovo MaterialState, mai con
un secondo tentativo fittizio. Le pause sono i vuoti tra intervalli attivi e non esiste
un editor separato delle pause. Due secondarie possono sovrapporsi tra
loro; due intervalli della stessa Sessione no.

«Aggiungi intervallo» crea una riga già valida solo quando
esiste spazio nel passato: inizio minimo = fine del precedente + 1 minuto,
fine massima = ora attuale e, nelle secondarie, anche fine del padre.
Durata e pausa minime delle nuove registrazioni: 1 minuto.
Senza spazio crea una riga nello stesso layout, con i consueti selettori
DANTE, gli orari vuoti e la stessa X di rimozione. Il nuovo intervallo
si completa automaticamente alla conferma dei campi, senza pulsanti
aggiuntivi. Per liberare spazio si modificano esplicitamente gli
intervalli esistenti: nessuna divisione automatica del precedente.
Dopo un POST accettato, la rilettura
deve confermare tutte le ricevute prima di sostituire le righe e cancellare
la bozza: una risposta incompleta lascia visibili gli input e conserva gli
identificativi delle operazioni per un tentativo idempotente.

Una secondaria deve restare dentro i tratti attivi della principale.
**Durante la digitazione la UI non riscrive l'orario:**
i componenti DANTE acquisiscono ore e minuti separatamente.
Alla conferma (uscita dal controllo, Invio o scelta della data)
il motore temporale applica minimo e massimo da precedente,
successivo, padre e ora attuale, correggendo **solo il campo confermato**.
Se non esiste un valore ammissibile, la riga resta editabile con
messaggio locale breve («Nessuno spazio (min 1 min)»,
«Inizio minimo: 10:32», «Fine massima: 11:00»).
«Adatta ai limiti» resta disponibile quando una modifica del
padre lascia una secondaria fuori dal suo tratto. Salva rifiuta
l'eventuale violazione ancora presente, evidenziando il singolo intervallo
sbagliato; PostgreSQL ripete la verifica autorevole. Una modifica
temporaneamente invalida di un intervallo padre non deve far sparire,
spostare o rimontare le secondarie: l'appartenenza visiva dei singoli
tratti è stabile durante la bozza, anche quando si modifica prima
l'inizio e poi la fine. Dopo un salvataggio valido, la gerarchia si
ricostruisce dagli intervalli effettivi salvati. Anche «Registra sessione»
resta selezionabile quando il padre è momentaneamente invalido: viene
predisposto un intervallo secondario provvisorio da correggere insieme
al padre prima del salvataggio. Nessuna bozza provvisoria viene scritta
senza la verifica temporale finale.
Con principale disabilitata, le secondarie usano blocchi autonomi con gli
stessi controlli, senza limiti di padre inventati.

Il salvataggio di principale e secondarie avviene tramite un comando
di gruppo atomico, in una transazione SERIALIZABLE, ordinando principale
prima delle secondarie e riportando qualsiasi errore senza scritture
parziali. Il vecchio comando di una Sessione per volta rimane disponibile
per compatibilità, ma non è più usato dal nuovo pannello. Il client
verifica le ricevute e la rilettura canonica prima di abbandonare i dati
temporanei e, **solo dopo conferma**, chiude il pannello e l'Inspector
riportando alla Home. In caso di errore o riscontro incompleto, il pannello
resta aperto e conserva le modifiche. Le registrazioni salvate sono mostrate in sola lettura;
«Correggi» è accanto all'intervallo e apre la modifica della stessa
Sessione. Correggere mantiene SessionRef e storico MaterialState.
Una Sessione live aperta non è correggibile qui.
La correzione simultanea di principale e secondarie verifica il loro stato
finale alla fine della transazione: spostarle insieme non viene respinto a
causa dei vecchi orari. Il comando singolo mantiene lo stesso vincolo alla
fine della propria transazione.

Il pannello mantiene la stessa riga data/ora di Create/Edit ma
rimuove il testo decorativo sul fuso. Il nome dell'Attività è sopra
la card principale. Aggiungi intervallo modifica soltanto i tratti
attivi della registrazione, mai gli Schedule dell'Activity.
Il punto d'ingresso da «Da verificare» resta fuori da questa candidata.

Il calendario usa orari locali nel fuso indicato e converte in istanti
assoluti prima della scrittura. Un'ora inesistente durante il cambio d'ora
è rifiutata; per un'ora ripetuta l'utente sceglie «Prima volta» o «Seconda
volta». Una correzione ripropone la scelta corrispondente all'istante già
registrato. Gli errori di input o del server
restano accanto al modulo attivo. Il salvataggio del pannello è atomico per il gruppo di registrazioni
modificate, ma ogni Sessione conserva il proprio tentativo e la propria
identità. Non cambia la configurazione di Activity, Schedule o delle altre
Sessioni non incluse nella richiesta. Dopo il
successo, il pannello rilegge la fonte canonica, notifica Timeline,
Inspector e pannello destro e chiude l'Inspector. Una registrazione già conclusa non torna
avviabile per effetto del salvataggio.

Il punto d'ingresso da «Da verificare» è previsto come riuso dello stesso
componente; non è incluso nel candidate di questa prima implementazione.

Il test browser autenticato `temporal-session-recording-editor.spec.ts`
copre Create → Inspector → Registra → Correggi e rilegge la Sessione dal
backend dopo entrambi i salvataggi. L'owner lo ha eseguito sullo stack reale
con PostgreSQL migrato: **1 passato in 22,0 s** sul commit `9eefa40` e
**1 passato in 20,9 s** dopo il riordino grafico del commit `e1e4d6c`.
La revisione visiva manuale e il gate completo restano separati.
