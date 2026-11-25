# Editor delle registrazioni delle Sessioni

**Stato:** candidate sul branch Timeline; E2E con PostgreSQL superato,
revisione visiva locale ancora aperta. Regole di dominio:
[`activity-session-operational-lifecycle-v2.md`](../../domain/decisions/activity-session-operational-lifecycle-v2.md).

L'Inspector di un'Attività mostra l'azione «Registrazioni delle Sessioni»
accanto alle altre azioni solo quando esiste la principale, una secondaria
configurata o almeno un tentativo storico. Il pannello separato riusa il nome
dell'Attività, il fuso di visualizzazione della Timeline e il linguaggio
grafico degli editor Dante. Scorrono soltanto le registrazioni, non la testata.
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
specificare inizio, fine e intervalli di pausa; la barra di riepilogo
distingue visivamente il tempo attivo dalle pause e calcola il totale attivo.
Il campo non rappresenta l'orario pianificato della Sessione interna.

Il pannello usa gli stessi selettori data e ora di Crea/Modifica, con il fuso
dell'Attività fisso. Quando è presente la Sessione attività, principale e
secondarie formano un unico gruppo: le secondarie sono rientrate sotto la
principale. Dopo il salvataggio i campi si richiudono; una scala temporale
comune mostra i tratti attivi della principale e le secondarie registrate,
lasciando vuoti i tratti in pausa. «Correggi» riapre i controlli senza creare
una seconda registrazione. Senza principale, ogni secondaria conserva il
proprio riepilogo. «+ Pausa» propone un tratto interno modificabile, se gli
orari lo permettono. Prima della richiesta, gli errori di ordine e di
contenimento nella principale sono evidenziati vicino agli orari coinvolti.

Il calendario usa orari locali nel fuso indicato e converte in istanti
assoluti prima della scrittura. Un'ora inesistente durante il cambio d'ora
è rifiutata; per un'ora ripetuta l'utente sceglie «Prima volta» o «Seconda
volta». Una correzione ripropone la scelta corrispondente all'istante già
registrato. Gli errori di input o del server
restano accanto al modulo attivo. Il salvataggio è per tentativo e non cambia
la configurazione di Activity, Schedule o delle altre Sessioni. Dopo il
successo, il pannello rilegge la fonte canonica e notifica Timeline,
Inspector e pannello destro. Una registrazione già conclusa non torna
avviabile per effetto del salvataggio.

Il punto d'ingresso da «Da verificare» è previsto come riuso dello stesso
componente; non è incluso nel candidate di questa prima implementazione.

Il test browser autenticato `temporal-session-recording-editor.spec.ts`
copre Create → Inspector → Registra → Correggi e rilegge la Sessione dal
backend dopo entrambi i salvataggi. L'owner lo ha eseguito sullo stack reale
con PostgreSQL migrato: **1 passato in 22,0 s** sul commit `9eefa40` e
**1 passato in 20,9 s** dopo il riordino grafico del commit `e1e4d6c`.
La revisione visiva manuale e il gate completo restano separati.
