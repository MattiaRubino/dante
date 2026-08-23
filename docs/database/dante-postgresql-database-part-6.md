# DANTE PostgreSQL Database — Architecture, Reference & Whole-Database Blueprint — Part 6

- **Status:** CP6-03 ACTIVE / CANONICAL CONTINUATION / GATE 03 NOT YET EARNED
- **Created:** 2026-08-23
- **Product:** DANTE
- **Database:** PostgreSQL 18 major family
- **Current repository patch:** PostgreSQL 18.6
- **Schema:** `dante`
- **Workstream:** `../workstreams/logical-postgresql.md`
- **Database documentation authority:** `README.md`
- **Part 1:** `dante-postgresql-database.md` — sections 1–30
- **Part 2:** `dante-postgresql-database-part-2.md` — section 31
- **Part 3:** `dante-postgresql-database-part-3.md` — section 32
- **Part 4:** `dante-postgresql-database-part-4.md` — section 33
- **Part 5:** `dante-postgresql-database-part-5.md` — section 34
- **Continuation numbering:** section 35 onward
- **Continuation anchor:** `52b37da42b3c50ddd079eb3bbc8580269f6b74c7`
- **Implementation status:** business schema / business SQLAlchemy mappings / product vertical **NOT YET MATERIALIZED**

---

## Canonical continuity contract

This file is the canonical continuation of Parts 1–5. It does not replace, summarize or supersede any prior part as a whole.

```text
dante-postgresql-database.md
PART 1 / sections 1–30
+

dante-postgresql-database-part-2.md
PART 2 / section 31
+

dante-postgresql-database-part-3.md
PART 3 / section 32
+

dante-postgresql-database-part-4.md
PART 4 / section 33
+

dante-postgresql-database-part-5.md
PART 5 / section 34
+

dante-postgresql-database-part-6.md
PART 6 / section 35 onward
=

ONE CANONICAL HUMAN-READABLE
DANTE DATABASE ARCHITECTURE & REFERENCE
```

Readers, reviewers, migration planning, SQLAlchemy mapping review, Database Dictionary reconciliation, generated-reference checks, direct PostgreSQL proof planning and Gate-03 review MUST consume all active parts.

The preservation, no-summary, explicit-supersession and whole-database cumulative-audit rules already established remain fully applicable.

---

## 35. Consolidation checkpoint H — Account / Principal security-boundary baseline disposition

### 35.1 Scope and authority

This checkpoint closes the two global CP6-03 database-open items that sit at the boundary between DANTE semantic identity and application/platform security identity:

```text
DB-U09  Account
DB-U10  Principal / security context
```

The decision is derived from the complete accumulated authority, including:

```text
Domain authority and 57-concept census
Whole-Logical 57/57 representation model
CP6-01 persistence coverage and exception classification
accepted PostgreSQL Physical mapping
CP6-02 Persistence Constitution / ADR-010
Database Architecture & Reference Parts 1–5
representation / provenance / authority / agreement closure
current backend package/dependency/configuration surface
current FastAPI bootstrap and public route surface
current PostgreSQL role/provisioning model
current backend README implementation boundary
```

This checkpoint is a database-baseline disposition. It does not implement authentication, authorization, identity-provider integration, login, credentials, sessions, tokens, account recovery or product security workflows.

The decisive non-collapse remains:

```text
Person != Account != Principal != Actor
Authority != AuthZ decision
```

Neither Account nor Principal is one of the accepted 15 LR-01 native owners.

### 35.2 Current accepted classification

The accepted persistence coverage classifies Account as an application/security construct outside the 57-concept semantic census.

The accepted persistence coverage classifies Principal/security context as technical security identity/context outside the 57-concept semantic census.

Therefore:

```text
Account
!= new Domain concept
!= sixteenth LR-01 native owner
!= Person subtype
!= Actor role
!= Principal automatically

Principal
!= new Domain concept
!= sixteenth LR-01 native owner
!= Person
!= Account automatically
!= Actor
!= Authority
```

Any later Account or Principal persistence must enter through a concrete security/application contract rather than through semantic-root inflation.

### 35.3 Current code and runtime evidence

The current backend foundation contains the PostgreSQL, SQLAlchemy, Alembic, process/configuration and health/readiness infrastructure required before business schema materialization.

The current backend does not contain a concrete product AuthN/AuthZ implementation contract.

The repository audit found no accepted current implementation equivalent to:

```text
Account ORM model
Principal ORM model
credential model
login session model
OIDC adapter
OAuth adapter
JWT verifier
JWKS resolver
identity-provider subject mapper
account recovery subsystem
account-linking subsystem
product authorization engine
product permission registry
product role registry
```

The current runtime configuration likewise contains no accepted product configuration contract for:

```text
OIDC issuer
OAuth client
JWT audience
JWKS endpoint
security realm
application session lifetime
credential policy
account recovery policy
identity-provider linking
product permission vocabulary
```

The current FastAPI surface remains technical foundation/health-oriented rather than product AuthN/AuthZ materialization.

This absence is not interpreted as evidence that DANTE will never have accounts or principals. It proves only that CP6-03 has no concrete accepted security contract from which to derive their database shape today.

### 35.4 DB-U09 — final Account baseline disposition

The final disposition is:

```text
DB-U09
CLOSED

CP6-04 BASELINE ACCOUNT BUSINESS OBJECTS
0
```

CP6-04 MUST NOT create generic Account persistence merely in anticipation of a future login system.

Objects equivalent to the following are not baseline-authorized:

```text
dante.account
dante.person_account
dante.account_person
dante.account_identity
dante.account_credential
dante.account_session
dante.login_session
dante.account_status_history
dante.account_provider_identity
```

This is a resolved no-baseline disposition, not an unresolved TODO.

### 35.5 Account is not Person

The database must preserve:

```text
Person != Account
```

A Person is semantic DANTE identity within the accepted model.

An Account, if later materialized, is an application/security construct used to access or operate the product under a concrete authentication/access contract.

The existence of one does not manufacture the other.

Allowed future possibilities include, subject to concrete security authority:

```text
Person exists without Account
Account exists before Person reconciliation
one Person linked to one Account
one Person linked to more than one Account
Account linked to no Person
external service/security identity with no Person
```

This checkpoint deliberately does not select one cardinality as universal truth.

### 35.6 No assumed Person↔Account 1:1 relation

CP6 MUST NOT encode:

```text
UNIQUE(account.person_ref)
UNIQUE(person.account_ref)
Person.account_ref NOT NULL
Account.person_ref NOT NULL
```

merely because a first UI might expose one login per human.

The exact future relation depends on real requirements such as:

```text
multiple authentication providers
account migration
account recovery
shared-device behavior
service/system identities
pre-registration states
household/guardian flows
organizational access
external collaborators
identity reconciliation
```

Those concerns are not resolved by the current Domain model and must not be guessed in CP6.

### 35.7 Account is not Actor

Actor remains a contextual agency role, not an Account identity class.

Therefore:

```text
Account != Actor
```

A future operation may be authenticated through one Account while the semantic action is attributed to another eligible Actor or represented party under a concrete representation/authority contract.

The database must never infer:

```text
authenticated account
→ semantic Actor automatically
```

### 35.8 Account is not Principal automatically

A future application may choose an Account as one source of Principal context, but the equivalence is not globally valid.

Potential Principal sources may include:

```text
authenticated Account
external identity-provider subject
service identity
system identity
automation identity
device-bound security identity
session-bound security context
another future bounded security mechanism
```

Therefore CP6 does not encode:

```text
Principal = Account
```

or require a Principal row for every future Account row.

### 35.9 No generic Account lifecycle vocabulary

The absence of a baseline Account table also means there is no baseline authorization for generic account lifecycle fields such as:

```text
status
is_active
is_disabled
is_locked
locked_at
disabled_at
verified_at
last_login_at
failed_login_count
recovery_state
```

These fields have security semantics that depend on the concrete authentication implementation.

A generic lifecycle enum created now would silently decide security behavior before the responsible subsystem exists.

### 35.10 No generic credential persistence

CP6 MUST NOT introduce a credential root or generic credential payload to make Account appear complete.

No baseline objects equivalent to:

```text
dante.credential
dante.password_credential
dante.api_key
dante.refresh_token
dante.recovery_token
dante.mfa_secret
```

are authorized by this checkpoint.

Credential persistence, if any, belongs to the concrete security architecture and must account for hashing/encryption, rotation, revocation, retention, breach response and provider ownership.

None of those details is inferable from the current semantic database model.

### 35.11 No generic login/application session persistence

DANTE Session is an accepted semantic native owner and MUST NOT be reused for authentication sessions.

```text
DANTE Session
!= login session
!= browser session
!= refresh-token session
!= OAuth session
```

Therefore no future security design may collapse application login/session persistence into the semantic `Session` owner merely because both use the English word “session”.

CP6-04 creates no product login-session baseline in this checkpoint.

### 35.12 Account future materialization trigger

Account persistence becomes eligible only when a concrete AuthN/access requirement defines enough bounded semantics to derive a real database contract.

At minimum, the triggering design must determine applicable items such as:

```text
account stable identity
account lifecycle
local vs external authentication ownership
identity provider(s)
issuer / realm boundaries
provider subject identity
credential ownership, if any
Person relationship/cardinality
linking/unlinking
reconciliation
account recovery
disabled/locked/deactivated meaning
multi-provider behavior
security-sensitive history
retention/deletion behavior
administrative authority
privacy/security classification
runtime access paths
migration strategy
proof obligations
```

The resulting future schema may be small or may be provider-specific. This checkpoint does not pre-authorize a universal Account shape.

### 35.13 DB-U10 — final Principal baseline disposition

The final disposition is:

```text
DB-U10
CLOSED

CP6-04 BASELINE PRINCIPAL REGISTRY OBJECTS
0
```

CP6-04 MUST NOT create a universal persistent Principal registry merely because future AuthN/AuthZ or provenance may need security context.

Objects equivalent to the following are not baseline-authorized:

```text
dante.principal
dante.security_principal
dante.principal_identity
dante.principal_person
dante.principal_account
dante.principal_actor
dante.principal_role
dante.principal_permission
```

This is a resolved no-baseline disposition, not an unresolved TODO.

### 35.14 Principal is technical security identity/context

Principal is retained as the technical identity/context relevant to security decisions and provenance where a concrete operation requires it.

Conceptually:

```text
Principal
= authenticated / security-relevant technical identity or context
  under a concrete security mechanism
```

It is not promoted into the Domain object census.

Its exact representation may be transient, externally addressed, account-backed, service-backed or persistently materialized later depending on a real security contract.

### 35.15 Principal is not Person

The database must preserve:

```text
Principal != Person
```

A Principal may authenticate a request involving a Person, but authentication identity and semantic human identity are separate facts.

The database must not infer a Person NativeRef from a token subject, username, email, PostgreSQL role or external identity-provider identifier without an explicit accepted reconciliation contract.

### 35.16 Principal is not Actor

The database must preserve:

```text
Principal != Actor
```

A useful future consequential-action record may distinguish:

```text
Principal P
→ technical authenticated/security context

Actor A
→ semantic agent that performed the action

represented party R
→ party on whose behalf the Actor acted, when applicable

Authority basis M
→ semantic/legal/governance basis that made the effect valid, when applicable
```

These may coincide in a simple case, but coincidence is operation-specific and must never be encoded as a universal identity collapse.

### 35.17 Principal is not represented party

Representation closure already establishes that the actual Actor and represented party are distinct roles where on-behalf-of semantics exist.

A Principal used to authenticate the request does not automatically become either one.

Therefore:

```text
Principal
!= represented party
```

and future provenance must be able to retain the distinction whenever consequential reconstruction requires it.

### 35.18 Principal is not Authority

The database must preserve:

```text
Principal != Authority
```

Authentication answers a technical identity question.

Authority answers a semantic/governance question about why an effect is authorized or legitimate within the accepted DANTE model.

One must never be manufactured from the other.

### 35.19 Technical AuthZ ALLOW is not Domain Authority

A technical authorization engine may eventually answer:

```text
ALLOW
DENY
```

for a request.

That result is not itself DANTE Authority.

```text
technical AuthZ ALLOW
!= canonical Domain Authority
```

An ALLOW decision may be based on product permissions, role assignments, resource policies, account posture or infrastructure policy.

Those mechanisms may permit a request to proceed, but they do not manufacture the semantic Authority basis required by a Domain operation.

### 35.20 Technical AuthZ DENY does not prove Authority absent

Likewise:

```text
technical AuthZ DENY
!= proof that Domain Authority does not exist
```

A request may be technically denied because of:

```text
expired authentication
account disabled
session expired
missing product permission
security lockdown
device posture
rate limiting
operational maintenance
another technical policy
```

while the underlying semantic Authority may still exist.

Technical access control and semantic Authority therefore remain separate decision layers.

### 35.21 PostgreSQL roles are database operational identities only

The current foundation uses:

```text
dante_owner      NOLOGIN
dante_migrator   LOGIN NOINHERIT
dante_runtime    LOGIN NOINHERIT
```

These are PostgreSQL roles used to enforce database ownership, migration and runtime privilege boundaries.

They are not DANTE semantic records.

The database must preserve:

```text
PostgreSQL role
!= Account
!= Principal registry row
!= Person
!= Actor
!= Authority
```

### 35.22 `current_user` is not semantic attribution

A database operation executed as:

```text
current_user = dante_runtime
```

proves only the PostgreSQL role under which SQL executes.

It does not prove:

```text
semantic Actor = dante_runtime
Principal = dante_runtime
Person = dante_runtime
Account = dante_runtime
represented party = dante_runtime
```

Application-level provenance must never substitute database connection identity for semantic attribution.

### 35.23 Migrator and owner roles are not application principals

The same rule applies to:

```text
dante_migrator
dante_owner
```

Their existence is infrastructure/security posture for schema control.

They must not be inserted into future product Principal, Actor or Authority models merely because they are identities known to PostgreSQL.

### 35.24 DB-U21 remains independent

`DB-U21` owns the exact PostgreSQL object ACL matrix for the concrete CP6 schema.

That work concerns privileges such as:

```text
schema USAGE
SELECT
INSERT
UPDATE
DELETE
sequence privileges
function execution
view access
migration ownership
PUBLIC hardening
```

for the concrete PostgreSQL operational roles.

It does not require Account or Principal rows.

Therefore:

```text
DB-U21 PostgreSQL ACL closure
is independent of
DB-U09 / DB-U10 product-security persistence
```

### 35.25 Future provenance pressure does not require a Principal registry now

Consequential provenance may later need to retain exact security context.

That requirement is preserved.

However:

```text
future provenance may need Principal context
!= universal Principal registry required now
```

A future concrete operation may retain Principal context through a bounded security reference such as an Account reference, external identity reference, immutable provider subject tuple, service identity or another accepted representation.

The operation contract must define the exact reference family and retention semantics.

CP6 does not create an empty universal root to avoid making that later decision.

### 35.26 Principal/security context future materialization trigger

Persistent Principal/security-context materialization becomes eligible only when a concrete security or provenance requirement proves independent persistence is necessary.

The triggering design must answer applicable questions such as:

```text
what stable thing is being identified?
what security mechanism created the context?
what issuer/realm/provider scopes the identity?
is the identity external, account-backed, service-backed or local?
what is the stable external key?
what may change over time?
what must remain historically reconstructible?
what lifecycle exists independently of Account?
what references need persistent resolution?
what retention/privacy/security requirements apply?
what exact AuthN/AuthZ subsystem owns reconciliation?
what semantic operations need the context?
what proof requires persistence rather than transient capture?
```

Without those answers, a universal `dante.principal` row would be structurally easy but semantically unjustified.

### 35.27 External identity is not NativeRef

External authentication identifiers may include values such as:

```text
OIDC subject (`sub`)
OAuth/provider user id
issuer + subject pair
email
username
directory object id
provider tenant/realm subject
```

None automatically becomes a DANTE NativeRef.

The database must preserve:

```text
External/provider identity
!= NativeRef(Person)
!= Account automatically
!= Principal registry row automatically
```

A future integration/AuthN contract must retain sufficient issuer/realm/provider context to prevent identity collisions and define reconciliation explicitly.

### 35.28 Email and username are not identity roots

CP6 MUST NOT use email address or username as the hidden universal key for Person, Account or Principal.

Reasons include:

```text
email can change
email can be reassigned
username can be scoped to a provider/realm
multiple providers may use the same string
one person may have multiple addresses
service identities may have no human email
```

A future security subsystem may index or constrain such values within its own bounded contract, but they do not redefine DANTE reference identity.

### 35.29 Token subjects do not directly identify Person

A JWT/OIDC token subject may be stable only within an issuer/tenant/security domain.

Therefore:

```text
token.sub
→ Person.native_ref
```

is forbidden without a concrete mapping/reconciliation layer.

Likewise token claims must not be copied into canonical Person semantics merely because they are authenticated assertions from a provider.

Provider/security source state remains separate from canonical DANTE truth.

### 35.30 No universal security role/permission tables

This checkpoint does not authorize generic product authorization tables such as:

```text
dante.security_role
dante.permission
dante.role_permission
dante.principal_role
dante.account_role
```

The future authorization model may be RBAC, ABAC, relationship-based, capability-based, policy-engine based or a bounded mixture.

CP6 has no authority to choose one merely to make the schema look complete.

PostgreSQL database roles remain separate infrastructure identities and are not evidence that product RBAC is selected.

### 35.31 No universal tenant/realm model

Likewise this checkpoint does not invent:

```text
dante.tenant
dante.realm
dante.organization_account
```

DANTE may later require a product tenancy/security boundary, but current authority does not define one.

Collective is a semantic native owner and MUST NOT be silently reused as a security tenant.

```text
Collective
!= security tenant automatically
```

### 35.32 No security semantics hidden in semantic owner tables

Because Account/Principal are not baseline materialized, CP6 MUST NOT compensate by adding security columns to semantic owners.

No generic additions such as:

```text
person.login_email
person.password_hash
person.is_admin
person.auth_role
person.last_login_at
collective.tenant_id
actor.permission_code
```

are baseline-authorized.

Security persistence must remain an explicit future concern rather than contaminating semantic owner tables.

### 35.33 No security semantics hidden in MaterialState

The generic MaterialState control topology also does not become a security payload store.

CP6 MUST NOT introduce generic facets equivalent to:

```text
account.security
principal.security
person.authentication
person.authorization
```

without concrete owner/facet semantics and a real security contract.

MaterialStateRef remains exact material semantic state, not a universal version token for every technical subsystem.

### 35.34 No security semantics hidden in JSONB

The absence of a baseline Account/Principal schema must not be bypassed through generic JSONB fields such as:

```text
auth_json
principal_json
claims_json
permissions_json
identity_json
```

on unrelated canonical tables.

Required security semantics must be typed and bounded when the responsible subsystem is designed.

### 35.35 No security event ontology introduced here

This checkpoint does not authorize a universal security-event table for:

```text
login
logout
failed_login
token_refresh
permission_check
account_lock
```

Operational/security audit logging may later require its own bounded architecture.

That concern must not be conflated with DANTE semantic Event, Observation, Actual or material-history concepts.

### 35.36 DANTE Event is not security audit event

DANTE Event is an accepted semantic native owner.

It must not be used as a catch-all for infrastructure/security telemetry.

Therefore:

```text
DANTE Event
!= authentication event stream
!= generic security audit event
```

unless a concrete future domain requirement independently establishes that a particular real-world event is semantically represented as Event.

### 35.37 Observation is not security claim storage

Observation remains a semantic observation capability.

It must not become the generic storage location for token claims, identity-provider claims or AuthZ decisions merely because those are “observed” facts.

```text
provider/auth claim
!= Observation automatically
```

The provider/security contract owns its own source semantics.

### 35.38 Agreement / Consent / Authority boundaries remain intact

Checkpoint G closed Agreement baseline materialization without deleting Agreement semantics.

The current checkpoint preserves the separate governance boundaries:

```text
Account
!= Agreement party automatically

Principal
!= Agreement party automatically

AuthZ ALLOW
!= Consent
!= Agreement
!= Authority

login acceptance of terms
!= durable Agreement automatically
```

A product screen labelled “I agree” does not by itself determine which DANTE semantic family is materialized.

### 35.39 Representation/on-behalf-of remains explicit

A future authenticated Principal may act through a semantic Actor on behalf of another party.

Example conceptual reconstruction:

```text
Principal P1
→ authenticated technical context

Actor A1
→ actual semantic agent

represented party R1
→ person/collective on whose behalf A1 acted

Authority basis M1
→ exact semantic basis for the effect
```

The future provenance model must preserve these distinctions when consequential.

No Account/Principal baseline table is required to preserve this architectural rule today.

### 35.40 Absence of Account/Principal rows is not semantic negative evidence

Because CP6 baseline creates no Account or Principal registry:

```text
no Account row
```

must never be interpreted as:

```text
Person cannot access DANTE
Person is unauthenticated forever
Person has no external identity
Person lacks Authority
Person cannot be an Actor
```

Likewise:

```text
no Principal row
```

must never be interpreted as:

```text
no technical principal existed
operation was anonymous
no authenticated security context existed
```

The absence simply reflects that no universal persistent registry is part of the CP6 baseline.

### 35.41 Reference-topology consequence

This checkpoint adds no new reference family.

Specifically:

```text
NativeRef families added       0
ScopedRecordRef families added 0
MaterialState facets added     0
ExternalRef families added     0 by this checkpoint
```

No new entry is added to `native_address`, `scoped_address` or `material_state_address` for Account or Principal.

If a future security design introduces persistent Account or Principal identity, its reference family must be designed from the concrete contract and must not be retrofitted by pretending it was an LR-01 native owner all along.

### 35.42 Current-binding/history consequence

This checkpoint adds no current-binding or semantic material-history topology for Account/Principal.

No baseline objects equivalent to:

```text
account_current_state
principal_current_state
account_current_history
principal_current_history
account.material_state
principal.material_state
```

are authorized.

A future security subsystem may require append-only audit history, status history or state revisions, but those are not automatically DANTE MaterialState history.

### 35.43 Lifecycle consequence

The global non-destructive semantic lifecycle baseline remains unchanged.

However, future Account/credential/security-data retention may have different requirements driven by security/privacy policy.

This checkpoint does not project those unknown requirements onto semantic owner lifecycle.

No universal:

```text
deleted_at
is_deleted
is_active
security_status
```

is added to existing DANTE owners as a substitute.

### 35.44 Provider/integration consequence

External identity-provider state, if later introduced, belongs to bounded provider/integration persistence.

It must preserve:

```text
provider/issuer identity
external subject identity
provider revision/claim basis where consequential
reconciliation to DANTE security/application identity
separation from canonical semantic identity
```

This remains compatible with the broader rule:

```text
provider state != canonical DANTE state
```

`DB-U17` remains independently open and will determine whether any provider/integration baseline objects are justified globally.

### 35.45 Idempotency consequence

Account/Principal closure does not create a reason for a generic idempotency table.

Future security operations such as account creation or provider callbacks may require idempotency, but that belongs to the concrete operation contract.

`DB-U18` therefore remains independently open.

### 35.46 Outbox consequence

Account/Principal closure does not create a real Class-A asynchronous effect requirement.

A future security integration may publish events, but no transactional outbox is justified merely by future possibility.

`DB-U19` remains independently open.

### 35.47 Derived/search/vector consequence

Account/Principal closure creates no derived/search/vector persistence requirement.

No search index, vector table or derived security projection is baseline-authorized.

`DB-U20` remains independently open.

### 35.48 Final naming consequence

Because no Account/Principal objects enter the baseline object inventory, `DB-U08` final naming work has fewer objects to freeze.

Names such as:

```text
account
principal
security_principal
account_identity
```

must not be reserved in the canonical inventory as if materialization were certain.

`DB-U08` remains open until the complete final object inventory is frozen.

### 35.49 Final index consequence

This checkpoint contributes zero Account/Principal indexes to the CP6 baseline.

No speculative indexes for:

```text
email
username
provider subject
principal type
last login
account status
```

are authorized.

`DB-U15` remains open for the exact index review of objects that actually survive the final inventory.

### 35.50 Final ACL consequence

This checkpoint contributes zero Account/Principal table ACL entries because those objects do not exist in the baseline inventory.

`DB-U21` still must finalize exact privileges for every concrete business/control object that does survive.

The final ACL review must preserve:

```text
PostgreSQL operational role
!= product Principal
```

throughout its documentation and tests.

### 35.51 Alembic materialization plan

Checkpoint H authorizes no business-schema migration object for Account or Principal.

Therefore CP6-04 migration planning records:

```text
create dante.account               NO
create dante.principal             NO
create account/person relation     NO
create credential tables           NO
create security session tables     NO
create product role tables         NO
create product permission tables   NO
```

No placeholder migration is created to reserve future names.

Future AuthN/AuthZ schema evolution enters the normal Alembic DAG when a concrete approved contract exists.

### 35.52 SQLAlchemy mapping plan

Checkpoint H authorizes no SQLAlchemy business mapping for Account or Principal.

Therefore CP6-04 mapping planning records:

```text
Account ORM class                 NO
Principal ORM class               NO
Credential ORM class              NO
LoginSession ORM class            NO
SecurityRole ORM class            NO
Permission ORM class              NO
```

No abstract generic security base model is introduced to anticipate them.

### 35.53 Database Dictionary plan

The CP6 baseline Database Dictionary MUST NOT fabricate entries for non-materialized Account/Principal objects.

Instead, the final dictionary/reference system must make their intentional non-materialization discoverable through the human-readable blueprint and unresolved/deferred disposition register.

Object entries added by this checkpoint:

```text
tables      0
views       0
functions   0
triggers    0
indexes     0
sequences   0
```

### 35.54 Direct PostgreSQL proof impact

Because no Account/Principal DDL is authorized, CP6-05 must not pretend to execute table-level positive tests for objects that do not exist.

Applicable direct proof instead includes negative inventory assertions such as:

```text
no unexpected dante.account table
no unexpected dante.principal table
no unexpected Account/Principal material-state facet
no unexpected generic credential/session tables
no runtime ACL grants for nonexistent Account/Principal tables
```

The exact automated inventory mechanism is finalized with the Database Dictionary / final object catalog.

### 35.55 Static/documentation proof impact

The final CP6 documentation QA must prove the non-collapse remains visible across:

```text
Database Architecture & Reference
Database Dictionary/object inventory
migration plan
SQLAlchemy plan
ACL matrix
proof plan
```

No later implementation batch may silently reintroduce Account/Principal as generic roots without a new explicit schema-evolution decision.

### 35.56 Future Account example — external IdP, illustrative only

A future real product may eventually establish a contract such as:

```text
issuer I1
subject S1
→ Account A1
→ optionally reconciled to Person P1
```

This example does not authorize any of those tables or cardinalities now.

Its purpose is to show why issuer/provider scope must be preserved and why `sub = PersonRef` is not safe as a global assumption.

### 35.57 Future service identity example — illustrative only

A future system-to-system operation may authenticate as a service identity:

```text
Principal SP1
→ service credential / workload identity
→ no Person
```

That possibility alone proves why `Principal = Person` is invalid.

It does not authorize a service-principal registry in the CP6 baseline.

### 35.58 Future represented-action example — illustrative only

A future operation may reconstruct:

```text
Account A1 authenticates Principal P1
P1 corresponds to Actor Person X
X acts on behalf of Collective C
Authority basis = exact accepted governance state M1
```

Even if all references happen to resolve to one human in a simpler flow, the database model must preserve the conceptual distinctions needed by the consequential case.

### 35.59 Future technical deny example — illustrative only

A person may retain valid semantic Authority while a request is technically blocked:

```text
Authority basis M1 remains valid
Account temporarily locked
AuthZ/security layer returns DENY
```

This is not contradiction.

It demonstrates:

```text
technical access decision
!= semantic Authority state
```

### 35.60 Future technical allow example — illustrative only

Conversely:

```text
Principal has broad product permission
AuthZ layer returns ALLOW
semantic Authority basis required by operation is absent
```

The product must not manufacture Domain Authority from technical permission.

The application operation must still enforce the relevant semantic/governance contract.

### 35.61 Security logging remains a separate future concern

Operational security logs may later need immutable storage, SIEM export or provider-native retention.

That concern is not solved by:

```text
Observation
Event
Actual
MaterialState history
```

as generic substitutes.

A real security logging requirement must define its own authority, retention, privacy and access model.

### 35.62 Privacy classification remains future concrete work

Accounts, credentials, authentication identifiers and security logs may contain highly sensitive data.

Because the baseline does not materialize them, CP6 does not invent a universal security-data classification framework here.

The first concrete security persistence contract must explicitly address applicable privacy/security handling rather than inheriting ordinary semantic-table access by accident.

### 35.63 Runtime access remains future concrete work

No product AuthN/AuthZ adapter is added merely because the database blueprint mentions Account/Principal boundaries.

The existing runtime remains responsible for its current technical database access only.

Future security implementation must enter through application/platform boundaries with explicit ownership and tests.

### 35.64 No direct AI security identity assumption

The architecture already forbids direct AI canonical acceptance authority.

Likewise CP6 does not assume that an AI/agent automatically maps to Person, Account, Principal or Actor.

A future AI/agent security identity must be defined by the concrete agent/security architecture.

### 35.65 No device-as-Principal assumption

A device identifier may participate in security context, but device identity is not universally a Principal identity.

No device registry or device→Principal relation is introduced by this checkpoint.

A future device-trust capability must define exact identity, lifecycle, ownership, compromise and reconciliation semantics.

### 35.66 No IP-address-as-identity assumption

Network source information such as IP address is contextual telemetry, not stable Account/Principal identity.

It must never become a hidden key for semantic attribution.

### 35.67 No `created_by` universal semantic shortcut

Checkpoint H does not authorize adding generic fields such as:

```text
created_by_account_ref
created_by_principal_ref
created_by_user_id
```

to every canonical table.

Consequential provenance is operation/family-specific and must retain the exact distinctions required by that contract.

A universal creator column would collapse technical request identity, semantic Actor, provenance and current-state authorship into one ambiguous field.

### 35.68 No `updated_by` universal semantic shortcut

The same applies to:

```text
updated_by
modified_by
last_changed_by
```

as universal business semantics.

Technical audit metadata may exist where justified, but it must not substitute for exact semantic provenance or authority basis.

### 35.69 No implicit owner from authentication

Authenticated identity does not establish ownership, possession, stewardship, responsibility or membership.

Therefore no future Account/Principal mapping may infer:

```text
Account/Principal
→ Ownership
→ Possession
→ Stewardship
→ Responsibility
→ Membership
```

without the relevant semantic relation/state.

### 35.70 No implicit visibility from authentication

A Principal being authenticated does not itself decide semantic Visibility.

```text
Authentication
!= Visibility
```

Future access-control implementation may use visibility information, but the semantic concept and technical enforcement remain distinct.

### 35.71 No implicit consent from login

Successful login or account creation does not automatically mean Consent to unrelated domain actions.

```text
login success
!= Consent
```

Any future consent flow must use the accepted Consent semantics and exact material basis where applicable.

### 35.72 No implicit Agreement from terms checkbox

A product onboarding checkbox may be part of a legal/product terms flow, but it does not automatically justify the generic Agreement DDL rejected in Checkpoint G.

A future consequential terms profile must establish its own bounded Agreement/Consent/acknowledgement semantics and exact terms basis.

### 35.73 No implicit responsibility from admin role

A future product admin permission does not automatically create semantic Responsibility.

```text
technical admin role
!= Responsibility
```

This preserves the governance distinction already accepted upstream.

### 35.74 No implicit authority from PostgreSQL ownership

Likewise:

```text
PostgreSQL object owner
!= Domain Authority holder
```

`dante_owner` owning schema objects is a database DDL control mechanism, not a semantic statement about real-world authority.

### 35.75 Security-context persistence may be append-only without being MaterialState

If a future security system needs immutable audit/security-context capture, append-only persistence may be appropriate.

But:

```text
append-only security record
!= MaterialStateRef automatically
```

MaterialState is reserved for exact material semantic state under the accepted DANTE state architecture.

### 35.76 No hidden auth provider selection

No database names or columns in CP6 should hard-code a provider that has not been selected by a future security architecture.

No baseline fields such as:

```text
google_user_id
apple_user_id
auth0_user_id
cognito_sub
firebase_uid
```

are authorized.

Provider-specific persistence belongs to `DB-U17`/future integration work if and when the provider is actually selected.

### 35.77 No hidden local-password assumption

The baseline does not assume DANTE will store local passwords.

Therefore no password hash, salt, algorithm, reset token or password-history schema enters CP6 merely as a conventional Account design.

External-only authentication, passwordless authentication or another future model remain possible until a real security decision is made.

### 35.78 No hidden single-user assumption

The absence of Account persistence also does not authorize treating the whole database as one implicit hard-coded person/account forever.

CP6 keeps semantic identity explicit where the Domain requires it and leaves application access identity for the future security contract.

A later single-user-first product vertical may optimize UX without redefining the canonical database identity model.

### 35.79 No hidden multi-tenant assumption

Conversely, CP6 does not prebuild tenant-scoped Account/Principal columns into every table.

A future multi-user/multi-tenant access architecture must be derived explicitly if required.

### 35.80 No generic security foreign keys on canonical owners

No canonical owner gains a mandatory FK to a nonexistent Account/Principal table.

Therefore the CP6 baseline avoids structural coupling between semantic persistence and an undecided authentication architecture.

### 35.81 Migration-DAG consequence

Checkpoint H introduces no new migration node by itself.

Its effect on the final CP6-04 DAG is negative/clarifying:

```text
Account/Principal security branch
→ absent from baseline DAG
```

The final migration DAG remains built only from objects that survive the complete blueprint.

### 35.82 Object-inventory consequence

The final object inventory MUST record Account/Principal as intentional non-materializations, not as missing objects.

The baseline inventory count therefore excludes:

```text
Account tables
Principal tables
credential tables
login-session tables
product-role tables
product-permission tables
```

This reduces accidental reintroduction during CP6-04.

### 35.83 Dictionary contract consequence

The Database Dictionary format must be able to distinguish:

```text
materialized object
vs
intentionally non-materialized semantic/application concern
```

without creating fake object entries.

The human-readable blueprint remains the authority for the detailed no-baseline rationale.

### 35.84 Generated-reference consequence

Generated schema references will naturally contain no Account/Principal objects in the CP6 baseline.

That absence is correct only if generated-object inventory matches the approved dictionary/object catalog.

A later unexpected Account/Principal table would be a drift defect.

### 35.85 Test taxonomy consequence

Final CP6 tests must distinguish:

```text
positive database invariant tests
negative forbidden-object inventory tests
documentation/dictionary consistency tests
```

Checkpoint H contributes primarily to the second and third categories.

No fake passing test should be recorded for a nonexistent business object.

### 35.86 Security failure does not rewrite semantic history

A future account lock, credential revocation or access denial must not delete or rewrite historical semantic records merely because the user can no longer authenticate.

Security lifecycle and semantic-history retention are separate concerns.

Any future erasure/redaction requirement must enter through the dedicated lifecycle/privacy contract rather than account deletion cascading through DANTE history.

### 35.87 Account deletion must not imply Person deletion

Future Account lifecycle must preserve:

```text
Account deletion/deactivation
!= Person semantic deletion
```

The concrete security design may unlink access while retaining Person/history under applicable policy.

This checkpoint does not choose the eventual account-retention mechanism, but it forbids the identity collapse that would make account lifecycle automatically destructive to Person.

### 35.88 Principal disappearance must not erase provenance

If future Principal/security context is retained in consequential provenance, later account/provider/principal lifecycle must not make required historical provenance undecodable.

The future security/provenance contract must define durable historical reference or captured immutable basis where needed.

This is a future trigger requirement, not authorization for a universal registry now.

### 35.89 Provider reassignment/reuse must be handled explicitly

External identity values can have provider-specific reuse or lifecycle semantics.

A future mapping must rely on the provider's stable scoped identity contract, not on display values.

This reinforces the requirement for issuer/realm/provider context and explicit reconciliation.

### 35.90 Current baseline schema consequence summary

Checkpoint H changes the approved baseline schema by subtraction/closure only:

```text
new tables                     0
new views                      0
new functions                  0
new triggers                   0
new indexes                    0
new sequences                  0
new NativeRef families         0
new ScopedRecordRef families   0
new MaterialState facets       0
new universal roots            0
```

No real DDL is executed in CP6-03.

### 35.91 Whole-database cumulative audit inputs

The cumulative audit for Checkpoint H re-evaluates the accepted database against at least the following global boundaries:

```text
15 native-owner census
NativeRef / ScopedRecordRef / MaterialStateRef / ExternalRef separation
Actor / Subject / Resource contextual-role model
MaterialState acceptance/current discipline
provider != canonical
Authority != AuthZ
Agreement / Consent / Representation closure
lifecycle/non-destructive history posture
PostgreSQL role separation
CP6-02 privilege doctrine
current backend runtime/code/config surface
remaining DB-U register
```

The purpose is to ensure Account/Principal closure does not repair one gap by introducing a different semantic collapse.

### 35.92 Whole-database audit — identity topology

Result:

```text
15 / 15 native owners preserved
Account added as native owner       NO
Principal added as native owner     NO
Person = Account collapse           NO
Person = Principal collapse         NO
Account = Principal collapse        NO
Principal = Actor collapse          NO
```

Status:

```text
PASS
```

### 35.93 Whole-database audit — reference topology

Result:

```text
NativeRef family inflation          NO
ScopedRecordRef family inflation    NO
MaterialState genericization        NO
ExternalRef → NativeRef collapse    NO
provider subject → Person collapse  NO
```

Status:

```text
PASS
```

### 35.94 Whole-database audit — governance/provenance topology

Result:

```text
Principal = Actor                   NO
Principal = represented party       NO
Principal = Authority               NO
AuthZ ALLOW = Authority             NO
AuthZ DENY = no Authority           NO
Account = Agreement party universal NO
```

Status:

```text
PASS
```

### 35.95 Whole-database audit — PostgreSQL security topology

Result:

```text
dante_owner    remains DB role only
dante_migrator remains DB role only
dante_runtime  remains DB role only

DB role = product Principal         NO
DB role = semantic Actor            NO
DB role = Person                    NO
```

Status:

```text
PASS
```

### 35.96 Whole-database audit — lifecycle topology

Result:

```text
Account lifecycle projected onto Person       NO
security deletion cascades invented           NO
universal is_active/status fields invented     NO
credential lifecycle invented                 NO
semantic history tied to login ability         NO
```

Status:

```text
PASS
```

### 35.97 Whole-database audit — implementation topology

Result:

```text
baseline Account migration          NO
baseline Principal migration        NO
baseline security ORM root          NO
baseline generic credential store   NO
baseline generic session store      NO
baseline generic RBAC tables        NO
```

Status:

```text
PASS
```

### 35.98 A/B/C defect classification

The audit classifies candidate defects using the established severity discipline.

A-class architectural regressions rejected by this checkpoint include:

```text
new universal security semantic root
Account promoted to Person
Principal promoted to Actor
PostgreSQL runtime role used as semantic attribution
AuthZ permission treated as Authority
```

B-class premature physical assumptions rejected include:

```text
1:1 Person↔Account cardinality
local-password storage assumption
RBAC assumption
OIDC-provider-specific columns
universal account lifecycle enum
```

C-class documentation/traceability drift rejected includes:

```text
DB-U09/10 left open after final disposition
non-materialized objects still listed for Alembic/ORM
ACL matrix incorrectly waiting for Principal rows
future provenance requirement misread as current registry requirement
```

After repair:

```text
A defects open 0
B defects open 0
C defects open 0
```

### 35.99 DB-U09 closure statement

Final:

```text
DB-U09
ACCOUNT
CLOSED
```

Reason:

```text
Account remains a valid future application/security construct,
but current authority does not provide a concrete AuthN/access contract
that justifies deterministic CP6 baseline persistence.
```

Disposition:

```text
NO BASELINE DDL
FUTURE CONCRETE AUTHN/ACCESS CONTRACT TRIGGER
```

### 35.100 DB-U10 closure statement

Final:

```text
DB-U10
PRINCIPAL / SECURITY CONTEXT
CLOSED
```

Reason:

```text
Principal remains a valid technical security/provenance context,
but current authority does not justify a universal persistent registry.
```

Disposition:

```text
NO BASELINE PRINCIPAL REGISTRY DDL
FUTURE CONCRETE SECURITY/PROVENANCE CONTRACT TRIGGER
```

### 35.101 Register transition

Pre-checkpoint global DB-U open set:

```text
DB-U08
DB-U09
DB-U10
DB-U15
DB-U17
DB-U18
DB-U19
DB-U20
DB-U21

COUNT = 9
```

Checkpoint H closes:

```text
DB-U09
DB-U10
```

Post-checkpoint global DB-U open set:

```text
DB-U08
DB-U15
DB-U17
DB-U18
DB-U19
DB-U20
DB-U21

COUNT = 7
```

### 35.102 Local exact blocker register

The local exact CP6-03 blocker register remains:

```text
OPEN ITEMS = 0
```

Checkpoint H does not reopen:

```text
OUT-U01
MIL-U01
AGR-U01
CRT-U01
EVL-U01
TC-U01
```

All remain closed under their accepted final dispositions.

### 35.103 Unclassified register

No new unresolved or unclassified database item is created by this checkpoint.

```text
UNCLASSIFIED NEW ITEMS
0
```

If a future security requirement appears, it enters through explicit schema evolution rather than being smuggled into the current unresolved register retroactively.

### 35.104 Gate-03 status

Checkpoint H does not earn Gate 03.

Remaining mandatory global consolidation includes:

```text
DB-U08  final naming
DB-U15  final index review
DB-U17  provider/integration disposition
DB-U18  idempotency disposition
DB-U19  transactional outbox disposition
DB-U20  derived/search/vector disposition
DB-U21  exact object ACL matrix

final object inventory
final constraint/reference integrity catalog
final migration DAG
final SQLAlchemy mapping plan
Database Dictionary materialization
final direct PostgreSQL proof plan
whole-database final reconciliation
```

Therefore:

```text
CP6 BUSINESS DDL AUTHORIZED
NO

GATE 03
NOT YET EARNED
```

### 35.105 Checkpoint H final state

```text
CONSOLIDATION CHECKPOINT H
ACCOUNT / PRINCIPAL SECURITY BOUNDARY

PASS AFTER HARDENING

DB-U09
CLOSED

DB-U10
CLOSED

ACCOUNT BASELINE DDL
NONE

PRINCIPAL REGISTRY BASELINE DDL
NONE

LOCAL EXACT OPEN
0

GLOBAL DB-U OPEN
7

GLOBAL DB-U OPEN SET
DB-U08
DB-U15
DB-U17
DB-U18
DB-U19
DB-U20
DB-U21

UNCLASSIFIED NEW ITEMS
0

WHOLE ACCUMULATED DATABASE AUDIT
PASS AFTER HARDENING

CP6 BUSINESS DDL AUTHORIZED
NO

GATE 03
NOT YET EARNED
```

### 35.106 Next global consolidation boundary

The next CP6-03 work begins from the seven-item global set only.

A sensible next grouping must be determined by dependency rather than convenience.

Likely dependency clusters are:

```text
provider / idempotency / outbox / derived
→ DB-U17 / DB-U18 / DB-U19 / DB-U20

final inventory closure
→ DB-U08 / DB-U15 / DB-U21
```

This is planning guidance only. No later DB-U item is closed by implication in Checkpoint H.

Part 6 remains CP6-03 design authority. No real business DDL, Alembic business migration, SQLAlchemy business mapping, product AuthN/AuthZ implementation or first-product-vertical implementation is authorized by this checkpoint.
