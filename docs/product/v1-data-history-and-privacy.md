# LifeOS V1 — Data History, Privacy, and Legal Boundaries

## Product principle

LifeOS should preserve a rich personal history so the user can review past activity, calculate trends, compare periods, and improve future planning.

Examples include:

- distance run last week;
- average training volume over a year;
- time spent studying by month;
- completion, postponement, and replacement patterns;
- changes in goals, routines, constraints, and preferences;
- source documents and prior plans;
- user-confirmed health, dietary, rehabilitation, or accessibility constraints.

The product goal is to retain as much information as is useful for declared LifeOS functions, not to collect everything merely because storage is available.

## Purpose limitation and minimisation

Every stored data category must have a documented purpose, such as:

- calendar operation;
- personal history;
- analytics and comparisons;
- adaptive planning;
- safety and compatibility checks;
- user-requested reminders or integrations;
- legal, security, or audit requirements.

LifeOS should not collect unrelated data, retain unused raw data indefinitely, or reuse sensitive information for advertising, unrelated profiling, or new purposes without a valid legal basis and clear user information.

## Historical retention

The user may choose long-term or indefinite retention for their own personal history when this is necessary for the requested service and clearly explained.

Retention policy should be configurable by category where practical. The system should support:

- full-detail history;
- reduced or aggregated history after a defined period;
- automatic deletion after a chosen period;
- manual deletion of individual records or categories;
- export before deletion;
- account-wide export and deletion.

Deleting raw records must also remove or irreversibly anonymise derived data that can still be linked to the user, unless another valid retention obligation applies.

## Health and other sensitive data

Health, allergy, dietary, disability, rehabilitation, and similar information is treated as sensitive data with stricter controls.

For a consumer LifeOS service that is not operating under a healthcare professional's responsibility, explicit user consent is expected before processing health data for personalisation and safety checks. Consent must be specific, informed, demonstrable, and withdrawable.

Withdrawal stops future processing based on consent. The product must explain what happens to existing plans and stored data, and provide deletion or another lawful retention path where applicable.

Sensitive data should be separated logically from ordinary planning data and protected with stricter authorisation, logging, encryption, and sharing rules.

## Transparency and user control

The user must be able to understand:

- which data is stored;
- why it is stored;
- where it came from;
- how long it is retained;
- which integrations or service providers receive it;
- which results were user-confirmed, imported, automatically recorded, or inferred;
- how to correct, deactivate, export, or delete it.

Privacy choices must not be hidden inside a single broad acceptance screen. Sensitive features should use contextual, granular choices.

## Security baseline

LifeOS must include security by design, including:

- encryption in transit and at rest;
- strict access control and least privilege;
- separate production and development data;
- secure secret and key management;
- audit logs for sensitive-data access and changes;
- backup protection and tested recovery;
- vulnerability management and dependency updates;
- incident response and personal-data-breach procedures;
- processor agreements and security review for cloud, analytics, notification, and AI providers;
- protection against sensitive data leaking into logs, prompts, notifications, shared events, or debugging tools.

## AI and external providers

Health or other sensitive context must not be sent automatically to an external AI provider merely because it may improve an answer.

Provider use requires:

- a documented purpose and legal basis;
- a data-processing agreement where required;
- clear rules on retention, training use, access, and deletion;
- appropriate safeguards for transfers outside the EEA;
- minimised prompts containing only the context necessary for the current task;
- a safe fallback when sensitive context cannot be sent.

## DPIA and governance

Because LifeOS may combine sensitive data, profiling, systematic personal history, new technology, and AI-assisted recommendations, a Data Protection Impact Assessment should be completed before public processing begins and reviewed when major features or providers change.

The project should maintain:

- a record of processing activities;
- data-flow and processor inventories;
- retention schedules;
- access-control documentation;
- incident and breach procedures;
- a process for data-subject requests;
- periodic privacy and security reviews.

A Data Protection Officer may become mandatory if the organisation's core activities involve large-scale regular monitoring or large-scale processing of special-category data. This must be reviewed before launch and as the user base grows.

## Wellness versus medical purpose

LifeOS V1 is intended as a personal organisation, lifestyle, and wellbeing product. It can preserve user-provided professional plans and prevent obvious conflicts with declared constraints.

It must not claim to diagnose, treat, predict, monitor, or make clinical decisions unless the project intentionally enters the medical-device regulatory framework and completes the required legal, clinical, quality, safety, and conformity work.

The distinction depends on intended purpose, actual functionality, instructions, marketing claims, and how recommendations are presented—not only on a disclaimer.

## Launch requirement

These requirements are a product and architecture baseline, not a substitute for professional legal advice.

Before releasing LifeOS to other users, the final data model, consent flow, privacy notice, terms, retention policy, processor contracts, security controls, DPIA, and medical-device boundary should be reviewed by a qualified privacy professional or lawyer familiar with Italian and EU digital-health products.