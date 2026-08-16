<!-- LIFEOS-CANONICAL-CONTINUATION document="asset.md" follows="asset.md" -->
> **Canonical continuation of the single logical Asset document.** Earlier Asset v0 semantics remain preserved; this physical continuation records Ownership / Possession / Custody integration only.

# 2026-08-16 — Ownership / Possession / Custody integration

Asset v0 already established a native identity for individually tracked non-human physical objects where identity/history matter. Ownership / Possession / Custody v0 now closes the previously deferred relations around that identity.

```text
Asset
= native physical-object identity

Ownership
= specific contextual owner relation

Possession
= specific contextual actual holding relation

Custody
= bounded entrusted/safeguarding profile
  composed from holding + applicable Responsibility/governance basis
```

Mandatory non-collapse:

```text
Asset != Ownership
Asset != Possession
Asset != Custody
owner change != new Asset
possessor change != new Asset
custodian change != new Asset
```

A materially continuous Asset may be sold, lent, returned, possessed by another Actor or placed in custody while retaining its native identity.

Conversely, preservation of Asset identity does not silently preserve Ownership/Possession/Custody state when those relations materially change.

Resource role remains contextual:

```text
Asset may play Resource
Ownership != Resource role
Possession != Resource Allocation
Possession != Actual use universally
```

Ownership/Possession/Custody grant no universal Responsibility, Coordination Stewardship, Authority or Visibility.

Asset v0 remains **PASS WITH HARDENING, REOPEN = 0**.

Normative downstream references:

- `ownership.md`;
- `possession.md`;
- `../checkpoints/ownership-possession-custody-v0-validation.md`.
