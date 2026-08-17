# LifeOS Logical Model — Slice A Identity / Reference Benchmark v1

**Status:** Canonical benchmark evidence — activation conditional on Slice-A remote QA  
**Date:** 2026-08-17  
**Scope:** identity, reference/addressability, provider/security identity, merge/reconciliation, version distinction, privacy/correlation and physical-feasibility pressure

---

## 1. Purpose

This benchmark supports Slice A — Identity / Reference. It does **not** choose a vendor schema or ontology for LifeOS.

The research question is:

> Which identity/reference mechanisms have survived large-scale real systems, which failure modes have forced migrations or reversals, and which structural principles can LifeOS adapt without importing a foreign ontology?

Authority remains:

```text
LifeOS Domain Atlas / North Star
>
ADR-007 + Logical Model methodology
>
accepted Slice-A invariants
>
external evidence
>
vendor implementation shape
```

External evidence is classified as:

```text
STRUCTURAL PRINCIPLE
CURRENT PRODUCT BEHAVIOR
INTEROPERABILITY CONSTRAINT
SPECIALIST BOUNDARY EVIDENCE
NEGATIVE BENCHMARK
```

---

## 2. Research breadth

The benchmark intentionally crosses unrelated product categories so that LifeOS does not overfit personal-productivity patterns.

Reviewed families include:

```text
identity / authentication / provisioning
health interoperability
CRM / enterprise polymorphic relationships
commerce / GraphQL global objects
work-management APIs
cloud resource addressing
container orchestration
source-control/reference systems
knowledge graphs
contact aggregation
home automation / IoT registry
communications APIs
relational database constraints
```

Primary/official sources only are used for material conclusions.

---

## 3. Evidence matrix

### BM-A01 — OpenID Connect

**Source:** OpenID Connect Core 1.0, Subject Identifier Types  
**Official:** https://openid.net/specs/openid-connect-core-1_0.html

**Problem**  
Identify an end-user to relying parties without forcing universal correlation.

**Mechanism**  
`sub` is locally unique and never reassigned within an issuer; pairwise subject identifiers deliberately produce different `sub` values for different sectors/clients.

**Transferable invariant**

```text
same human
!= same provider/security identifier in every context
```

**LifeOS disposition**  
ADAPT: Account/Principal/provider identities are scoped identity spaces and cannot define Person identity.

---

### BM-A02 — SCIM RFC 7643

**Source:** RFC 7643 — SCIM Core Schema  
**Official:** https://www.rfc-editor.org/rfc/rfc7643

**Problem**  
Cross-domain provisioning while keeping provider-owned and provisioning-client-owned identifiers distinct.

**Mechanism**  
SCIM `id` is stable, non-reassignable and service-provider-issued; `externalId` belongs to the provisioning client/domain.

**Transferable invariant**

```text
service-provider identity
!= external/provisioning identity
```

**LifeOS disposition**  
ADAPT: external mappings must carry provider/source scope and must not become canonical LifeOS identity.

---

### BM-A03 — Auth0 account linking

**Source:** Auth0 User Account Linking / Unlink User Accounts  
**Official:** https://auth0.com/docs/manage-users/user-accounts/user-account-linking

**Problem**  
One application user may authenticate through several provider identities.

**Mechanism**  
Identities are separate by default; linking is explicit and security-sensitive; unlinking is supported.

**Transferable invariant**

```text
candidate identity match
!= established equivalence
established link
!= irreversible truth
```

**Limitation**  
Auth0's primary/secondary profile mechanics are product-specific and may discard secondary metadata.

**LifeOS disposition**  
ADAPT the explicit/reversible linking principle; do not copy Auth0 profile-merging semantics.

---

### BM-A04 — Sign in with Apple transfer identifiers

**Source:** Apple — Transferring your apps and users to another team  
**Official:** https://developer.apple.com/documentation/signinwithapple/transferring-your-apps-and-users-to-another-team

**Problem**  
Move users between developer teams without exposing team-scoped identifiers.

**Mechanism**  
Apple issues a target-team-specific transfer identifier that bridges old and new team-scoped user identifiers during migration.

**Transferable invariant**

```text
canonical application identity continuity
may require explicit migration mapping
without exposing/reusing provider-scoped identifiers
```

**LifeOS disposition**  
ADAPT: provider-identity migration is mapping/reconciliation, not native-identity replacement.

---

### BM-A05 — Microsoft Entra ID

**Source:** Microsoft Entra authorization guidance  
**Official:** https://learn.microsoft.com/en-us/entra/architecture/authorize-applications-resources-workloads

**Problem**  
Represent user/security identity across applications.

**Mechanism**  
Microsoft documents pairwise `sub` per application while `oid` is constant across applications in the tenant.

**Transferable invariant**

```text
one provider ecosystem can expose multiple legitimate identity handles
for the same represented user
```

**LifeOS disposition**  
ADAPT: do not infer Person count from raw security-ID count.

---

### BM-A06 — Microsoft Graph Outlook Immutable ID

**Source:** Microsoft Graph — Obtain immutable identifiers for Outlook resources  
**Official:** https://learn.microsoft.com/en-us/graph/outlook-immutable-id

**Problem**  
Ordinary item IDs may change when Outlook items move.

**Mechanism**  
Optional immutable IDs remain stable for the item lifetime within a mailbox, while still having documented scope/lifetime boundaries.

**Transferable invariant**

```text
provider 'stable ID'
can still have a bounded scope/lifetime
```

**LifeOS disposition**  
ADAPT as provider-mapping evidence; never make provider stability claims stronger than the provider contract.

---

### BM-A07 — HL7 FHIR Reference

**Source:** FHIR R5 Reference / references  
**Official:** https://hl7.org/fhir/R5/references.html

**Problem**  
Reference heterogeneous resource types while preserving expected target type and logical/literal identity forms.

**Mechanism**  
FHIR has a generic `Reference` datatype, may carry target `type`, and profiles/elements can restrict allowed target profiles/types.

**Transferable invariant**

```text
shared reference mechanism
+
slot-specific allowed target contract
```

**LifeOS disposition**  
STRONGLY ADAPT the separation between reference transport and semantic target eligibility. Do not import FHIR resource ontology.

---

### BM-A08 — FHIR Person / identity linking pressure

**Source:** FHIR Person and Reference model  
**Official:** https://hl7.org/fhir/person.html

**Problem**  
A human may have several role-specific representations.

**Mechanism**  
FHIR separates Person-style identity linking from operational role-specific resources such as Patient/Practitioner/RelatedPerson.

**Transferable invariant**

```text
human identity
!= every contextual/operational role representation
```

**LifeOS disposition**  
SUPPORTING EVIDENCE ONLY: LifeOS already has Person != Actor/Subject/Resource and does not adopt FHIR's role-resource taxonomy.

---

### BM-A09 — Salesforce polymorphic references

**Source:** Salesforce GraphQL Polymorphic Relationship Filters / Object Metadata  
**Official:** https://developer.salesforce.com/docs/platform/graphql/guide/filter-polymorphic.html

**Problem**  
One relationship field may validly target one of several concrete object types.

**Mechanism**  
Polymorphic fields expose an explicit finite set/union of concrete target types; metadata reports reference targets.

**Transferable invariant**

```text
polymorphic reference
!= unconstrained any-object reference
```

**LifeOS disposition**  
ADAPT: Reference Contracts must declare eligible target families/types rather than permit arbitrary endpoints.

---

### BM-A10 — Shopify Global IDs

**Source:** Shopify — Global IDs in Shopify APIs  
**Official:** https://shopify.dev/docs/api/usage/gids

**Problem**  
Uniformly address objects of many GraphQL types.

**Mechanism**  
Application-wide global IDs encode an object type and identifier; Node enables common lookup.

**Transferable invariant**

```text
uniform addressability can coexist with concrete object type
```

**Limitation**  
Shopify's GID string format and Node ontology are product/API choices, not LifeOS requirements.

**LifeOS disposition**  
ADAPT principle only; reject copying encoded-string format as canonical logical contract.

---

### BM-A11 — Asana GID + resource_type

**Source:** Asana API resource references  
**Official:** https://developers.asana.com/reference/projects

**Problem**  
Compact references to many object types in a work-management API.

**Mechanism**  
Compact objects expose `gid` plus `resource_type`; some relationship slots explicitly permit a union such as team-or-user.

**Transferable invariant**

```text
common globally unique address
+
explicit semantic/resource type
```

**LifeOS disposition**  
ADAPT as supporting evidence for typed technical addressability, not Asana's domain vocabulary.

---

### BM-A12 — Atlassian Resource Identifier (ARI)

**Source:** Atlassian Teamwork Graph — Understanding ARIs  
**Official:** https://developer.atlassian.com/platform/teamwork-graph/understanding-aris/

**Problem**  
Address objects across multiple Atlassian products/sites.

**Mechanism**  
ARI carries app/site/object-type/object-id scope and supports cross-product graph lookup.

**Transferable invariant**

```text
global addressability may need explicit namespace/scope/type
```

**LifeOS disposition**  
ADAPT the scope-awareness principle only; LifeOS internal identity must not be coupled to an encoded ARI-like string.

---

### BM-A13 — AWS ARN

**Source:** AWS IAM — Amazon Resource Names  
**Official:** https://docs.aws.amazon.com/IAM/latest/UserGuide/reference-arns.html

**Problem**  
Unambiguously address heterogeneous cloud resources across services/accounts/regions.

**Mechanism**  
ARN includes partition/service/region/account/resource-specific components.

**Transferable invariant**

```text
reference uniqueness may depend on namespace/scope
not only a local object ID
```

**LifeOS disposition**  
ADAPT for ExternalRef scoping; do not copy ARN syntax or assume all LifeOS native owners need encoded scope.

---

### BM-A14 — Oracle Cloud OCID

**Source:** OCI Resource Identifiers  
**Official:** https://docs.oracle.com/en-us/iaas/Content/General/Concepts/identifiers.htm

**Problem**  
Stable cloud resource identification across resource categories and realms/regions.

**Mechanism**  
OCID includes version, resource type, realm, optional region and unique portion.

**Transferable invariant**  
Type/scope can be part of an address contract while resource semantics remain distinct.

**LifeOS disposition**  
SUPPORTING EVIDENCE; no format copy.

---

### BM-A15 — Kubernetes Name / UID / resourceVersion

**Source:** Kubernetes — Object Names and IDs; ObjectMeta  
**Official:** https://kubernetes.io/docs/concepts/overview/working-with-objects/names/

**Problem**  
Distinguish user-friendly identity/name, historical object occurrence, and mutable version state.

**Mechanism**  
Name is reusable after deletion; UID distinguishes historical occurrences; `resourceVersion` is a separate opaque version/concurrency value.

**Transferable invariant**

```text
human-friendly/reference name
!= persistent occurrence identity
!= material version/state token
```

**LifeOS disposition**  
STRONGLY ADAPT: NativeRef identity and Version/material-state addressing remain separate.

---

### BM-A16 — Git object IDs and refs

**Source:** Pro Git — Git References  
**Official:** https://git-scm.com/book/en/v2/Git-Internals-Git-References

**Problem**  
Address immutable content/history while providing movable human-meaningful pointers.

**Mechanism**  
Object IDs address Git objects; refs are movable names/pointers to those IDs.

**Transferable invariant**

```text
identity/address of a state/version
!= mutable alias/pointer
```

**LifeOS disposition**  
ADAPT only as identity-vs-version/alias pressure; LifeOS native identity is not content-addressed by default.

---

### BM-A17 — GitHub GraphQL global node-ID migration

**Source:** GitHub — Migrating GraphQL global node IDs  
**Official:** https://docs.github.com/en/graphql/guides/migrating-graphql-global-node-ids

**Problem**  
Change global-ID encoding without breaking clients.

**Mechanism**  
GitHub explicitly instructs clients to treat global IDs as opaque and not decode them for type information.

**Transferable invariant**

```text
ID serialization format
!= semantic/type contract
```

**LifeOS disposition**  
STRONGLY ADAPT: identity keys/handles are opaque; owner kind/contract must not depend on parsing ID bytes/prefixes.

---

### BM-A18 — Google People

**Source:** Google People API — Person resource / merged data  
**Official:** https://developers.google.com/people/api/rest/v1/people

**Problem**  
Aggregate person data from contacts/profiles/source records.

**Mechanism**  
Person carries source records, linked people and previous resource names; documentation explicitly says `resourceName` can change when linking changes.

**Transferable invariant**

```text
aggregated representation handle
may change as source-linking changes
source records remain separately identifiable
```

**LifeOS disposition**  
ADAPT source/mapping separation; do not treat Google Person resourceName as canonical LifeOS Person identity.

---

### BM-A19 — Wikidata merge / redirects / unmerge

**Source:** Wikidata Help:Merge / Help:Redirects  
**Official:** https://www.wikidata.org/wiki/Help:Merging

**Problem**  
Merge duplicate identifiers while preserving old external/internal references and recovering from mistakes.

**Mechanism**  
Obsolete IDs redirect to the recipient; merged identifiers are persistent and not reused; documented unmerge workflow exists.

**Transferable invariant**

```text
merge
!= delete historical identity handle
merged identifier must not be reused for another referent
wrong merge must remain correctable
```

**LifeOS disposition**  
STRONGLY ADAPT: identity reconciliation must preserve historical anchors/mappings and allow correction/revocation.

---

### BM-A20 — Home Assistant Core 2026.8

**Source:** Home Assistant Developer Blog — Devices are restricted to a single config entry  
**Official:** https://developers.home-assistant.io/blog/2026/07/21/device-registry-single-config-entry/

**Problem**  
Global device merging across multiple integrations created ownership/source-of-truth complexity.

**Mechanism change**  
Home Assistant now represents a physical device once per config entry rather than globally merging device-registry identities across integrations.

**Transferable anti-pattern**

```text
same-looking external identifiers across providers
!= automatic one canonical object
```

**LifeOS disposition**  
NEGATIVE BENCHMARK: never force provider representations into one native identity solely from identifier similarity/provider heuristics.

---

### BM-A21 — Twilio SID

**Source:** Twilio — String Identifier (SID)  
**Official:** https://www.twilio.com/docs/glossary/what-is-a-sid

**Problem**  
Identify many API resource types with compact unique keys.

**Mechanism**  
Twilio SIDs use type prefixes plus unique payload.

**Transferable observation**  
Typed IDs are operationally convenient.

**Anti-copy lesson**  
LifeOS must not make encoded prefixes the only source of semantic type because GitHub demonstrates such encodings can change.

**LifeOS disposition**  
EVIDENCE ONLY; do not copy SID prefix contract.

---

### BM-A22 — PostgreSQL referential integrity / inheritance caveat

**Source:** PostgreSQL 18 — Table Inheritance / Constraints  
**Official:** https://www.postgresql.org/docs/current/ddl-inherit.html

**Problem**  
Determine whether a universal parent/inheritance table automatically gives global PK/FK integrity across heterogeneous child tables.

**Mechanism / limitation**  
PostgreSQL inheritance does not propagate unique, primary-key or foreign-key constraints across children in the required global way.

**Transferable invariant**

```text
logical typed addressability
must not assume one future SQL inheritance trick solves referential integrity
```

**LifeOS disposition**  
PHYSICAL FEASIBILITY PRESSURE: keep logical contract independent from exact registry/FK/table strategy.

---

## 4. Cross-system synthesis

Across unrelated systems, the strongest reusable pattern is not one schema. It is a separation of concerns:

```text
A. domain/native identity
B. technical addressability/reference
C. contextual relationship/role meaning
D. provider/security identity space
E. reconciliation/equivalence state
F. version/material-state identity
G. public/context-scoped disclosure handle
```

Systems vary heavily in how they encode IDs, but robust systems repeatedly preserve at least several of these distinctions.

### Synthesis S-A01 — typed addressability

```text
shared technical reference
+
explicit target type/eligibility
```

Supported by FHIR, Salesforce, Shopify, Asana, Atlassian and cloud-resource naming patterns.

### Synthesis S-A02 — scoped external identity

```text
provider identity
=
provider/source scope + provider object type + opaque provider ID
```

Supported by OIDC, SCIM, Apple, Entra, AWS and provider APIs.

### Synthesis S-A03 — opaque ID contract

Consumers must not infer durable semantics from ID serialization/prefix format.

Strong negative evidence: GitHub global-ID migration.

### Synthesis S-A04 — reconciliation is a separate lifecycle

```text
possible same referent
!= established same referent
established same referent
!= irreversibly rewritten history
```

Supported by Auth0 linking/unlinking, Wikidata redirects/unmerge, Google People source linking and FHIR identity-linking pressure.

### Synthesis S-A05 — identity vs version

Native referent identity must remain distinct from a particular material state/version.

Supported by Kubernetes UID/resourceVersion and Git object/ref distinctions.

### Synthesis S-A06 — privacy/correlation

A globally stable internal identity is not automatically a safe externally exposed correlation handle.

Supported by OIDC pairwise `sub`, SCIM privacy considerations and Apple transfer identifiers.

---

## 5. Explicit anti-patterns for LifeOS

Reject:

```text
provider ID = LifeOS native identity
email/name/phone equality = automatic Person merge
technical global node = semantic Entity/Thing root
generic endpoint reference = permission for any semantic relation
ID prefix/encoding = sole durable type contract
current provider mapping overwrites mapping history
identity merge deletes/reuses obsolete identity handle
current reference resolution rewrites what LifeOS knew historically
Account/Principal ID = Person ID
NativeRef = Version
internal native ID = universally discloseable API/public handle
all Resource providers must have native identity
SQL inheritance = assumed universal referential-integrity solution
```

---

## 6. LifeOS disposition

The benchmark supports a LifeOS-specific fusion rather than copying any one external model:

```text
Layered Typed Identity & Reference Model

native identity
+
common logical native addressability where justified
+
slot/relation-specific Reference Contracts
+
scoped ExternalRef/provider identity
+
explicit reversible/history-preserving reconciliation
+
separate Version/material-state reference
+
context/visibility-safe exposure
```

This evidence does **not** preselect:

```text
UUID vs integer vs other key
one global registry table
table inheritance
owner-specific FKs
composite typed keys
GraphQL Node
URI/GID/ARI/ARN encoding
API public-ID format
ORM strategy
```

Those remain physical/API-stage choices constrained by the logical contract.

---

## 7. Freshness / recheck triggers

Material current-product evidence must be refreshed when:

- Slice A is reopened logically;
- a later slice changes shared identity/reference/history infrastructure;
- Physical Model feasibility contradicts an assumption;
- a provider/standard materially changes identity semantics;
- Whole-Logical final regression runs.

Stable standards/patterns remain useful as historical evidence but do not eliminate re-validation where implementation behavior matters.
