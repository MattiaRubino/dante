# B05-B — actor-local primary Life Area assignment closure

- **Status:** CLOSED / PROVEN
- **Date:** 2026-09-20
- **Proved branch head:** `1ba879cc3874e14c355b627d5badfb7ece2f09c8`
- **Alembic:** `20260920_46`
- **Expected topology asserted by direct PostgreSQL test:** `123|5|54|90|245|170|354|0|0|0`
- **CI / Actions:** not run

The user fast-forwarded to the proved branch and ran the eight selected PostgreSQL
test modules from the B05 handoff. Result: **16 passed in 26.47s**. The first
attempt stopped during pytest collection because legacy regression tests used a
top-level helper import incompatible with the project's importlib mode. The
test-only repair was published at the proved head; all 16 tests then passed.

The selected proof includes the current whole-database/Dictionary/SQLAlchemy/
Alembic catalog, `_46` actor-local assignment/receipt and runtime ACL tests,
Life Area catalog, B04-D/E catalog regressions, Activity/Event creation and
B04-F constrained authoring. No prototype-only evidence was counted.

Two typed relations give each self-organizing Person at most one current primary
area for an Activity or Event, without becoming a Domain owner or duplicating
canonical items. All new backend creates bind an area atomically. Legacy items
remain explicitly unassigned and discoverable for reconciliation; there is no
invented default or database totality claim. Archived targets reject new
assignments; existing assignments/history remain discoverable. B04 scheduling
truth is independent of area visibility. Frontend migration remains B05-D.

Next gate: B05-C secondary actor-local multi-valued Tags, distinct from the
primary area, Goal, Plan, Context, Place and provider calendars.
