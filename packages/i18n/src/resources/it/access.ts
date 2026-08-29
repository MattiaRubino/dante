export const access = {
  stage: {
    titleFirst: 'Comprendi la vita.',
    titleSecond: 'Dai forma al prossimo passo.',
    body: 'Uno spazio personale per capire cosa sta succedendo, mantenere continuità nel tempo e decidere cosa viene dopo.',
    foot: 'Una sola realtà. Più modi per comprenderla.',
  },
  kicker: {
    access: 'Accesso',
    setup: 'Configurazione iniziale',
  },
  signin: {
    title: 'Accedi a DANTE',
    body: 'Continua con il tuo account oppure usa email e password.',
    forgot: 'Password dimenticata?',
    new: 'Nuovo su DANTE?',
  },
  signup: {
    title: 'Crea il tuo account DANTE',
    body: 'Usa un indirizzo email a cui hai accesso. Ti chiederemo di verificarlo.',
    existing: 'Hai già un account?',
    progress: 'Avanzamento creazione account',
    stepEmail: 'Email',
    stepPassword: 'Password',
    stepVerify: 'Verifica',
    continueEmail: 'Continua con email',
    orProvider: 'oppure continua con',
    google: 'Continua con Google',
    apple: 'Continua con Apple',
  },
  signupPassword: {
    title: 'Proteggi il tuo account',
    body: 'Scegli una password lunga e unica. Puoi usare quella generata dal tuo password manager.',
  },
  password: {
    guideTitle: 'Lunghezza minima',
    proposal: '15+ caratteri',
    manager:
      'Puoi incollare o generare la password con il tuo password manager.',
  },
  provider: {
    google: 'Continua con Google',
    apple: 'Continua con Apple',
    googleName: 'Google',
    appleName: 'Apple',
    body: 'DANTE apre il flusso ufficiale del provider. La schermata di consenso appartiene al provider, non DANTE.',
    wait: 'Completa l’accesso',
    pendingBody:
      'Completa l’accesso nella finestra del provider. Tornerai automaticamente a DANTE.',
    scopeNote:
      'Usare Google o Apple per accedere non autorizza DANTE a leggere Calendar, Gmail o iCloud.',
  },
  common: {
    or: 'oppure',
  },
  field: {
    email: 'Email',
    emailPlaceholder: 'nome@esempio.com',
    password: 'Password',
    verificationCode: 'Codice di verifica',
  },
  action: {
    signin: 'Accedi',
    logout: 'Esci',
    createAccount: 'Crea un account',
    showPassword: 'Mostra password',
    hidePassword: 'Nascondi password',
    continue: 'Continua',
    cancel: 'Annulla',
    changeEmail: 'Cambia email',
    backSignin: 'Torna all’accesso',
    tryAgain: 'Riprova',
    back: 'Indietro',
  },
  validation: {
    email: 'Inserisci un indirizzo email valido.',
    passwordRequired: 'Inserisci la password.',
    passwordMinimum: 'Usa almeno 15 caratteri.',
    passwordMismatch: 'Le password non coincidono.',
    verificationCode: 'Inserisci il codice a 6 cifre.',
    preferredName: 'Inserisci il nome con cui vuoi essere chiamato.',
    firstAction: 'Scrivi cosa vuoi aggiungere prima di continuare.',
  },
  network: {
    offlineTitle: 'Sei offline.',
    offlineBody: 'Riconnettiti per continuare.',
    rateLimitedTitle: 'Troppi tentativi.',
    rateLimitedBody:
      'Attendi prima di riprovare. Il tempo effettivo sarà indicato dal server.',
    serverUnavailableTitle: 'Servizio temporaneamente non disponibile.',
    serverUnavailableBody:
      'Riprova quando il servizio di accesso torna raggiungibile.',
  },
  failure: {
    invalidCredentialsTitle: 'Accesso non riuscito.',
    invalidCredentialsBody: 'Email o password non sono corretti.',
    accountUnavailableTitle: 'Account non disponibile.',
    accountUnavailableBody:
      'Questo account non può aprire una nuova sessione in questo momento.',
    passwordCompromisedTitle: 'Password da aggiornare.',
    passwordCompromisedBody:
      'Per proteggere l’account, questa password non può essere usata per aprire una nuova sessione.',
    existingAccountTitle: 'Account già esistente.',
    existingAccountBody:
      'L’indirizzo è stato verificato. Accedi con l’account già associato a questa email.',
    verificationInvalidTitle: 'Codice non valido o scaduto.',
    verificationInvalidBody:
      'Richiedi un nuovo codice oppure ricomincia la creazione dell’account.',
    recoveryInvalidTitle: 'Link di recupero non valido o scaduto.',
    recoveryInvalidBody:
      'Richiedi un nuovo link per reimpostare la password in sicurezza.',
    requestInvalidTitle: 'Controlla i dati inseriti.',
    requestInvalidBody:
      'La richiesta non rispetta i requisiti di accesso. Controlla i dati e riprova.',
    unexpectedTitle: 'Non è stato possibile completare l’accesso.',
    unexpectedBody: 'Riprova. Se il problema continua, riprova più tardi.',
  },
  locale: {
    control: 'Cambia lingua. Lingua attuale: {{language}}',
    options: 'Lingue disponibili',
    italian: 'Italiano',
    english: 'English',
  },
  legal: {
    prefix: 'Continuando, accetti i',
    terms: 'Termini',
    privacy: 'Privacy',
  },
  verify: {
    title: 'Controlla la tua email',
    body: 'Inserisci il codice a 6 cifre che ti abbiamo inviato per verificare l’indirizzo.',
    resend: 'Invia di nuovo',
    action: 'Verifica e continua',
    privacy: 'Il codice è monouso e scade automaticamente.',
  },
  forgot: {
    title: 'Recupera l’accesso',
    body: 'Ti invieremo un link sicuro per impostare una nuova password.',
    action: 'Invia link di recupero',
    privacy:
      'Se l’indirizzo è associato a un account DANTE, riceverai un link per reimpostare la password.',
  },
  recovery: {
    title: 'Controlla la tua email',
    body: 'Se esiste un account associato all’indirizzo indicato, riceverai le istruzioni per recuperare l’accesso.',
    validatingTitle: 'Verifica del link di recupero',
    validatingBody:
      'Stiamo verificando il link in modo sicuro prima di mostrarti il cambio password.',
  },
  reset: {
    title: 'Crea una nuova password',
    body: 'La nuova password sostituirà quella precedente.',
    new: 'Nuova password',
    confirm: 'Conferma password',
    action: 'Aggiorna password',
    doneTitle: 'Password aggiornata',
    doneBody: 'Ora puoi accedere con la nuova password.',
  },
  providerError: {
    title: 'Accesso non completato',
    body: 'Non siamo riusciti a completare l’accesso con il provider.',
    safe: 'Il tuo account è al sicuro.',
    retry: 'Puoi riprovare o scegliere un altro metodo di accesso.',
  },
  link: {
    title: 'Conferma il collegamento',
    body: 'Esiste già un account DANTE associato a questa email. Accedi prima di collegare il provider.',
    action: 'Accedi e collega',
    other: 'Usa un altro account',
  },
  authenticated: {
    title: 'Accesso confermato',
    body: 'La tua identità è stata confermata. Stiamo preparando il tuo spazio DANTE.',
  },
  reauth: {
    title: 'Conferma di nuovo la tua identità',
    body: 'Per proteggere il tuo account, inserisci di nuovo la password prima di continuare.',
    action: 'Conferma identità',
  },
  setupName: {
    title: 'Come vuoi che DANTE ti chiami?',
    body: 'Serve solo per rendere l’esperienza più naturale. Puoi cambiarlo quando vuoi.',
    label: 'Nome preferito',
  },
  setupLocale: {
    title: 'Lingua e fuso orario',
    body: 'DANTE usa queste informazioni per mostrare orari e date correttamente. Abbiamo precompilato ciò che possiamo rilevare.',
    note: 'Stai confermando solo impostazioni operative; potrai modificarle in seguito.',
    language: 'Lingua',
    timezone: 'Fuso orario',
  },
  setupStart: {
    title: 'Da dove vuoi iniziare?',
    body: 'Scegli una strada. Nessuna di queste decisioni è definitiva.',
  },
  start: {
    real: 'Crea qualcosa di reale',
    realBody: 'Un evento, un’attività, una routine o un obiettivo.',
    import: 'Importa qualcosa che usi già',
    importBody: 'Porta un calendario o un file esistente.',
    demo: 'Fammi vedere una demo rapida',
    demoBody: 'Prova l’interazione senza creare dati reali.',
    skip: 'Esplora da solo',
    skipBody: 'Entra subito in Home. Potrai riprendere la guida più tardi.',
  },
  firstAction: {
    title: 'Crea la tua prima cosa reale',
    body: 'Partiamo da qualcosa di semplice. Potrai aggiungere dettagli dopo.',
    label: 'Cosa vuoi aggiungere?',
    action: 'Crea e apri Home',
  },
  importFlow: {
    title: 'Importa nel tuo spazio',
    body: 'L’import è separato dall’accesso: collegare Google per fare login non autorizza DANTE a leggere il calendario.',
    google:
      'L’import da Google richiederà un’autorizzazione separata e specifica.',
    file: 'Potrai importare un calendario da file senza collegare un account.',
  },
  demo: {
    title: 'Una demo, senza sporcare i tuoi dati',
    body: 'L’elemento qui sotto è solo tutorial e non entra nella tua cronologia reale.',
    item: 'Passeggiata · 18:30',
    itemBody:
      'Puoi aprirla, spostarla, completarla o eliminarla durante il tour.',
    action: 'Avvia demo e apri Home',
  },
  home: {
    title: 'Tutto pronto',
    body: 'Hai completato la configurazione iniziale. Ora puoi entrare nel tuo spazio DANTE.',
    pending: 'Potrai modificare queste impostazioni in seguito.',
  },
} as const;
