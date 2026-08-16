<!-- LIFEOS-CANONICAL-CONTINUATION document="resource-v0-validation.md" follows="resource-v0-validation-part-3.md" -->
> **Canonical continuation of the single logical Resource v0 validation document.** Earlier validation remains preserved; this physical continuation records Place integration only.

# 2026-08-16 — Resource ↔ Place downstream closure

Place v0 supplies the native spatial identity that Resource v0 intentionally left open for rooms/sites/venues.

```text
Place != Resource
Place may play Resource role
```

Regression invariants:

- Place identity exists independently of Resource candidacy/Allocation/Reservation;
- bookability/capacity does not create Place identity;
- Place may be unavailable as Resource while remaining the same Place;
- Resource substitution does not rewrite Place identity/history;
- Visibility of a Place does not automatically expose capacity sources/private events;
- no universal Room/Resource entity is introduced.

Historical `Place/Service/Skill native semantics` pressure is resolved for Place only; Service/Skill remain governed by their existing independent dispositions/stages.

```text
RESOURCE v0
PASS WITH HARDENING
REOPEN 0
UNCLASSIFIED 0
```

Normative reference: `place-v0-validation.md`.
