# DANTE — Frontend UI Registry

**Status:** current production-depth registry  
**Branch:** `feature/home-react`  
**Rule:** every active/deprecated frontend UI element must be traceable here or in a linked surface contract.

## Status vocabulary

- `ACTIVE` — part of the current accepted implementation/contract.
- `WORKING` — present, but purpose/name/content is still under explicit review.
- `PROTOTYPE_ONLY` — interaction exists only as local/mock UX; no backend semantics implied.
- `DEFERRED` — visible/discoverable capability whose real owning vertical or backend contract is intentionally not implemented yet.
- `DEPRECATED` — still visible but superseded and scheduled for removal/reconciliation.
- `REMOVED` — no longer present in current accepted UI; history retained.
- `REJECTED` — tested and intentionally not part of the current direction.

## Registry schema

Every durable entry records: technical ID, current visible label (if any), status, purpose, current interaction, and important exclusions/dependencies.

## Home — global shell / AppShell P1

P1 implementation is frozen at `e11d6c53d2fe1361b37345bbc3f49792541bd45d`. Closure details: `docs/frontend/app-shell/p1-global-app-shell.md`.

| Technical ID | Current label | Status | Current behavior / contract |
|---|---|---|---|
| `home.topbar.shell` | — | ACTIVE | Shared persistent AppShell infrastructure outside Home feature ownership. Owns the Global Topbar and route outlet for application pages; Access `/` remains outside AppShell. |
| `home.topbar.brand` | DANTE | ACTIVE | Product identity anchor using the approved DANTE master symbol/wordmark assets without recoloring the master. Current Topbar background treatment is accepted P1 polish and may be revisited later without altering brand geometry/colors. |
| `home.topbar.create` | Crea | DEFERRED | Opens the shared Create capability menu. Capabilities are discoverable but intentionally perform no fake persistence/write until their owning verticals exist. |
| `home.topbar.nav.home` | Home | ACTIVE | Real router navigation to `/home`, with normal browser history/deep-link semantics. |
| `home.topbar.nav.worlds` | Mondi | ACTIVE | Real router destination `/worlds`. The destination is routable now; the actual Mondi vertical remains a later production-depth pass. |
| `home.topbar.nav.today` | Oggi | ACTIVE | Real router destination `/today`. The route exists without inventing the future Oggi/day vertical implementation. |
| `home.topbar.search` | lens / Cerca in DANTE | ACTIVE | Lens trigger enters inline Topbar Search mode; primary nav is temporarily replaced by the search field. `/` and Ctrl/Cmd+K are supported. Local destinations are searched live; Arrow Up/Down, Enter, Escape and click are supported. Remote/personal-data search is explicitly unavailable until backend integration. |
| `home.topbar.reviewLegacy` | Review | DEPRECATED | Legacy Review remains visible/disabled bounded debt. It overlaps the accepted Resolution role and must later be removed, redirected or reframed; no new workflow investment in P1. |
| `home.topbar.launcher` | launcher | ACTIVE | Opens the shared DANTE application launcher using real local router destinations. |
| `home.topbar.account` | Account | ACTIVE / DEFERRED SESSION | Opens the shared account menu with a neutral user icon. Profile/settings destinations are real; identity/avatar/session/logout semantics remain deferred to Access/Auth. |

## Home — conversational / AI surface

| Technical ID | Current label | Status | Current behavior / contract |
|---|---|---|---|
| `home.aiSurface` | conversational card | ACTIVE | Global conversational interaction surface over the same semantic product reality; current Home materialization is frontend-local until its production-depth AI pass. |
| `home.aiSurface.handoff` | Continua su | WORKING | Provider handoff menu exposes external-provider options currently represented by ChatGPT / Claude. |
| `home.aiSurface.expand` | — | ACTIVE | Expands/collapses the conversational surface using the existing composition. |
| `home.aiSurface.attach` | — | PROTOTYPE_ONLY | Attachment affordance. |
| `home.aiSurface.voice` | — | PROTOTYPE_ONLY | Voice affordance. |
| `home.aiSurface.send` | — | PROTOTYPE_ONLY | Local/prototype interaction only; no production AI/backend contract implied. |

## Home — orientation / current situation

| Technical ID | Current label | Status | Current behavior / contract |
|---|---|---|---|
| `home.orientation` | greeting + viewed-day context | ACTIVE | Stable orientation band tying Home composition to the viewed day. |
| `home.orientation.nowNext` | Ora / Prossimo | WORKING | Current moment and immediate continuation; must not absorb all current-situation relevance. |
| `home.orientation.highlight` | In evidenza | WORKING | Materially relevant attention item; not generic recommendation. |
| `home.orientation.dynamic` | Per te | WORKING | Contextual suggestion/opportunity/discovery role; naming/content still subject to later pass. |
| `home.dayRibbon` | — | ACTIVE | Environmental/day ribbon synchronized to viewed-day context. P2 owns production-depth day-route/state behavior. |

## Home — central stage

Current working oracle: **B2 v27 infrastructure color over v26 edge over v25 shell/timeline over v24 visual skin over v23 branding over v22 no persistent add**. Accepted macro geometry remains frozen; component-specific fidelity is closed in its own production-depth pass.

| Technical ID | Current label | Status | Current behavior / contract |
|---|---|---|---|
| `home.stage` | — | WORKING | Shared central workspace and sole owner of outer stage geometry, selector anchor and lateral navigation anchors. Home-stage role is read/navigate/open; it is not a configuration CRUD surface. |
| `home.stage.continuity` | Mondi | WORKING / LOCKED NAME | Carried-forward significant realities the user wants readily recoverable/resumable. Current visual grammar preserves the sphere carousel. Partial state renders only real items. Not a Domain Model taxonomy and not necessarily a persisted `World` entity. |
| `home.stage.continuity.previous` | — | PROTOTYPE_ONLY | Previous continuity item/carousel navigation. |
| `home.stage.continuity.next` | — | PROTOTYPE_ONLY | Next continuity item/carousel navigation. |
| `home.stage.continuity.select` | mondo | PROTOTYPE_ONLY | Selects/centers a visible continuity item in the local frontend materialization. |
| `home.stage.continuity.open` | — | PROTOTYPE_ONLY | Existing deeper-open affordance lineage; final destination remains undefined. |
| `home.stage.mode.previous` | — | ACTIVE | Switches central-stage projection backward without moving the stage shell/anchors. |
| `home.stage.mode.next` | — | ACTIVE | Switches central-stage projection forward without moving the stage shell/anchors. |
| `home.stage.signals` | Segnali | WORKING / LOCKED NAME | Compact analytical projection for values/deltas/trends/targets/planned-vs-actual/cautious patterns. Current desktop composition shows at most three complete visible items. No persistent add/configure control is part of Home. |
| `home.stage.signals.previous` | — | PROTOTYPE_ONLY | Previous Signal using the same carousel navigation grammar. |
| `home.stage.signals.next` | — | PROTOTYPE_ONLY | Next Signal using the same carousel navigation grammar. |
| `home.stage.signals.select` | segnale | PROTOTYPE_ONLY | Selects/centers a Signal in the local frontend materialization. |

Stage management rule:

- no persistent `+` in Home for Mondi, Segnali or future projections by default;
- `partial` means the real items that exist, not visual capacity slots;
- `full/overflow` keeps normal projection navigation;
- a true `empty` state may expose a contextual CTA that opens the dedicated management/creation surface;
- that CTA is a navigation/management-entry intent, not a direct Home mutation;
- Mondi and Segnali management surfaces own creation/configuration/order/removal.

The timeline `+` is outside this central-stage rule: it belongs to the temporal surface and does not create a Mondi/Segnali capacity/add slot.

Historical `home.stage.worlds` / `home.stage.stats` implementation vocabulary is deprecated by the projection IDs above; historical files/checkpoints remain evidence.

## Home — time / timeline

| Technical ID | Current label | Status | Current behavior / contract |
|---|---|---|---|
| `home.timeline` | — | ACTIVE | Primary temporal projection; 24h continuous timeline with scrolling and nonlinear density. |
| `home.timeline.calendar` | mese/anno | ACTIVE | Opens calendar/date navigation; viewed day is distinct from real/current “today”. |
| `home.timeline.now` | Ora | ACTIVE | Returns temporal viewport toward current day/time context within the existing frontend behavior. |
| `home.timeline.quickAdd` | + | PROTOTYPE_ONLY | Real contextual timeline affordance. Final production date/time prefill, destination, command and persistence semantics are explicitly not defined yet. |
| `home.timeline.viewOptions` | Vista e legenda | ACTIVE | Opens view-options popover. |
| `home.timeline.splitGroups` | — | ACTIVE | Separates/rejoins timeline by groups while preserving temporal semantics. |
| `home.timeline.resetView` | — | ACTIVE | Restores group/focus view state. |
| `home.timeline.groupFilters` | Focus, Riunioni, Salute, Creatività, Personale, Urgenze | ACTIVE | Visibility/group controls; historical prototype group vocabulary, not domain taxonomy. |
| `home.timeline.zoomOut` | − | ACTIVE | Reduces zoom while preserving semantic anchor. |
| `home.timeline.zoomIn` | + | ACTIVE | Increases zoom while preserving semantic anchor. |
| `home.timeline.expansionHandle` | — | ACTIVE | Horizontal grouped-view expansion control; contextual rail yields space as expansion progresses. |
| `home.timeline.event.open` | event title | ACTIVE | Opens event/detail surface through title-specific interaction. |
| `home.timeline.event.subtasks` | — | ACTIVE | Expands/collapses event subactivities where present. |
| `home.timeline.event.timeEdit` | event time | ACTIVE | Anchored precise time-edit interaction in the current frontend lineage. |
| `home.timeline.event.drag` | event body/drag zone | ACTIVE | Moves event with existing frontend snap/cross-day/undo behavior. |
| `home.timeline.undo` | Annulla | ACTIVE | Reverts supported recent time/move operation. |

## Home — contextual rail

| Technical ID | Current label | Status | Current behavior / contract |
|---|---|---|---|
| `home.contextRail` | — | ACTIVE | One integrated secondary surface beside the timeline. Full-height relative to the timeline column; disappears/yields space when timeline expands. |
| `home.contextRail.capture` | Cattura | ACTIVE / WORKING NAME | `user -> DANTE`: low-friction capture without requiring classification first. Shows composer + small recent-capture trace. |
| `home.contextRail.capture.input` | Scrivi qualcosa… | ACTIVE | Free-text capture input. |
| `home.contextRail.capture.voice` | — | PROTOTYPE_ONLY | Voice affordance; no production capture backend implied. |
| `home.contextRail.capture.attach` | — | PROTOTYPE_ONLY | Attachment affordance; no production upload backend implied. |
| `home.contextRail.capture.submit` | — | PROTOTYPE_ONLY | Local frontend capture behavior; no durable persistence implied. |
| `home.contextRail.capture.history` | Registro completo | WORKING | Explicit deeper-history control. Destination/overlay implementation is deferred. |
| `home.contextRail.resolution` | Da risolvere | ACTIVE / WORKING NAME | `DANTE -> user`: matters that materially benefit from user confirmation/correction/choice. Not a notification feed. |
| `home.contextRail.resolution.count` | 3 | ACTIVE | Count of currently demonstrated unresolved matters. |
| `home.contextRail.resolution.quickOutcome` | Fatto / Parziale / Saltato | PROTOTYPE_ONLY | Frontend segmented controls for quick Actual-resolution choices; no production mutation implied. |
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
| `home.overlay.search` | inline Search results | ACTIVE | No modal/backdrop. Results are anchored below the inline Topbar Search field; local destinations only until remote-search integration exists. |
| `home.overlay.create` | create menu | DEFERRED | Shared AppShell menu; no fake backend write. |
| `home.overlay.reviewLegacy` | Review | DEPRECATED | Legacy behavior is bounded/disabled pending reconciliation with Resolution. |
| `home.overlay.launcher` | launcher | ACTIVE | Shared AppShell launcher using real application routes. |
| `home.overlay.account` | account menu | ACTIVE / DEFERRED SESSION | Profile/settings routing is real; identity/session/logout is deferred to Access/Auth. |
| `home.overlay.calendar` | calendar popover | ACTIVE | Date navigation; P2 owns viewed-day production-depth state/routing semantics. |
| `home.overlay.timelineOptions` | Vista e legenda | ACTIVE | Timeline view controls. |
| `home.overlay.timePicker` | Inizio/Fine | ACTIVE | Anchored precise time editing in current frontend behavior. |
| `home.overlay.eventDetail` | event detail | ACTIVE | Event detail surface in the existing Home lineage. |
| `home.feedback.moveToast` | Annulla | ACTIVE | Temporary feedback + undo. |

## Rejected / superseded

| Technical ID / old label | Status | Replacement / reason |
|---|---|---|
| Home-owned `global-topbar` component | REMOVED | Global Topbar ownership moved to shared `apps/web/src/app-shell/` in P1. |
| modal `SearchCommandDialog` / dialog backdrop | REMOVED | Replaced in P1 visual polish by inline expanding Topbar Search + anchored results panel. |
| fake account initials `MR` | REMOVED | Replaced by neutral user icon until real Access/Auth identity exists. |
| side `Appunti` card | REMOVED | Replaced by `home.contextRail.capture`; old card was too note-centric and visually separate. |
| side `Review` card | REMOVED | Replaced by `home.contextRail.resolution`; old generic review framing was weaker. |
| `home.contextRail.focusExpand` | REJECTED | Focus/expand chevrons were ambiguous and created unnecessary state. Accepted rail keeps both functions visible. |
| short rail ending mid-column | REJECTED | Accepted rail stretches with the timeline column to avoid arbitrary empty lower space. |
| generic `Stats` stage framing | DEPRECATED | Replaced by the more meaningful `home.stage.signals` / Segnali projection. |
| `home.stage.continuity.emptySlot` / ghost `+` | REMOVED | Partial state renders only real items; creation/configuration belongs to dedicated management surfaces. |

## Maintenance rule

When any row changes, update this registry and the linked surface contract/changelog in the same checkpoint write. Never leave a stale row because the frontend “still looks right.”
