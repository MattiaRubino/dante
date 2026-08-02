# Technical Decisions

## Clients

### Web

- Next.js
- React
- TypeScript

### Mobile

- Expo
- React Native
- TypeScript
- Android and iOS from the same mobile codebase where practical

Web and mobile are separate clients of the same product. They share contracts, types, validation, design tokens, and selected business rules while retaining platform-appropriate interfaces.

## Backend

- Python
- FastAPI
- Pydantic
- SQLAlchemy
- Alembic

The backend exposes versioned APIs used by every client. Clients never connect directly to the primary database.

## Data

- PostgreSQL is the primary source of truth.
- Structured data remains relational by default.
- JSONB is reserved for genuinely flexible properties.
- MongoDB is not planned for the primary domain.
- PostgreSQL search is used before introducing a dedicated search engine.

## Files

The first implementation uses local file storage behind a provider interface. Future providers may include S3-compatible storage, Cloudflare R2, Azure Blob Storage, or similar services without changing domain logic.

## AI

AI access is isolated behind an AI gateway.

Initial providers:

1. mock provider;
2. manual ChatGPT import/export workflow;
3. future API provider.

AI produces structured proposals. The backend validates permissions, versions, constraints, and consequences before applying changes.

## Local development

- Web, mobile, and backend may run natively for fast development.
- PostgreSQL runs through Docker initially.
- Docker Compose is prepared for repeatable infrastructure startup.
- Production images will be added when application code begins.

## Deployment direction

The architecture must remain portable across local machines, single-server deployments, managed container platforms, and future orchestration systems. Kubernetes is not required initially.
