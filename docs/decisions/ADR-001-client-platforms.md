# ADR-001: Client Platforms

- Status: Accepted
- Date: 2026-08-02

## Decision

Use Next.js and React for the web client, and Expo with React Native for Android and iOS.

## Rationale

The product requires complete web and mobile experiences with equivalent functionality and device-adapted UX. Shared TypeScript contracts and packages reduce duplication without forcing identical interfaces.

## Consequences

- Two client applications are maintained.
- API contracts and shared packages become important.
- Complex web interactions can remain web-native.
- Mobile retains access to native device capabilities.
