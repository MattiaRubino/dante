# ADR-004: File Storage Abstraction

- Status: Accepted
- Date: 2026-08-02

## Decision

Start with local filesystem storage behind a provider interface.

## Rationale

The first implementation must remain free to run locally while preserving a fast transition to cloud object storage.

## Consequences

- Domain data stores logical file identifiers, not absolute machine paths.
- Storage operations pass through a provider contract.
- Cloud migration should require configuration and file transfer rather than domain rewrites.
