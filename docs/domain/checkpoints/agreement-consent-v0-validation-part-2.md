<!-- LIFEOS-CANONICAL-CONTINUATION document="agreement-consent-v0-validation.md" follows="agreement-consent-v0-validation.md" -->
> **Canonical continuation of the single logical Agreement / Consent v0 validation checkpoint.** Earlier validation remains preserved; this physical continuation records Collective / Membership integration only.

# 2026-08-16 — Collective / Membership downstream resolution

Agreement / Consent v0 previously left collective/group identity SAFE DEFERRED. Collective v0 resolves the generic identity boundary without changing Agreement or Consent semantics.

Current rules:

```text
true Collective may be Agreement party
YES

Agreement party set != Collective identity
Membership != Agreement
member assent != Collective assent automatically
Collective Agreement != every member personally agreed
```

Consent remains independently actor-scoped:

```text
Membership != Consent
Collective Agreement != member Consent
Collective governance != universal Consent on behalf of members
```

The historical deferred item is now narrowed:

```text
collective/group identity for Agreement party
RESOLVED

legal personality/capacity
formal Contract/signature
specialist collective-consent validity
STILL SAFE DEFERRED
```

Regression:

```text
CORE-03 reductio           PASS WITH HARDENING
CORE-04 redundancy         PASS WITH HARDENING
CORE-09 history            PASS WITH HARDENING
MA-05 common ground        PASS WITH HARDENING
MA-06 Authority            PASS WITH HARDENING
MA-13 unequal power        PASS WITH HARDENING
MA-19 redundancy           PASS WITH HARDENING
MA-20 actor stance         PASS WITH HARDENING
XCON-01 identity           PASS WITH HARDENING
XCON-04 relationships      PASS WITH HARDENING
XCON-05 multi-actor        PASS WITH HARDENING
```

Agreement / Consent v0 remains **PASS WITH HARDENING; REOPEN = 0; UNCLASSIFIED = 0**.

Normative references:

- `../concepts/collective.md`;
- `../concepts/membership.md`;
- `../concepts/agreement-part-2.md`;
- `collective-membership-quorum-v0-validation.md`.
