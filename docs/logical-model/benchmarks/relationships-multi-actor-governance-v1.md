# External Benchmark — Relationships / Multi-Actor / Governance v1

**Status:** Current benchmark evidence for Slice F  
**Date:** 2026-08-17  
**Policy:** External systems are evidence, not LifeOS ontology authority.

## 1. Benchmark objective

This benchmark tests whether LifeOS should preserve or collapse distinctions among:

- semantic relationship families;
- group/collective membership;
- relationship-based authorization;
- policy-based authorization;
- domain Authority;
- technical authorization;
- Consent;
- Visibility;
- Agreement;
- Representation / on-behalf-of;
- actor identity versus security Principal;
- delegation/capability mechanisms;
- historical authorization/governance state.

The benchmark deliberately mixes authorization systems, identity standards, healthcare consent models and capability research. The goal is to extract transferable mechanisms without importing vendor ontologies.

## 2. Google Zanzibar

### SOURCE
Google Research — *Zanzibar: Google’s Consistent, Global Authorization System*.

Primary source:
`https://research.google/pubs/zanzibar-googles-consistent-global-authorization-system/`

### PROBLEM
Evaluate access-control relationships at enormous scale while preserving consistency as ACL/object relationships change.

### MECHANISM
Zanzibar provides a uniform authorization data model and configuration language for access-control policies. The published system stores/evaluates access-control relationships at very large scale and emphasizes causal ordering/external consistency for authorization decisions.

### TRANSFERABLE INSIGHT

```text
relationship-oriented authorization can scale
and can preserve strong consistency properties
```

This is strong evidence that a relation projection can be an excellent runtime authorization substrate.

### LIMITATION / ANTI-PATTERN FOR LIFEOS
Zanzibar’s concern is authorization, not preserving the complete semantic ontology of personal reality. A relation tuple that is sufficient for “may user U access object O?” does not prove sufficiency for Responsibility history, Agreement common ground, Consent purpose/version or actor-scoped interpersonal meaning.

### LIFEOS DISPOSITION

```text
Zanzibar-style ReBAC
RETAIN as serious technical authorization projection/enforcement candidate

Zanzibar tuple model
REJECT as universal LifeOS domain relationship ontology
```

## 3. OpenFGA

### SOURCE
OpenFGA official documentation — Concepts / relationship tuples / authorization model.

Primary sources:
`https://openfga.dev/docs/concepts`
`https://openfga.dev/docs/interacting/managing-user-access`

### PROBLEM
Represent which user/object relationships are possible and evaluate whether an authorization relationship exists.

### MECHANISM
OpenFGA combines an authorization model with relationship tuples using user, relation and object building blocks. Type restrictions constrain which user/object types can be directly related.

### TRANSFERABLE INSIGHT
Typed relation contracts and target eligibility are valuable. A relation string without a model/type restriction would be materially weaker.

### LIMITATION / ANTI-PATTERN FOR LIFEOS
OpenFGA’s relation belongs to an authorization model. Treating every LifeOS semantic relation as an OpenFGA tuple would pressure n-ary/versioned relations into permission-centric forms and tempt the tuple store to become source truth.

### LIFEOS DISPOSITION
Retain typed relation eligibility and possible ReBAC projection. Reject OpenFGA tuples as the canonical owner of Membership, Responsibility, Agreement, Consent, Contribution or Interpersonal Relationship.

## 4. OpenFGA organization-context patterns

### SOURCE
OpenFGA official documentation — organization-context authorization.

Primary source:
`https://openfga.dev/docs/modeling/organization-context-authorization`

### PROBLEM
Derive permissions through organization membership and contextual roles.

### MECHANISM
Authorization models can express relations such as member, project manager, editor and derived can-view/can-edit permissions.

### TRANSFERABLE INSIGHT

```text
membership / organizational relation
+ authorization model
-> effective permission
```

The permission is a derivation, not an unavoidable semantic identity collapse.

### LIFEOS DISPOSITION
Supports the LifeOS rule that Membership may be an input to an Authority/Visibility policy without being equal to Authority/Visibility.

## 5. Cedar

### SOURCE
Cedar Policy Language Reference Guide — authorization request model and context guidance.

Primary sources:
`https://docs.cedarpolicy.com/auth/authorization.html`
`https://docs.cedarpolicy.com/bestpractices/bp-using-the-context.html`

### PROBLEM
Evaluate application authorization policy over a structured request.

### MECHANISM
A Cedar authorization request is built around:

```text
principal
action
resource
context
```

The authorizer evaluates policies/entities and returns `Allow` or `Deny`.

Cedar also explicitly treats request context as distinct from principal/resource information and documents on-behalf-of request-context patterns.

### TRANSFERABLE INSIGHT
A technical authorization decision benefits from a precise request contract and explicit separation of principal/action/resource/context.

### LIMITATION / ANTI-PATTERN FOR LIFEOS
`Allow`/`Deny` is a runtime policy decision. It does not by itself establish a canonical LifeOS fact that the Person held domain Authority, consented, agreed, was responsible or participated.

### LIFEOS DISPOSITION

```text
Cedar/PARC-like request model
RETAIN as serious AuthZ adapter candidate

Cedar policy store
REJECT as LifeOS domain ontology/source truth
```

## 6. Open Policy Agent (OPA)

### SOURCE
Open Policy Agent official documentation.

Primary sources:
`https://www.openpolicyagent.org/docs`
`https://www.openpolicyagent.org/docs/deploy`
`https://www.openpolicyagent.org/docs/integration`

### PROBLEM
Decouple policy decision-making from application policy enforcement across heterogeneous systems.

### MECHANISM
OPA accepts structured input/data, evaluates policy in Rego, and returns a policy decision. Its documentation explicitly separates the policy decision point from policy enforcement points.

### TRANSFERABLE INSIGHT

```text
canonical/business state
-> structured policy input
-> policy decision
-> enforcement
```

is a healthy separation.

### LIMITATION / ANTI-PATTERN FOR LIFEOS
OPA is intentionally domain-agnostic. Making generic JSON/Rego the canonical representation of LifeOS governance would move semantic ownership into policy code and recreate an untyped property/payload escape hatch.

### LIFEOS DISPOSITION
Retain OPA/Rego as a potential runtime policy engine. Keep canonical relation/governance state outside OPA.

## 7. SCIM Group / Membership

### SOURCE
RFC 7643 — SCIM Core Schema.

Primary source:
`https://www.rfc-editor.org/rfc/rfc7643.html`

### PROBLEM
Interoperate user/group identity and membership data across service providers.

### MECHANISM
SCIM defines Group resources and members. Critically, the specification states that although Group resources can support group/role-based access-control models, no explicit authorization model is defined; semantics and authorization granted from membership are service-provider concerns.

### TRANSFERABLE INSIGHT

```text
Group membership
!= authorization semantics automatically
```

### LIFEOS DISPOSITION
This strongly supports:

```text
Membership
!= Authority
!= Visibility
```

and provider group membership remains external/provider evidence until semantics are proven equivalent.

## 8. OAuth 2.0 Token Exchange — `act` / `may_act`

### SOURCE
RFC 8693 — OAuth 2.0 Token Exchange.

Primary source:
`https://www.rfc-editor.org/rfc/rfc8693.html`

### PROBLEM
Represent delegation/impersonation semantics and actor identity in exchanged tokens.

### MECHANISM
RFC 8693 distinguishes:

- `act`: identifies the current actor in a delegated context;
- `may_act`: identifies a party authorized to become the actor and act on behalf of another party.

Nested `act` claims can preserve delegation history.

### TRANSFERABLE INSIGHT

```text
who is acting
!= who is represented / token subject
!= who is authorized to become actor
```

This aligns strongly with LifeOS separation of Actor, represented party, Representation and Authority.

### LIMITATION / ANTI-PATTERN FOR LIFEOS
OAuth token claims are security/token semantics, not canonical domain truth. Token presence/absence cannot replace historical domain attribution or governance state.

### LIFEOS DISPOSITION
Retain the separation principle. Do not map `act` or `may_act` directly to canonical Actor/Authority without explicit adapter/reconciliation semantics.

## 9. HL7 FHIR Consent

### SOURCE
HL7 FHIR R5 Consent resource.

Primary source:
`https://hl7.org/fhir/consent-definitions.html`

### PROBLEM
Represent consent directives with controlled actors/actions/purposes/time/data scope in healthcare contexts.

### MECHANISM
FHIR Consent provisions can carry dimensions including actor, action, purpose, period and controlled data/resource scope.

### TRANSFERABLE INSIGHT
A meaningful Consent cannot be reduced safely to an unbounded boolean or generic permission edge. Scope, action, purpose and temporal applicability can materially change its meaning.

### LIMITATION / ANTI-PATTERN FOR LIFEOS
FHIR is a healthcare interoperability model with specialist/legal/regulatory assumptions. It is not a general LifeOS ontology.

### LIFEOS DISPOSITION
Retain the multidimensional pressure:

```text
Consent giver
+ action/use/exposure
+ target
+ scope
+ purpose
+ context
+ time/material state
```

without importing the FHIR resource model wholesale.

## 10. AWS IAM policy evaluation

### SOURCE
AWS IAM official documentation — policy evaluation logic.

Primary sources:
`https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_evaluation-logic.html`
`https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_evaluation-logic_policy-eval-denyallow.html`

### PROBLEM
Evaluate a request against multiple policy classes, boundaries and explicit denies.

### MECHANISM
AWS evaluates applicable identity/resource policies, permissions boundaries, organization policies and session policies. Explicit deny can override allow, and effective permission may be an intersection/union depending on policy type.

### TRANSFERABLE INSIGHT

```text
runtime allow/deny
= result of technical policy composition
```

not a direct statement of one underlying semantic relation.

### LIFEOS DISPOSITION
Strongly supports:

```text
technical ALLOW != domain Authority
technical DENY != proof domain Authority absent
```

A deny can arise from a security boundary even while legitimate domain Authority exists; an allow can exist due to technical configuration while domain legitimacy is absent.

## 11. Macaroons / contextual caveats

### SOURCE
Google Research / NDSS — *Macaroons: Cookies with Contextual Caveats for Decentralized Authorization in the Cloud*.

Primary source:
`https://research.google/pubs/macaroons-cookies-with-contextual-caveats-for-decentralized-authorization-in-the-cloud/`

### PROBLEM
Support decentralized delegation with attenuated, context-constrained authorization credentials.

### MECHANISM
Macaroons support delegated bearer credentials whose caveats can restrict authorization by context such as when, where, by whom and for what purpose.

### TRANSFERABLE INSIGHT
Capabilities can be powerful for bounded delegation such as:

```text
AI may schedule appointments
for Person P
until time T
under scope S
```

without granting every other Authority.

### LIMITATION / ANTI-PATTERN FOR LIFEOS
A capability credential does not represent all LifeOS relationship semantics. Friendship, Responsibility, Contribution, Agreement and Ownership are not naturally reducible to delegable authorization credentials.

### LIFEOS DISPOSITION
Retain capability mechanisms as a bounded delegation/enforcement ingredient. Reject universal capability ledger as the complete Logical Model.

## 12. OPA decision logs

### SOURCE
OPA official decision-log documentation.

Primary source:
`https://www.openpolicyagent.org/docs/management-decision-logs`

### PROBLEM
Audit technical policy queries/decisions.

### MECHANISM
OPA decision logs can record queried policy, request input and bundle metadata for auditing/debugging.

### TRANSFERABLE INSIGHT
Technical authorization decisions may need their own audit history independently from canonical domain governance history.

### LIMITATION / ANTI-PATTERN FOR LIFEOS
A decision log proves what the policy engine decided, not necessarily the full domain basis, truth, consent validity or semantic Authority history unless those inputs/bindings were themselves preserved.

### LIFEOS DISPOSITION
Retain technical AuthZ audit as a downstream history surface; do not substitute it for LifeOS Provenance/MaterialState governance history.

## 13. Cross-source synthesis

Across the benchmark set, the strongest reusable architecture is layered rather than universal:

```text
DOMAIN / BUSINESS SEMANTICS
specific relationship/governance state
        |
        v
TYPED POLICY / AUTHORIZATION PROJECTION
        |
        v
PRINCIPAL + ACTION + RESOURCE + CONTEXT
        |
        v
RELATION / POLICY / CAPABILITY EVALUATION
        |
        v
ALLOW / DENY / BOUNDED TECHNICAL DECISION
```

Recurring transferable principles:

1. relation-target typing matters;
2. membership alone does not define authorization semantics;
3. actor identity and represented/delegated party can differ;
4. authorization is request/context specific;
5. effective permission may be derived from multiple policy sources;
6. capability/delegation should be attenuated and scoped;
7. consent can require action/purpose/time/data scope;
8. authorization history and domain history are related but not identical;
9. consistency/staleness matters when permission state changes;
10. enforcement engines are replaceable mechanisms.

## 14. Anti-patterns rejected for LifeOS

```text
universal semantic Relationship(from,type,to,payload)
ReBAC tuple store as source of all domain truth
ABAC policy language as canonical ontology
Membership implies Authority
security Group membership equals Collective Membership automatically
technical ALLOW creates domain Authority
technical DENY erases domain Authority
Principal becomes semantic Actor
represented party replaces actual Actor
Consent becomes generic allow flag
Agreement becomes pairwise edges only
capability token becomes universal relationship object
authorization decision log substitutes for material domain history
current policy state explains every historical action automatically
```

## 15. Technology/mechanism reconsideration

```text
Layered typed LifeOS relation/governance model
RETAIN + HARDEN

Zanzibar/OpenFGA ReBAC
RETAIN as serious technical AuthZ candidate

Cedar
RETAIN as serious typed policy/AuthZ candidate

OPA/Rego
RETAIN as policy decision candidate

capability credentials
RETAIN for bounded delegation/attenuation

fully owner-specific physical relation tables
RETAIN as strong Physical Model ingredient

shared technical edge/reference infrastructure
RETAIN only if semantic owner/eligibility remains deterministic

universal relationship graph as canonical ontology
REJECT

universal capability/grant ontology
REJECT
```

## 16. Benchmark verdict

```text
EXTERNAL BENCHMARK
PASS

PREFERRED LIFEOS DIRECTION
Layered Typed Relations & Governance

DOMAIN GOVERNANCE
SEPARATE FROM TECHNICAL AUTHORIZATION

DOMAIN REOPEN IMPACT
0
```

No benchmark provides evidence strong enough to reopen the accepted Domain model or replace the layered A+B+C+D+E architecture.