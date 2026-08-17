# LifeOS Logical Model External Benchmark & Obsolescence Policy v1

**Status:** Stage-0 foundation  
**Date:** 2026-08-17  
**Purpose:** define how current external systems, standards and specialist products are used as evidence during Logical Model design without becoming ontology authority

---

## 1. Why this policy exists

LifeOS must not design its logical model in isolation, but it also must not copy the data model of the most visible productivity application.

Useful mechanisms may exist in:

- direct competitors;
- calendar/task/project/knowledge products;
- health/finance/inventory specialist systems;
- collaboration or authorization systems;
- infrastructure/databases;
- standards and protocols;
- products unrelated to LifeOS that solved the same structural problem better.

The benchmark therefore asks:

> What mechanism, invariant, failure mode or trade-off can LifeOS learn from this system?

It does **not** ask:

> Which external schema should LifeOS reproduce?

---

## 2. Mandatory benchmark rings

For every material Logical Model slice, review the rings that can realistically challenge it.

### Ring A — Direct / personal orchestration products

Examples:

```text
Motion
Reclaim
Todoist
Things
other current personal planning/orchestration products
```

Use for:

- scheduling behavior;
- task/time distinctions;
- recurrence/routine behavior;
- user-facing lifecycle pressure;
- simple-case ergonomics;
- adaptive planning failure modes.

### Ring B — Adjacent general products

Examples:

```text
Google Calendar
Notion
project-management systems
collaboration systems
document/content systems
home/device systems
```

Use for:

- recurring-instance identity;
- flexible relationships/properties;
- shared-state patterns;
- revision/history patterns;
- external/accountless participation;
- stable identity versus presentation/provider identity.

### Ring C — Specialist domain systems

Examples:

```text
banking/payment systems
inventory/warehouse systems
clinical/health standards
legal/compliance systems
identity/auth systems
```

Use to detect where apparently simple LifeOS concepts become materially richer in a specialist domain.

Specialist richness is evidence for a boundary, not automatic evidence for a general-kernel primitive.

### Ring D — Infrastructure / standards

Examples:

```text
iCalendar / RFC 5545
FHIR / W3C Provenance where relevant
PostgreSQL capabilities
provider API contracts
versioning/audit standards
```

Use for:

- interoperability pressure;
- temporal identity;
- provenance/version requirements;
- feasible representation mechanisms;
- long-lived data semantics.

Infrastructure is evidence about representation capability, not proof of domain meaning.

### Ring E — Negative/counterexample systems

Actively search for systems that expose a behavior LifeOS must **not** inherit.

Examples:

```text
schedule elapsed -> assume work completed
provider ID -> canonical domain identity
generic relation/property -> canonical truth
latest write -> universal conflict winner
one universal status machine
```

A strong anti-pattern can be as valuable as a positive pattern.

---

## 3. Source quality and freshness

Preferred order:

```text
1 official product documentation / API docs / current standards
2 official engineering documentation or specification repositories
3 authoritative primary research where relevant
4 secondary analysis only when primary evidence is unavailable
```

For fast-changing products/providers:

- verify against current official documentation at slice start;
- re-check before final acceptance if the external behavior materially influenced the decision;
- re-check again during final Whole-Logical regression.

For stable standards:

- identify the latest/current published version;
- retain older versions only when interoperability/history requires them.

Do not rely on remembered product behavior when there is a material chance it has changed.

---

## 4. What to extract from every benchmark

For each relevant external mechanism record:

```text
SOURCE
what system/version/document was checked

PROBLEM
what structural problem it addresses

MECHANISM
how the external system appears to solve it

INVARIANT / INSIGHT
what is structurally useful to LifeOS

LIMITATION / ANTI-PATTERN
what should not be copied or where the model breaks down for LifeOS

LIFEOS DISPOSITION
ADOPT PRINCIPLE / ADAPT / REJECT / SPECIALIST-ONLY / NO IMPACT

REOPEN IMPACT
none / logical candidate change / targeted semantic evidence
```

A benchmark is incomplete if it records only "Product X does Y" without stating why that matters or why LifeOS should/should not copy it.

---

## 5. Anti-copy rules

```text
competitor feature != LifeOS semantic primitive
competitor table/property != LifeOS logical owner
provider object != LifeOS canonical identity
popular architecture != correct architecture
flexibility != permission for untyped canonical truth
specialist lifecycle != universal kernel lifecycle
UI status != domain lifecycle
calendar placement != Actual
```

The strongest external design may be borrowed at the behavior or representation-mechanism level while keeping LifeOS semantic ownership different.

---

## 6. Seed benchmark — current evidence captured at Stage 0

This seed exists to calibrate the methodology. It is not a substitute for slice-specific research.

### Google Calendar — recurring instance identity

Current Google Calendar API documentation distinguishes the recurring master from individual instances using `recurringEventId`, while `originalStartTime` identifies the instance within the series even if the instance is moved.

LifeOS lesson:

```text
recurrence policy
!= generated instance identity
!= current scheduled placement
```

Disposition:

```text
ADOPT PRINCIPLE
```

Do not copy Google provider identity as LifeOS canonical identity.

Primary source checked 2026-08-17:
`https://developers.google.com/workspace/calendar/api/guides/recurringevents`

### Todoist — work date vs deadline

Current Todoist documentation separates the date on which the user plans to work on a task from a fixed external deadline.

LifeOS lesson:

```text
planned work placement
!= hard latest-completion constraint
```

Disposition:

```text
ADOPT/CONFIRM PRINCIPLE
```

LifeOS already has richer temporal semantics and should not collapse them into one due-date field.

Primary source checked 2026-08-17:
`https://www.todoist.com/help/articles/introduction-to-deadlines-in-todoist-uMqbSLM6U`

### Todoist — fixed vs floating time

Current Todoist supports both floating local-clock times and fixed timezone-aware times.

LifeOS lesson:

Temporal semantics cannot assume that every `09:00` means the same instant behavior across travel/timezone changes.

Disposition:

```text
ADOPT PRESSURE TEST
```

Primary source checked 2026-08-17:
`https://www.todoist.com/help/articles/set-a-fixed-time-or-floating-time-for-a-task-YUYVp27q`

### Motion — adaptive scheduling

Current Motion documentation schedules tasks from duration, start date, deadline, priority, effort/chunking, schedules and existing events and dynamically reshuffles as conditions change.

LifeOS lesson:

A logical model intended to support orchestration must keep constraints, task/action identity and schedule output distinct enough that schedules can be recomputed without rewriting the underlying intention/execution semantics.

Disposition:

```text
ADOPT BEHAVIORAL PRESSURE
DO NOT COPY ONTOLOGY
```

Primary source checked 2026-08-17:
`https://www.usemotion.com/help/time-management/auto-scheduling/reference-auto-scheduling`

### Reclaim — recurring default vs adaptive rules

Reclaim 2.0 documentation describes Habits as a recurring default event plus automation rules controlling what happens under conflicts, including moving within a window, shortening, skipping or defending time.

LifeOS lesson:

```text
Routine / recurrence intent
!= conflict policy
!= generated/scheduled instance
```

Disposition:

```text
ADOPT PRINCIPLE / BENCHMARK FOR ORCHESTRATION
```

Primary source checked 2026-08-17:
`https://help.reclaim.ai/en/articles/15280604-reclaim-2-0-faq`

### Reclaim — negative Actual inference

Reclaim 1.0 task documentation states that elapsed Task Events are assumed to represent work done for scheduling purposes.

For LifeOS this is a deliberate negative benchmark:

```text
elapsed scheduled block
!= Actual automatically
```

Disposition:

```text
REJECT AS LIFEOS CANONICAL REALITY RULE
```

Primary source checked 2026-08-17:
`https://help.reclaim.ai/en/articles/4303610-key-concepts-in-reclaim-tasks`

### Notion — flexible relations/properties

Current Notion databases support generic property types, relations and rollups across databases.

LifeOS lesson:

Generic configurable mechanisms are valuable for user/product flexibility and derived views.

LifeOS anti-pattern:

A required Domain Atlas semantic owner must not become only a generic relation/property because the mechanism is flexible.

Disposition:

```text
ADAPT FLEXIBILITY
REJECT AS UNIVERSAL CANONICAL SEMANTIC MODEL
```

Primary sources checked 2026-08-17:
`https://www.notion.com/help/database-properties`
`https://www.notion.com/help/relations-and-rollups`

### Plaid — pending and posted financial records

Current Plaid transaction documentation models a pending transaction and its posted counterpart as distinct provider records that may be linked; fields may differ when posting occurs.

LifeOS lesson:

A specialist lifecycle can require identity/linkage semantics richer than a generic status change.

Disposition:

```text
SPECIALIST-BOUNDARY EVIDENCE
```

This does not justify a universal LifeOS Transaction root.

Primary source checked 2026-08-17:
`https://plaid.com/docs/transactions/transactions-data/`

### Odoo Inventory — count vs adjustment/movement

Current Odoo inventory documentation distinguishes recorded stock, physical count and the application of an inventory adjustment; applying the adjustment creates stock-move history for traceability.

LifeOS lesson:

```text
Observation/count
!= specialist stock Movement lifecycle
```

Disposition:

```text
SPECIALIST-BOUNDARY EVIDENCE
```

Primary source checked 2026-08-17:
`https://www.odoo.com/documentation/19.0/applications/inventory_and_mrp/inventory/warehouses_storage/inventory_management/count_products.html`

### HL7 FHIR Provenance — version-specific lineage

FHIR R5 Provenance can target specific resource versions and records the entities/agents/processes involved in creation, revision or deletion.

LifeOS lesson:

Provenance/history requirements may force stable/version-addressable logical references where consequence requires them.

Disposition:

```text
ADOPT PRESSURE / DO NOT COPY FHIR ONTOLOGY
```

Primary source checked 2026-08-17:
`https://hl7.org/fhir/provenance.html`

---

## 7. Benchmark failure conditions

External research fails its purpose if it becomes:

```text
feature checklist only
competitor popularity ranking
schema copying
provider-driven ontology
confirmation bias for a preferred candidate
research performed only after a design is already accepted
```

At least one benchmark pass should be performed **before** candidate selection and one falsification pass should actively seek evidence against the preferred candidate.

---

## 8. Final Whole-Logical benchmark

Before Logical Model closure, rerun a broad benchmark over the integrated representation.

Required question:

> Has any current direct, adjacent, specialist or infrastructure system exposed a structural requirement or failure mode that the integrated LifeOS logical representation cannot naturally support without semantic loss?

Allowed dispositions:

```text
ALREADY COVERED
LOGICAL HARDENING
REJECT EXTERNAL PATTERN
SPECIALIST-ONLY
STAGE-DEFERRED PHYSICAL
TARGETED DOMAIN REOPEN EVIDENCE
```

No external pattern causes a Domain Atlas reopen by naming or popularity alone.
