<!-- LIFEOS-CANONICAL-CONTINUATION document="domain-model.md" follows="domain-model-part-8.md" -->
> **Canonical continuation of the single logical domain-model workstream record.** Earlier workstream history remains preserved; this physical continuation records Collective / Membership / Quorum v0 only.

# 2026-08-16 — Collective / Membership / Quorum v0 propagation

## Accepted semantic milestone

```text
Collective
SCOPED NATIVE REFERENT
PASS WITH HARDENING

Membership
SPECIFIC CONTEXTUAL RELATION FAMILY / CAPABILITY
PASS WITH HARDENING

Quorum
BOUNDED ELIGIBILITY + CRITERION/EVALUATION + GOVERNANCE/POLICY VOCABULARY
NO NEW PRIMITIVE
```

Validation standard: Domain Validation Methodology v3.

CORE, MA, XCON and ADS gates all passed with incorporated hardenings; REOPEN = 0; UNCLASSIFIED = 0.

## Propagation scope

Authorized pre-scope:

```text
branch
feature/domain-model

pre-scope SHA
767997b7e5e1706460dd3067b5b5b9cb88080832
```

Semantic propagation creates only new canonical files/physical continuation segments. No existing payload is overwritten.

Logical consumers integrated:

```text
Actor
Subject
Participation
Responsibility
Coordination Stewardship
Agreement / Consent
Decision
Criterion / Evaluation
Data / Subjects
Relationship validation
deferred dependency register
Cross-Cluster Validation
Multi-Actor Readiness
Language Map
Domain Atlas README
workstream
```

## Important non-closures

Collective availability does not silently solve all joint semantics.

Still SAFE DEFERRED:

```text
joint Responsibility among several distinct Actors
joint Coordination Stewardship among several distinct Actors
Organization / legal entity
voting / ballot / proxy mechanics
specialist membership/admission flows
```

True Collective bearer semantics are now representable independently from these questions.

## Guardrails preserved

```text
current member set != Collective identity
Membership != Participation / Responsibility / Stewardship
Membership != Authority / Visibility
member stance != Collective Decision
quorum satisfied != Decision / Agreement / Consent / Authority
```

No universal Group, Organization, Party, Member, Quorum, Vote or Ballot root is accepted.

## OOS preserved

Not touched:

```text
SQL
migrations
API
backend
AuthN/AuthZ implementation
frontend
prototype
product docs
main
Contribution
ownership / possession / custody
comprehension
Subject focus/context
Personal Knowledge links
```

## Closure discipline

Propagation is not considered durable CLOSED from write success alone.

Required sequence:

```text
1. create semantic propagation paths
2. compare against exact pre-scope
3. verify 27 added / 0 updated / 0 deleted / 0 unexpected
4. fetch/read remote payloads and continuation chronology
5. verify main unchanged and no OOS
6. only then write pre-authorized validation closure continuation
7. final compare must show 28 added / 0 updated / 0 deleted / 0 unexpected
8. only then declare CLOSED
```

After durable closure, invalidate the prior candidate ranking and perform a fresh read-only candidate-space re-score. Do not automatically promote the previous runner-up.
