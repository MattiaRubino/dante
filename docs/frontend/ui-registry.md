# DANTE — Frontend UI Registry

**Status:** current pre-production registry  
**Branch:** `prototype/frontend` with bounded child surface scopes such as `prototype/access-system`  
**Rule:** every active/deprecated prototype UI element must be traceable here or in a linked surface contract.

## Status vocabulary

- `ACTIVE` — part of the current accepted prototype.
- `WORKING` — present, but purpose/name/content is still under explicit review.
- `PROTOTYPE_ONLY` — interaction exists only as local/mock UX; no backend semantics implied.
- `DEPRECATED` — still visible somewhere in the artifact but superseded and scheduled for removal/reconciliation.
- `REMOVED` — no longer present in current accepted UI; history retained.
- `REJECTED` — tested and intentionally not part of the current direction.

## Registry schema

Every durable entry records: technical ID, current visible label (if any), status, purpose, current interaction, and important exclusions/dependencies.

## Home — global shell

| Technical ID | Current label | Status | Current behavior / contract |
|---|---|---|---|
| `home.topbar.brand` | DANTE/LifeOS historical lockup | WORKING | Product identity anchor. Final logo/skin treatment deferred. |
| `home.topbar.create` | Crea | PROTOTYPE_ONLY | Opens the current quick-create popover. No durable write/backend behavior is implied. Semantic overlap with Capture must be reviewed later. |
| `home.topbar.nav.home` | Home | ACTIVE | Current Home navigation anchor. |
| `home.topbar.nav.worlds` | Mondi | WORKING | Current nav prototype; click currently changes active visual state only, not a production route. |
| `home.topbar.nav.today` | Oggi | WORKING | Current nav prototype; temporal vocabulary must not create a second competing Home identity. |
| `home.topbar.search` | Cerca | PROTOTYPE_ONLY | Opens mock search popover; `Ctrl/Cmd+K` also opens it; `Esc`/outside click closes it. |
| `home.topbar.reviewLegacy` | Review Queue / Da rivedere | DEPRECATED | Legacy topbar review popover still exists. It overlaps the accepted `home.contextRail.resolution` role and must be reconciled/removed in a later bounded scope. |
| `home.topbar.launcher` | Tutto LifeOS | WORKING | Opens a placeholder secondary-function launcher; content explicitly remains undefined. |
| `home.topbar.account` | Profilo | PROTOTYPE_ONLY | Opens account/settings menu mock. |

## Home — conversational / AI surface

| Technical ID | Current label | Status | Current behavior / contract |
|---|---|---|---|
| `home.aiSurface` | conversational card | ACTIVE | Global conversational interaction surface over the same semantic product reality; prototype interaction only. |
| `home.aiSurface.handoff` | Continua su | WORKING | Provider handoff menu exposes external-provider options currently represented by ChatGPT / Claude. |
| `home.aiSurface.expand` | — | ACTIVE | Expands/collapses the conversational surface using the existing composition. |
| `home.aiSurface.attach` | — | PROTOTYPE_ONLY | Attachment affordance. |
| `home.aiSurface.voice` | — | PROTOTYPE_ONLY | Voice affordance. |
| `home.aiSurface.send` | — | PROTOTYPE_ONLY | Sends within the local prototype interaction; no production AI/backend contract implied. |

## Home — orientation / current situation

| Technical ID | Current label | Status | Current behavior / contract |
|---|---|---|---|
| `home.orientation` | greeting + viewed-day context | ACTIVE | Stable orientation band tying Home composition to the viewed day. |
| `home.orientation.nowNext` | Ora / Prossimo | WORKING | Current moment and immediate continuation; must not absorb all current-situation relevance. |
| `home.orientation.highlight` | In evidenza | WORKING | Materially relevant attention item; not generic recommendation. |
| `home.orientation.dynamic` | Per te | WORKING | Contextual suggestion/opportunity/discovery role; naming/content still subject to later pass. |
| `home.dayRibbon` | — | ACTIVE | Environmental/day ribbon synchronized to viewed-day context. |

## Home — central stage

| Technical ID | Current label | Status | Current behavior / contract |
|---|---|---|---|
| `home.stage` | — | WORKING | Large central context surface. Purpose is not yet final. B2 owns its redesign/definition. |
| `home.stage.worlds` | WORLDS / Mondi | WORKING | Historical carousel of mixed life-category objects. Interaction exists, but `Worlds` is not accepted domain/IA vocabulary. |
| `home.stage.worlds.previous` | — | PROTOTYPE_ONLY | Previous item / carousel navigation. |
| `home.stage.worlds.next` | — | PROTOTYPE_ONLY | Next item / carousel navigation. |
| `home.stage.worlds.select` | world item | PROTOTYPE_ONLY | Selecting a world updates the contextual right-side stage detail. |
| `home.stage.worlds.open` | — | PROTOTYPE_ONLY | “Open item” affordance; deeper product destination is not yet defined. |
| `home.stage.mode.previous` | — | ACTIVE | Switches central-stage surface backward. |
| `home.stage.mode.next` | — | ACTIVE | Switches central-stage surface forward. |
| `home.stage.stats` | Stats | WORKING | Current chart/stat prototype. B2 will decide whether this remains a separate mode or becomes another projection of meaningful continuity/trajectory. |
| `home.stage.stats.previous` | — | PROTOTYPE_ONLY | Previous statistic/chart. |
| `home.stage.stats.next` | — | PROTOTYPE_ONLY | Next statistic/chart. |

## Home — time / timeline

| Technical ID | Current label | Status | Current behavior / contract |
|---|---|---|---|
| `home.timeline` | — | ACTIVE | Primary temporal projection; 24h continuous timeline with scrolling and nonlinear density. |
| `home.timeline.calendar` | mese/anno | ACTIVE | Opens calendar/date navigation; viewed day is distinct from immutable prototype “today”. |
| `home.timeline.now` | Ora | ACTIVE | Returns temporal viewport to the current prototype instant/day context. |
| `home.timeline.viewOptions` | Vista e legenda | ACTIVE | Opens view-options popover. |
| `home.timeline.splitGroups` | — | ACTIVE | Separates/rejoins timeline by groups while preserving temporal semantics. |
| `home.timeline.resetView` | — | ACTIVE | Restores group/focus view state. |
| `home.timeline.groupFilters` | Focus, Riunioni, Salute, Creatività, Personale, Urgenze | ACTIVE | Visibility/group controls; historical prototype group vocabulary, not domain taxonomy. |
| `home.timeline.zoomOut` | − | ACTIVE | Reduces zoom while preserving semantic anchor. |
| `home.timeline.zoomIn` | + | ACTIVE | Increases zoom while preserving semantic anchor. |
| `home.timeline.expansionHandle` | — | ACTIVE | Horizontal grouped-view expansion control; contextual rail yields space as expansion progresses. |
| `home.timeline.event.open` | event title | ACTIVE | Opens event/detail modal through title-specific interaction. |
| `home.timeline.event.subtasks` | — | ACTIVE | Expands/collapses event subactivities where present. |
| `home.timeline.event.timeEdit` | event time | ACTIVE | Opens anchored body-level time picker; no card reflow. |
| `home.timeline.event.drag` | event body/drag zone | ACTIVE | Moves event with existing snap/cross-day/undo behavior. |
| `home.timeline.undo` | Annulla | ACTIVE | Reverts supported recent time/move operation. |

## Home — contextual rail (B1 accepted)

| Technical ID | Current label | Status | Current behavior / contract |
|---|---|---|---|
| `home.contextRail` | — | ACTIVE | One integrated secondary surface beside the timeline. Full-height relative to the timeline column; disappears/yields space when timeline expands. |
| `home.contextRail.capture` | Cattura | ACTIVE / WORKING NAME | `user -> DANTE`: low-friction capture without requiring classification first. Shows composer + small recent-capture trace. |
| `home.contextRail.capture.input` | Scrivi qualcosa… | ACTIVE | Free-text capture input. |
| `home.contextRail.capture.voice` | — | PROTOTYPE_ONLY | Voice affordance; no production capture backend implied. |
| `home.contextRail.capture.attach` | — | PROTOTYPE_ONLY | Attachment affordance; no production upload backend implied. |
| `home.contextRail.capture.submit` | — | PROTOTYPE_ONLY | Adds the entry to the local recent-capture trace in this prototype. |
| `home.contextRail.capture.history` | Registro completo | WORKING | Explicit deeper-history control. Destination/overlay implementation is deferred. |
| `home.contextRail.resolution` | Da risolvere | ACTIVE / WORKING NAME | `DANTE -> user`: matters that materially benefit from user confirmation/correction/choice. Not a notification feed. |
| `home.contextRail.resolution.count` | 3 | ACTIVE | Count of currently demonstrated unresolved matters. |
| `home.contextRail.resolution.quickOutcome` | Fatto / Parziale / Saltato | PROTOTYPE_ONLY | Real segmented controls for quick Actual-resolution choices in the prototype. |
| `home.contextRail.resolution.confirm` | Conferma | PROTOTYPE_ONLY | Quick confirmation control. |
| `home.contextRail.resolution.correct` | Correggi | PROTOTYPE_ONLY | Opens/represents correction path; deeper correction surface remains deferred. |
| `home.contextRail.resolution.details` | Vedi dettagli | WORKING | Escalation to future standard contextual/deep surface when resolution is too complex for the rail. |

### Context-rail exclusions

The accepted rail must **not** become:

- generic notifications;
- generic reminders;
- `Ora/Prossimo`;
- `In evidenza`;
- `Per te`;
- a metrics dashboard;
- an AI feed/transcript;
- a duplicate calendar/task list;
- a permanent container for every unresolved fact.

## Home — overlays / transient surfaces currently present

| Technical ID | Current label | Status | Current behavior / contract |
|---|---|---|---|
| `home.overlay.search` | search popover | PROTOTYPE_ONLY | Topbar search mock. |
| `home.overlay.create` | create popover | PROTOTYPE_ONLY | Topbar create mock. |
| `home.overlay.reviewLegacy` | review popover | DEPRECATED | Legacy duplicate to reconcile with Context Rail. |
| `home.overlay.launcher` | Tutto LifeOS | WORKING | Placeholder. |
| `home.overlay.account` | account menu | PROTOTYPE_ONLY | Settings/profile mock. |
| `home.overlay.calendar` | calendar popover | ACTIVE | Date navigation. |
| `home.overlay.timelineOptions` | Vista e legenda | ACTIVE | Timeline view controls. |
| `home.overlay.timePicker` | Inizio/Fine | ACTIVE | Anchored precise time editing. |
| `home.overlay.eventDetail` | event modal | ACTIVE | Event detail surface in the existing prototype. |
| `home.feedback.moveToast` | Annulla | ACTIVE | Temporary feedback + undo. |

## Rejected / superseded in B1

| Technical ID / old label | Status | Replacement / reason |
|---|---|---|
| side `Appunti` card | REMOVED | Replaced by `home.contextRail.capture`; old card was too note-centric and visually separate. |
| side `Review` card | REMOVED | Replaced by `home.contextRail.resolution`; old generic review framing was weaker. |
| `home.contextRail.focusExpand` | REJECTED | Focus/expand chevrons were ambiguous and created unnecessary state. Accepted rail keeps both functions visible. |
| short rail ending mid-column | REJECTED | Accepted rail stretches with the timeline column to avoid arbitrary empty lower space. |

## Access — A3.4 selected review checkpoint

The detailed Access behavior contract lives in `docs/frontend/access/contract.md`. The rows below are the global inventory anchors.

| Technical ID | Current label | Status | Current behavior / contract |
|---|---|---|---|
| `access.signIn` | Accedi a DANTE | ACTIVE / PRE-PRODUCTION | Existing-account entry via Google, Apple or email/password. Provider UI remains provider-owned. |
| `access.signUpEmail` | Crea il tuo account DANTE | ACTIVE / PRE-PRODUCTION | First DANTE-owned account-creation step; validates email before password. |
| `access.signUpPassword` | Proteggi il tuo account | ACTIVE / PRE-PRODUCTION | Long-password/password-manager-friendly review UX; exact backend policy not frozen. |
| `access.verifyEmail` | Controlla la tua email | ACTIVE / PRE-PRODUCTION | Six-digit review UX with paste/advance/resend behavior; OTP backend semantics not frozen. |
| `access.forgotPassword` | Recupera l’accesso | ACTIVE / PRE-PRODUCTION | Starts recovery without revealing account existence. |
| `access.recoverySent` | Controlla la tua email | ACTIVE / PRE-PRODUCTION | Neutral recovery acknowledgement. |
| `access.resetPassword` | Crea una nuova password | ACTIVE / PRE-PRODUCTION | Recovery reset screen. |
| `access.resetComplete` | Password aggiornata | ACTIVE / PRE-PRODUCTION | Returns user toward normal sign-in; no prototype auto-login contract. |
| `access.providerPending` | provider pending | PROTOTYPE_ONLY | DANTE-side provider launch/wait state; no fake chooser/consent UI. |
| `access.providerError` | Accesso non completato | PROTOTYPE_ONLY | Provider cancellation/failure return. |
| `access.accountLink` | Conferma il collegamento | PROTOTYPE_ONLY | Collision/linking UX; silent account merge explicitly excluded. |
| `access.reauth` | Sessione scaduta | PROTOTYPE_ONLY | Re-auth overlay over existing application context. |
| `access.setupName` | Nome preferito | ACTIVE / PRE-PRODUCTION | Lightweight post-account setup. |
| `access.setupLocale` | Lingua e fuso orario | ACTIVE / PRE-PRODUCTION | Operational locale/time-zone confirmation. |
| `access.setupStart` | Da dove vuoi iniziare? | ACTIVE / PRE-PRODUCTION | First-run branch to real item/import/demo/skip. |
| `access.firstAction` | Crea la tua prima cosa reale | PROTOTYPE_ONLY | First real item review path. |
| `access.import` | Importa nel tuo spazio | PROTOTYPE_ONLY | Separate import path; sign-in provider consent does not imply import authorization. |
| `access.demo` | Una demo, senza sporcare i tuoi dati | PROTOTYPE_ONLY | Tutorial-only item isolated from real history. |
| `access.homeHandoff` | Tutto pronto | PROTOTYPE_ONLY | Access/first-run completion mock only; accepted Home implementation is unchanged. |
| `access.brand.cornerMark` | — | ACTIVE / VISUAL | Desktop-only cropped locked Living Orbits symbol. A3.4 selected opacity: `0.22` desktop / `0.18` compact desktop; hidden with brand stage at `<=900px`. |
| `access.localeSelector` | Italiano / English | ACTIVE / PRE-PRODUCTION | Switches the complete review UI between IT/EN dictionaries. |

### Access exclusions

The selected Access review must **not** imply:

- provider sign-in grants Calendar/Gmail/iCloud access;
- DANTE owns the provider chooser/consent screen;
- the prototype password/OTP values are frozen backend policy;
- onboarding/profile data is required before account creation;
- the `home` handoff mock replaces the accepted Home artifact;
- A3.5 full-opacity brand background is accepted.

## Maintenance rule

When any row changes, update this registry and the linked surface contract/changelog in the same write. Never leave a stale row because the prototype “still looks right.”
