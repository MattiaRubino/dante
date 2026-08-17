<!-- LIFEOS-CANONICAL-CONTINUATION document="multi-actor-readiness-v1.md" follows="multi-actor-readiness-v1-part-8.md" -->
> **Canonical continuation of the single logical Multi-Actor Readiness v1 document.** Earlier readiness findings remain preserved; this physical continuation records Collective / Membership / Quorum v0 integration only.

# 2026-08-16 — Collective / Membership / Quorum integration

Collective v0 adds one scoped native referent for materially meaningful plurality while preserving actor-specific state.

## Identity / account independence

```text
Collective != Account
member != Account holder
Membership != account/security membership
```

External/accountless Persons may be members. No synthetic Account is required.

## Shared state versus actor overlays

```text
Collective state
!= each member's personal state

Collective Decision
!= each member's personal stance

Collective Agreement
!= each member's personal Agreement
```

One shared Collective does not erase member-specific responses, beliefs, acknowledgements, consent or participation.

## Responsibility / Stewardship / Participation

```text
Membership != Responsibility
Membership != Coordination Stewardship
Membership != Participation
```

A true Collective may bear Responsibility/Stewardship/Participation where truthful. Several distinct holders do not automatically form a Collective.

## Authority / Visibility

Membership grants neither.

```text
member != Authority holder automatically
member != viewer automatically
```

A bounded membership or eligibility consequence may be shared without exposing private underlying membership reasons/source data.

## Collective decision formation

```text
member responses
+
eligible set
+
threshold Criterion
→ Evaluation / quorum assessment
```

The assessment does not itself become Decision, Agreement, Consent or Authority.

No response is not dissent. Unknown eligibility is not ineligibility. Conflicting eligibility/membership assertions may remain unresolved.

## Representation / on-behalf-of

A representative member acting for a Collective remains distinct from the Collective and from the represented party:

```text
actual Actor
!= Collective automatically
```

Applicable representation/delegation/Authority semantics must establish the bounded attribution where required.

## Lifecycle

Membership join/leave, Collective identity continuity and Account access lifecycle remain independent. Historical actor/member attribution survives current access/membership change where retention permits.

## AI

AI may infer or propose:

```text
possible Collective match
possible Membership
possible eligibility
possible quorum Evaluation
```

but inference does not establish Collective identity, Membership, human assent, Collective action, Authority or Decision by itself.

## Readiness regression

```text
MA-01 Identity/account independence       PASS WITH HARDENING
MA-02 Shared fact / actor overlay         PASS WITH HARDENING
MA-03 Responsibility                     PASS WITH HARDENING
MA-04 Stewardship                        PASS WITH HARDENING
MA-05 Common ground                      PASS WITH HARDENING
MA-06 Authority                          PASS WITH HARDENING
MA-07 Selective disclosure               PASS WITH HARDENING
MA-08 Inference privacy                  PASS WITH HARDENING
MA-09 External/accountless member        PASS
MA-10 Representation/on-behalf-of        PASS WITH HARDENING
MA-11 Lifecycle/revocation               PASS WITH HARDENING
MA-12 Conflict                           PASS WITH HARDENING
MA-13 Unequal power                      PASS WITH HARDENING
MA-14 Resource/capacity                  PASS
MA-15 Coordination burden                PASS WITH HARDENING
MA-16 Progressive formality              PASS
MA-17 AI                                 PASS WITH HARDENING
MA-18 Specialist systems                 PASS WITH HARDENING
MA-19 Primitive redundancy               PASS WITH HARDENING
MA-20 Actor-scoped attribution           PASS WITH HARDENING

MULTI-ACTOR GATE
PASS WITH HARDENING
REOPEN       0
UNCLASSIFIED 0
```

Still deferred: Organization/legal entity, joint Responsibility/Stewardship among distinct Actors, voting/ballot/proxy mechanics and specialist membership/governance systems.

Normative reference: `checkpoints/collective-membership-quorum-v0-validation.md`.
