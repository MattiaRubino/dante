# System Overview

## Logical architecture

```text
Web client (Next.js) ---------\
                               \
Mobile client (Expo/RN) --------> Versioned HTTPS API (FastAPI)
                                  |-- authentication and authorization
                                  |-- calendar and scheduling
                                  |-- goals and progress
                                  |-- modules and integrations
                                  |-- AI gateway
                                  |-- synchronization and validation
                                             |
                                             v
                                      PostgreSQL
                                             |
                                      Storage provider
```

## Client responsibilities

Clients handle:

- presentation and navigation;
- local interaction state;
- offline-capable caches and queued changes where appropriate;
- secure session storage;
- platform integrations such as notifications, location, HealthKit, or Health Connect.

Clients do not hold database credentials and do not enforce critical authorization or business rules.

## Backend responsibilities

The backend handles:

- authentication and authorization;
- data validation;
- domain rules;
- scheduling and recalibration;
- synchronization and conflict detection;
- audit and version checks;
- integration orchestration;
- AI proposal validation.

## Data responsibility

PostgreSQL is the official server-side state. Device-local storage is a cache and offline operation queue, not an independent source of truth.

## Scalability direction

The initial backend is a modular monolith. Modules should have clear boundaries so that expensive or independently scaled components can be extracted later only when measurements justify it.
