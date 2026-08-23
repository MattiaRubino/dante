# DANTE — Frontend UI Registry

**Status:** current pre-production registry  
**Branch:** `prototype/frontend`  
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
| `home.topbar.shell` | — | ACTIVE | B2 v25 application shell: real sticky top app bar, edge-to-edge at shell level with 24 px internal horizontal inset. DANTE + Search live left, Home/Mondi/Oggi remain centered, utility actions live right. Existing controls are moved/reused rather than duplicated. |
| `home.topbar.brand` | DANTE | ACTIVE | Product identity anchor. B2 v23 uses the approved DANTE symbol geometry with approved charcoal/orange fills plus approved wordmark geometry rendered white for the current dark surface. No extra backing panel; the white wordmark is a frontend dark-surface derivative, not a new brand master. |
| `home.topbar.create` | Crea | PROTOTYPE_ONLY | Opens the current quick-create popover. B2 v25 places it as the first control in the right utility group, before legacy Review. No durable write/backend behavior is implied; final Create-vs-Capture and timeline-context semantics remain separate decisions. |
| `home.topbar.nav.home` | Home | ACTIVE | Current Home navigation anchor. |
| `home.topbar.nav.worlds` | Mondi | WORKING | Current nav prototype; click currently changes active visual state only, not a production route. |
| `home.topbar.nav.today` | Oggi | WORKING | Current nav prototype; temporal vocabulary must not create a second competing Home identity. |
| `home.topbar.search` | Cerca | PROTOTYPE_ONLY | B2 v25 places Search immediately after DANTE on the left. Opens mock search popover; `Ctrl/Cmd+K` also opens it; `Esc`/outside click closes it. |
| `home.topbar.reviewLegacy` | Review Queue / Da rivedere | DEPRECATED | Legacy topbar review popover still exists. It overlaps the accepted `home.contextRail.resolution` role and must be reconciled/removed in a later bounded scope. |
| `home.topbar.launcher` | Tutto LifeOS | WORKING | Placeholder secondary-function launcher. B2 v23-v25 do not perform a blind global rename; this historical string remains a later explicit cleanup item. |
| `home.topbar.account` | Profilo | PROTOTYPE_ONLY | Opens account/settings menu mock. |

## Home — conversational / AI surface

| Technical ID | Current label | Status | Current behavior / contract |
|---|---|---|---|
| `home.aiSurface` | conversational card | ACTIVE | Global conversational interaction surface over the same semantic product reality; prototype interaction only. B2 v23 identity treatment is the approved DANTE symbol only, with no visible `LifeOS`/`DANTE` text label beside it. |
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

Current working oracle: **B2 v25 shell/timeline over B2 v24 visual skin over B2 v23 branding over B2 v22 no persistent add**. B2 remains open for remaining details and final responsive/visual/accessibility QA.

| Technical ID | Current label | Status | Current behavior / contract |
|---|---|---|---|
| `home.stage` | — | WORKING | Shared central workspace and sole owner of outer stage geometry, selector anchor and lateral navigation anchors. Home-stage role is read/navigate/open; it is not a configuration CRUD surface. |
| `home.stage.continuity` | Mondi | WORKING / LOCKED NAME | Carried-forward significant realities the user wants readily recoverable/resumable. Current visual grammar preserves the existing sphere carousel. Partial state renders only real items. Not a Domain Model taxonomy and not necessarily a persisted `World` entity. |
| `home.stage.continuity.previous` | — | PROTOTYPE_ONLY | Previous continuity item/carousel navigation. |
| `home.stage.continuity.next` | — | PROTOTYPE_ONLY | Next continuity item/carousel navigation. |
| `home.stage.continuity.select` | mondo | PROTOTYPE_ONLY | Selects/centers a visible continuity item in the local prototype. |
| `home.stage.continuity.open` | — | PROTOTYPE_ONLY | Existing deeper-open affordance lineage; final destination remains undefined. |
| `home.stage.mode.previous` | — | ACTIVE | Switches central-stage projection backward without moving the stage shell/anchors. |
| `home.stage.mode.next` | — | ACTIVE | Switches central-stage projection forward without moving the stage shell/anchors. |
| `home.stage.signals` | Segnali | WORKING / LOCKED NAME | Compact analytical projection for values/deltas/trends/targets/planned-vs-actual/cautious patterns. Current desktop composition shows at most three complete visible items. No persistent add/configure control is part of Home. |
| `home.stage.signals.previous` | — | PROTOTYPE_ONLY | Previous Signal using the same carousel navigation grammar. |
| `home.stage.signals.next` | — | PROTOTYPE_ONLY | Next Signal using the same carousel navigation grammar. |
| `home.stage.signals.select` | segnale | PROTOTYPE_ONLY | Selects/centers a Signal in the local prototype. |

Stage management rule:

- no persistent `+` in Home for Mondi, Segnali or future projections by default;
- `partial` means the real items that exist, not visual capacity slots;
- `full/overflow` keeps normal projection navigation;
- a true `empty` state may expose a contextual CTA that opens the dedicated management/creation surface;
- that CTA is a navigation/management-entry intent, not a direct Home mutation;
- Mondi and Segnali management surfaces own creation/configuration/order/removal.

The B2 v25 timeline `+` is outside this central-stage rule: it belongs to the temporal surface and does not create a Mondi/Segnali capacity/add slot.

Historical `home.stage.worlds` / `home.stage.stats` implementation vocabulary is deprecated by the B2 projection IDs above; historical files/checkpoints remain evidence.

## Home — time / timeline

| Technical ID | Current label | Status | Current behavior / contract |
|---|---|---|---|
| `home.timeline` | — | ACTIVE | Primary temporal projection; 24h continuous timeline with scrolling and nonlinear density. |
| `home.timeline.calendar` | mese/anno | ACTIVE | Opens calendar/date navigation; viewed day is distinct from immutable prototype “today”. B2 v25 places it after the contextual add column in the temporal-header grid. |
| `home.timeline.now` | Ora | ACTIVE | Returns temporal viewport to the current prototype instant/day context. B2 v25 keeps it in the same temporal-header grid immediately after month/year. |
| `home.timeline.quickAdd` | + | PROTOTYPE_ONLY | B2 v25 real contextual timeline button. It is the first item in the temporal-header grid (`add / month / now / week / actions`) and currently bridges to the existing global `Crea` popover. Final production date/time prefill, destination, command and persistence semantics are explicitly not defined yet. |
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
| `home.overlay.create` | create popover | PROTOTYPE_ONLY | Topbar create mock; also reused by the v25 timeline quick-add as a temporary prototype bridge. |
| `home.overlay.reviewLegacy` | review popover | DEPRECATED | Legacy duplicate to reconcile with Context Rail. |
| `home.overlay.launcher` | Tutto LifeOS | WORKING | Historical placeholder; B2 v23-v25 intentionally do not perform a global blind rename. |
| `home.overlay.account` | account menu | PROTOTYPE_ONLY | Settings/profile mock. |
| `home.overlay.calendar` | calendar popover | ACTIVE | Date navigation. |
| `home.overlay.timelineOptions` | Vista e legenda | ACTIVE | Timeline view controls. |
| `home.overlay.timePicker` | Inizio/Fine | ACTIVE | Anchored precise time editing. |
| `home.overlay.eventDetail` | event modal | ACTIVE | Event detail surface in the existing prototype. |
| `home.feedback.moveToast` | Annulla | ACTIVE | Temporary feedback + undo. |

## Rejected / superseded

| Technical ID / old label | Status | Replacement / reason |
|---|---|---|
| side `Appunti` card | REMOVED | Replaced by `home.contextRail.capture`; old card was too note-centric and visually separate. |
| side `Review` card | REMOVED | Replaced by `home.contextRail.resolution`; old generic review framing was weaker. |
| `home.contextRail.focusExpand` | REJECTED | Focus/expand chevrons were ambiguous and created unnecessary state. Accepted rail keeps both functions visible. |
| short rail ending mid-column | REJECTED | Accepted rail stretches with the timeline column to avoid arbitrary empty lower space. |
| generic `Stats` stage framing | DEPRECATED | Replaced by the more meaningful `home.stage.signals` / Segnali projection. |
| `home.stage.continuity.emptySlot` / ghost `+` | REMOVED | v22 removes capacity/add slots from Home central stage. Partial state renders only real items; creation/configuration belongs to dedicated management surfaces. |

## Maintenance rule

When any row changes, update this registry and the linked surface contract/changelog in the same checkpoint write. Never leave a stale row because the prototype “still looks right.”
