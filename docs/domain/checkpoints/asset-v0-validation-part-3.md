<!-- LIFEOS-CANONICAL-CONTINUATION document="asset-v0-validation.md" follows="asset-v0-validation-part-2.md" -->
> **Canonical continuation of the single logical Asset v0 validation document.** Earlier validation remains preserved; this physical continuation records Place / Location downstream closure only.

# 2026-08-16 — Asset ↔ Place downstream closure

Place v0 resolves the historical spatial/property pressure retained by Asset v0.

```text
Asset != Place
Asset identity != current location
Asset identity != address / coordinates / provider Place ID
```

Regression invariants:

- moving an Asset does not manufacture a new Asset;
- correcting an Asset's spatial association does not rewrite Asset identity;
- a Place may be related to an Asset without becoming Asset state source-of-truth universally;
- a building may use both Asset and Place semantics only where both independently matter;
- Place/Asset association grants no automatic Ownership, Authority or Visibility;
- no universal Property/ManagedObject root is introduced.

Historical `Place / Location / Property` pressure is therefore resolved at the general kernel boundary. Legal property/title semantics remain outside the current kernel.

```text
ASSET v0
PASS WITH HARDENING
REOPEN 0
UNCLASSIFIED 0
```

Normative reference: `place-v0-validation.md`.
