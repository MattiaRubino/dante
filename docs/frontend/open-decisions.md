# DANTE — Frontend Open Decisions

**Status:** CURRENT  
**Branch:** `feature/home-react`  
**Updated:** 2026-08-29

This file records intentionally deferred frontend/product decisions. A deferred item must keep truthful behavior until its owning pass or backend contract resolves it.

| ID | Decision / dependency | Current truthful behavior | Owning future pass | Status |
|---|---|---|---|---|
| `shell.search.remote` | Global/personal-data search contract | Shell Search resolves only real local application destinations. Personal-data/backend search is explicitly unavailable. | Backend integration / search vertical | OPEN |
| `shell.create.contract` | Definitive Create entities/workflows and persistence | Global Create exposes discoverable deferred capabilities and performs no fake write. | Relevant verticals | OPEN |
| `shell.account.session` | Real account identity, session and logout | Neutral account icon; identity/session/logout remain unavailable until Access/Auth integration. | Access/Auth integration | OPEN |
| `shell.review.legacy` | Remove, redirect or reframe legacy Review | Review remains visible but deprecated/disabled; no new workflow investment. | Resolution / integration hardening | OPEN |
| `shell.brand.surface` | Final Topbar brand-background polish | Master DANTE logo is preserved. Current shell background treatment is accepted as a temporary frozen P1 visual; further color tuning is optional and must not alter the brand master. | Whole-Home polish | DEFERRED |
| `timeline.quickAdd` | Date/time prefill, command target and persistence | Existing affordance remains frontend/prototype behavior without invented persistence. | Timeline | OPEN |
| `home.ai.integration` | Send/attach/voice/provider contract | No production backend semantics are implied by current Home materialization. | AI conversational surface | OPEN |
| `capture.integration` | Persistence/history/upload/voice | Current surface must not claim durable storage until its contract exists. | Context Rail — Capture | OPEN |
| `resolution.integration` | Mutation/confirmation/correction contract | Current surface does not imply production mutations. | Context Rail — Resolution | OPEN |
| `stage.management` | Mondi/Segnali management APIs and destinations | Home stage remains READ / NAVIGATE / OPEN with no direct management CRUD. | Central Stage / Mondi + Segnali | OPEN |
| `access.home.handoff` | Final authenticated Access → application routing/session handoff | Access stays outside AppShell; no fake authenticated transition is introduced by Home. | Access/Auth integration | OPEN |

## Maintenance rule

Resolve or update an item in the same bounded checkpoint that changes its actual contract. Do not silently implement a deferred backend/product meaning inside a component.
