# ADR-005: Replaceable AI Gateway

- Status: Accepted
- Date: 2026-08-02

## Decision

Isolate AI interactions behind a replaceable gateway and begin with mock/manual providers.

## Rationale

The application must support AI-assisted creation and recalibration without making the core product dependent on an API subscription during early development.

## Consequences

- AI output must follow structured schemas.
- AI never writes directly to the database.
- Backend validation and user confirmation remain authoritative.
- A future OpenAI API provider can be added without changing client workflows.
