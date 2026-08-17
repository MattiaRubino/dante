# AuthN / AuthZ Requirements

- Status: **CURRENT — Phase 5 accepted requirement package**
- Stage: Pre-Physical Repository & Architecture Coherence
- Physical implementation: **NOT SELECTED / NOT AUTHORIZED**

## Purpose

Define the authentication-context and authorization-enforcement requirements that later Physical/runtime/API/backend work must satisfy without collapsing LifeOS Domain governance into technical identity or permission machinery.

This document constrains implementation. It does not choose an identity provider, authentication protocol, token format, policy engine, session store, authorization language, database policy mechanism or concrete API surface.

## Accepted semantic boundary

The CLOSED Domain and Logical Models already require these distinctions:

```text
Person != Account != Principal != Actor
Authority != AuthZ decision
Consent != Authority
Visibility != Authority
Representation != Authority automatically
actual Actor != represented party automatically
```

Technical authorization may project accepted semantic governance into a request such as:

```text
Principal + Action + Resource + Context
        ↓
technical authorization evaluation
        ↓
allow / deny
```

The reverse mapping is not semantic identity:

```text
allow != Authority

deny != established semantic absence of Authority

authorization tuple / policy record != canonical Domain relation automatically
```

## Normative requirements

### AUTH-01 — Authentication establishes technical security context, not Domain identity by equivalence

Authentication MUST establish or recover a technical security identity/context suitable for enforcement.

It MUST NOT imply that:

```text
authenticated Account = Person
authenticated Principal = Actor
authenticated Principal = Authority
```

Mappings among technical identity and Domain referents MUST remain explicit and justified where needed.

### AUTH-02 — Technical identity concepts remain technical

Account, Principal, Credential, authentication factor, token, session, device credential, service identity and equivalent security artifacts MUST remain technical/runtime concepts unless separately justified by accepted Domain semantics.

Authentication/security session concepts MUST NOT be conflated with the Domain `Session` concept.

### AUTH-03 — Consequential authorization request context is semantically anchored

For a consequential governed operation/effect, the enforcement request MUST be able to identify or reconstruct, where applicable:

- Principal/security context;
- actual Actor;
- represented party;
- semantic target / bounded facet;
- governed operation/effect family;
- purpose/context;
- relevant expected/material target state;
- applicable governance basis.

A route string, UI button or generic permission verb MUST NOT replace the canonical governed-effect semantics required by `WL-H02`.

### AUTH-04 — Governance basis remains reconstructible

Where consequence/audit requires it, LifeOS MUST retain or reconstruct the materially applicable basis for the authorization decision/effect, including as applicable:

- Authority;
- Consent;
- Visibility;
- Agreement or terms state;
- Representation/delegation basis;
- policy/model version or technical decision basis;
- actual Actor and represented party;
- target MaterialStateRef or equivalent accepted semantic state binding;
- resulting effect/correlation.

This is enforcement provenance. It does not turn the AuthZ log into Domain Authority, Consent or Visibility by identity.

### AUTH-05 — Technical allow/deny does not rewrite Domain governance

A technical `ALLOW` MUST NOT manufacture Domain Authority, Consent, Visibility or Representation.

A technical `DENY` MUST NOT be interpreted as universal proof that Authority or Consent semantically does not exist; denial may result from technical policy, stale projection, missing context, safety posture or another enforcement condition.

### AUTH-06 — Actual Actor and represented party remain distinct

Actions performed on behalf of another party MUST preserve, where applicable:

```text
actual Actor
represented party
bounded action/effect
applicable representation/delegation/Authority/Consent basis
```

The system MUST NOT silently attribute the act to the represented party as though that party physically performed it.

### AUTH-07 — Non-human Principals do not bypass governance

Service accounts, background jobs, AI agents, automations, tools, provider callbacks and other non-human technical Principals MUST NOT bypass the same semantic governance boundary merely because the initiator is not an interactive user.

Their technical identity, delegated capability, initiating Actor where relevant, purpose and effect authority MUST remain bounded and auditable according to consequence.

### AUTH-08 — Authorization covers disclosure/non-interference, not only object access

Authorization and disclosure enforcement MUST account for recipient-observable information covered by `WL-H03` and `WL-H12`, including where material:

- object/field data;
- relationship existence/type/state/history;
- source/evidence/provenance existence;
- counts and aggregates;
- search result inclusion;
- ranking/order;
- candidate lists;
- explanations;
- errors/status differences;
- timing-relevant behavior;
- free/busy or other derived surfaces.

Visibility of endpoints does not automatically imply visibility of the relation between them. Visibility of a projection does not automatically imply visibility of its source.

### AUTH-09 — Delayed effects cannot rely indefinitely on stale authorization

A consequential delayed/queued effect MUST either:

1. revalidate applicable governance near effect time; or
2. rely on an explicitly valid immutable authorization/effect binding whose semantics permit delayed execution.

An authorization decision at `T1` MUST NOT become permanent authority at `T2` by technical accident.

### AUTH-10 — Session/device/service context required for security provenance is reconstructible

Where consequence/security investigation requires it, the system MUST be able to reconstruct the relevant authenticated session/device/service context without treating those technical artifacts as Domain owners.

The exact retention depth is consequence/risk sensitive and remains subject to privacy/minimization requirements.

### AUTH-11 — AuthZ projections/caches are downstream technical state

Policy-engine tuples, cached permissions, token claims, derived authorization projections and similar technical artifacts MUST remain downstream enforcement state.

They MUST NOT become canonical governance truth merely because enforcement depends on them.

Material canonical governance changes MUST have a defined way to invalidate, refresh, revalidate or safely reject stale technical authorization state.

### AUTH-12 — Revocation/withdrawal/material governance change affects future applicability truthfully

Withdrawal/revocation/supersession of Authority, Consent, Visibility, Representation or other applicable governance MUST be capable of stopping future effects according to its semantic effective boundary.

Past truthful history MUST NOT be rewritten as though prior authorized/visible states never existed where retention policy permits historical evidence.

### AUTH-13 — Expected-state/freshness applies to governance-dependent consequences

If an authorization/effect depends on a materially versioned governance basis or derived Effective Authority/Visibility, later execution MUST preserve `WL-H05` and `WL-H09`:

- stale material target/governance state cannot be silently accepted;
- consequential derived state is revalidated or materially bound before effect.

### AUTH-14 — Unknown/conflicting governance state remains representable

The technical enforcement layer MUST be able to operate safely when canonical governance state is unknown, unresolved or conflicting without rewriting that condition into a false semantic statement.

Safety-oriented denial is technically valid where policy requires it, but the underlying semantic state remains `unknown/unresolved/conflicting` rather than being rewritten to `no Authority` or `no Consent`.

### AUTH-15 — Least privilege and purpose-bounded technical access

Technical credentials, service capabilities and authorization grants MUST be bounded to the minimum actions/resources/context necessary for their accepted purpose and operational role.

Broad internal technical access MUST NOT be used as a shortcut around semantic target/purpose/visibility checks for consequential or sensitive operations.

## Open parameters / decisions

The following MUST be explicitly resolved before implementation or benchmark decisions that materially depend on them are accepted:

```text
AUTH-OPEN-01 identity provider / account architecture
AUTH-OPEN-02 authentication method set (for example password/passkey/federated factors)
AUTH-OPEN-03 MFA / step-up policy by risk/consequence class
AUTH-OPEN-04 session lifetime / inactivity / reauthentication policy
AUTH-OPEN-05 parallel-session policy
AUTH-OPEN-06 device trust / remembered-device policy
AUTH-OPEN-07 recovery-account and credential-recovery policy
AUTH-OPEN-08 service/non-human Principal issuance and rotation policy
AUTH-OPEN-09 identity-assurance/proofing requirements where any product flow needs them
AUTH-OPEN-10 administrative/support/break-glass access policy
```

`OPEN` means the policy must be decided before dependent implementation, not that the requirement can be ignored.

## Deferred mechanisms — not selected by Phase 5

No selection is made here among, for example:

```text
OAuth / OpenID Connect / other authentication protocols
managed or self-hosted identity provider
password / passkey / federation implementation
JWT / opaque token / cookie/session realization
session persistence technology
OpenFGA / Zanzibar-style engine
Cedar
OPA/Rego
custom policy engine
capability credentials
RLS / database policy enforcement
application-layer enforcement
sidecar enforcement
specific authorization cache design
specific audit-log store
```

A later selection must demonstrate that it preserves this document and the closed Domain/Logical model.

## Downstream acceptance / benchmark pressure

Later Physical/runtime/API design MUST demonstrate at minimum:

1. Principal, Actor and represented party can remain distinct end to end;
2. a consequential effect can reconstruct its materially applicable authorization/governance basis;
3. revocation/change can prevent stale future effect;
4. delayed effects handle governance-time semantics correctly;
5. hidden relationship/source/projection information cannot be inferred trivially through response surfaces;
6. non-human Principals cannot bypass governance;
7. policy/cache failure or staleness cannot silently convert into canonical governance truth;
8. the design does not require a universal permission/relationship ontology to function.

## Traceability

Primary downstream Logical pressure:

```text
WL-H02 governed operation/effect
WL-H03 projection/disclosure surface
WL-H04 absence/unknown != false
WL-H05 expected-state semantics
WL-H09 derived-state freshness
WL-H11 reconstructible consequential AuthZ provenance
WL-H12 non-interference/inference leakage
```

This package does not reopen Domain or Logical semantics and does not authorize AuthN/AuthZ implementation.
