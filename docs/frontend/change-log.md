# DANTE — Frontend Change Log

Append-only operational history. This is not a Git substitute; it records product/UI meaning.

## 2026-08-19 — A1 workstream migration

- `ADDED` `prototype/frontend` as active pre-production frontend workstream.
- `DEPRECATED` `prototype/phase-4-today-home` as active branch; retained as historical evidence.
- `ADDED` frontend research index and migrated Phase 4 interaction references.
- `ADDED` exact corrected Home baseline.

## 2026-08-19 — A2 modular source

- `ADDED` deterministic modular/copy-on-write Home work source.
- `ADDED` named CSS/JS module map and build QA.
- `CHANGED` workflow so the complete standalone artifact is retained while work can happen in bounded modules.
- `VISUAL_ONLY`: none.
- `BEHAVIOR_CHANGED`: none.

## 2026-08-19 — B1 Context Rail v1

- `REMOVED` old side `Appunti` card from the accepted B1 output.
- `REMOVED` old side `Review` card from the accepted B1 output.
- `ADDED` `home.contextRail` as one integrated secondary surface.
- `ADDED` `home.contextRail.capture` (`user -> DANTE`) with free capture, voice/attachment affordances, submit and recent-capture trace.
- `ADDED` `home.contextRail.resolution` (`DANTE -> user`) with unresolved count, real quick-action controls and deeper-detail affordance.
- `CHANGED` rail height to stretch with the timeline column instead of leaving arbitrary unused lower space.
- `REJECTED` focus/expand chevrons and the hidden balanced/focus state machine because the interaction was ambiguous and added no clear user value.
- `DEPRECATED` topbar legacy Review Queue as a duplicate concept; it remains physically present until a later explicit cleanup scope.
- `NO_CHANGE` timeline semantics, calendar/day ribbon, timeline toolbar, current `Worlds`/`Stats`, global brand/skin and backend semantics.

## 2026-08-19 — documentation invariant

- `ADDED` permanent frontend operational rule: registry + surface contract + terminology/localization/tokens + append-only history must stay synchronized with implementation.
- `ADDED` stable English technical IDs independent from visible labels.
- `ADDED` localization and semantic design-token authorities for new/touched UI.

## 2026-08-20 — Access A3.4 selected review checkpoint

- `ADDED` complete Access review contract/state model covering sign-in, DANTE-owned staged sign-up, verification, recovery/reset, provider handoff/error/linking, re-auth and lightweight first-run handoff.
- `ADDED` Italian/English `access.*` locale registry mirrored from the selected standalone prototype.
- `ADDED` semantic `--dante-access-*` token family for the reviewed light Access surface without changing Home token values.
- `ADDED` exact hash-verified A3.4 standalone archive and browser QA evidence.
- `CHANGED` Access selected checkpoint from A3.1 to A3.4.
- `VISUAL_ONLY` replaced the generic desktop orbit decoration with a large cropped locked Living Orbits symbol at the selected muted opacity.
- `REJECTED` A3.5 full-opacity corner-mark experiment as too visually dominant.
- `NO_CHANGE` Home/B1/B2 implementation, backend auth/session/provider contracts, production React/framework choice and locked brand masters.

## 2026-08-20 — Mobile Access M1.2 + PRG-0

- `ADDED` Mobile Access as a platform-native expression of the existing Access semantic system rather than a scaled desktop UI.
- `ADDED` mobile technical contract covering client↔backend capabilities, session lifecycle, provider/OAuth, deep links, offline/error taxonomy, lifecycle, accessibility, privacy and security test obligations.
- `ADDED` mobile-specific UI/behavior registry without forking global Access semantic IDs.
- `ADDED` PRG-0 production-readiness gate with threat/abuse model, account/session lifecycle consequences, assurance targets, pinning/attestation decision gates and implementation release gates.
- `CHANGED` future implementation password policy from the A3.4 historical 15+ review copy to the approved DANTE V1 `12+` policy, with no composition checklist, >=64 support, password-manager/paste support and required common/breached-password server checks.
- `DOCUMENTED` the 12+ password-only policy as a deliberate variance from the current NIST 15-character baseline; no false compliance claim.
- `ADDED` OWASP MASVS v2 + MAS Testing Profile assurance target for native clients and OWASP ASVS 5.0.0 Level-2 alignment target for backend with explicit exception register rather than false compliance.
- `DOCUMENTED` current MFA/passkey absence as an ASVS `V6.3.3` exception until an accepted mechanism exists; compensating controls and MFA/passkey-ready architecture are required.
- `ADDED` endpoint-pinning and Play Integrity/App Attest risk-signal gates with safe rotation/degraded-mode requirements.
- `HARDENED` mobile reauth dialog semantics, AutoFill metadata, offline localization parity and security-safe Escape/cancel behavior.
- `ADDED` exact hash-verified M1.2 PRG-0 archive plus executable-baseline and static/mechanical QA evidence.
- `QA` immediately preceding M1.2 browser suite passed 30/30; final PRG-0 bytes pass 18/18 static/mechanical checks. A final Chromium rerun was environment-blocked and is explicitly not misreported as executed.
- `NO_CHANGE` accepted Home implementation, backend code, locked brand masters, A3.4 historical bytes, production framework choice or concrete API route/token/schema design.
- `STATUS` Access is now frozen for ordinary implementation as a **production-ready specification / pre-implementation**; native/backend release verification remains mandatory before any production-software claim.
