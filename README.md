# LifeOS

LifeOS is an adaptive personal operating system for planning goals, activities, routines, and day-to-day changes across web, Android, and iOS.

## Project status

Phase 3 product definition is closed. Phase 4 is in progress with a coded UX prototype focused on the Home/Today surface, timeline density, progressive disclosure, overlapping items, and grouped expansion.

No production application code has been committed yet. The current milestone is an interactive validation prototype with simulated data.

## Current Phase 4 milestone

- Phase 4 frontend source of truth: [`docs/phase-4/frontend-master.md`](docs/phase-4/frontend-master.md)
- Home/Today v7 decisions: [`docs/ux/today-home-v7.md`](docs/ux/today-home-v7.md)
- Prototype archive and restore instructions: [`prototypes/today/archive/README.md`](prototypes/today/archive/README.md)
- Prototype index: [`prototypes/README.md`](prototypes/README.md)

The frontend master log must be read before each Phase 4 iteration and updated after every meaningful change. It records the current implementation, rationale, regressions, open issues, handoff rules, versioning, and Git workflow.

## Product direction

LifeOS will provide:

- a central adaptive calendar;
- goals, projects, activities, routines, and progress tracking;
- optional modules such as nutrition, training, health, learning, travel, and creative work;
- web, Android, and iOS clients with equivalent functionality and platform-adapted UX;
- AI-assisted planning behind a replaceable provider interface;
- local development with a future path to portable cloud deployment.

## Initial technical direction

- Web: Next.js + TypeScript
- Mobile: Expo + React Native + TypeScript
- Backend: Python + FastAPI
- Primary database: PostgreSQL
- File storage: local provider initially, replaceable by S3-compatible/cloud providers
- AI: mock/manual provider first, API provider later
- Repository: private monorepo
- Local infrastructure: Docker Compose for infrastructure dependencies

See [`docs/`](docs/) for the current product and architecture decisions.
