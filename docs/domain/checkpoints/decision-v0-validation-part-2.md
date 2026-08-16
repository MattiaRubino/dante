<!-- LIFEOS-CANONICAL-CONTINUATION document="decision-v0-validation.md" follows="decision-v0-validation.md" -->
> **Canonical continuation of the single logical Decision v0 validation checkpoint.** Earlier validation remains preserved; this physical continuation records Collective / Quorum downstream resolution only.

# 2026-08-16 — Collective Decision / Quorum downstream resolution

Decision v0 previously kept `Collective Decision / quorum / voting` SAFE DEFERRED. Collective / Membership / Quorum v0 resolves the generic core without turning Decision into a voting engine.

Current decomposition:

```text
Collective
= scoped native referent

member response/stance
= actor-scoped state

quorum
= bounded eligibility + threshold Criterion/Evaluation assessment

Decision
= bounded resolution under applicable governance/context
```

Required non-collapse:

```text
member stance != Collective Decision automatically
quorum satisfied != Decision
quorum satisfied != Approval automatically
quorum satisfied != Agreement / Consent / Authority
Collective Decision != every member personally agreed
```

Material eligible-set/policy/Criterion state must remain reconstructible where consequential. Membership or policy changes do not silently rewrite prior quorum assessments or Decisions.

Historical classification update:

```text
Collective Decision core
RESOLVED

Quorum threshold core
RESOLVED WITHOUT NEW PRIMITIVE

Voting / ballot / proxy / delegated-vote mechanics
STILL SAFE DEFERRED
```

Regression:

```text
CORE-04 redundancy         PASS WITH HARDENING
CORE-06 independence       PASS WITH HARDENING
CORE-09 history            PASS WITH HARDENING
CORE-12 complexity         PASS WITH HARDENING
MA-02 shared state         PASS WITH HARDENING
MA-05 common ground        PASS WITH HARDENING
MA-06 Authority            PASS WITH HARDENING
MA-13 unequal power        PASS WITH HARDENING
MA-19 redundancy           PASS WITH HARDENING
MA-20 actor stance         PASS WITH HARDENING
XCON-01 identity           PASS WITH HARDENING
XCON-04 relationships      PASS WITH HARDENING
XCON-05 multi-actor        PASS WITH HARDENING
```

Decision v0 remains **PASS WITH HARDENING; REOPEN = 0; UNCLASSIFIED = 0**.

Normative references:

- `../concepts/collective.md`;
- `../concepts/decision-part-2.md`;
- `../concepts/criterion-evaluation-part-4.md`;
- `collective-membership-quorum-v0-validation.md`.
