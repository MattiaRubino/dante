# LifeOS

LifeOS is an adaptive personal operating system for planning goals, activities, routines, and day-to-day changes across web, Android, and iOS.

## Project status

The project is currently in the product-definition and architecture-foundation phase. No production application code has been committed yet.

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
