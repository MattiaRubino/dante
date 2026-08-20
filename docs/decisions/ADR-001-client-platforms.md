# ADR-001: Client Platforms

- Status: **Superseded by ADR-008**
- Original date: 2026-08-02
- Superseded: 2026-08-20
- Replacement authority: [`ADR-008-frontend-engineering-stack.md`](ADR-008-frontend-engineering-stack.md)

## Historical decision

Use Next.js and React for the web client, and Expo with React Native for Android and iOS.

## Historical rationale

The product requires complete web and mobile experiences with equivalent functionality and device-adapted UX. Shared TypeScript contracts and packages reduce duplication without forcing identical interfaces.

## Historical consequences

- Two client applications are maintained.
- API contracts and shared packages become important.
- Complex web interactions can remain web-native.
- Mobile retains access to native device capabilities.

## Supersession note

The dedicated Frontend Engineering Foundation workstream retained the two-client/platform-adapted principle and Expo/React Native Mobile direction, but replaced Next.js for the application Web client with React DOM + Vite after evaluating the complete DANTE backend, sync/offline, state-ownership and monorepo constraints.

ADR-008 and `docs/architecture/frontend-engineering-foundation.md` are the current decision/specification. This file remains only as historical decision rationale.
