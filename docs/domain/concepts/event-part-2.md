<!-- LIFEOS-CANONICAL-CONTINUATION document="event.md" follows="event.md" -->
> **Canonical continuation of the single logical Event document.** Earlier Event semantics remain preserved; this physical continuation records Place integration only.

# 2026-08-16 — Place / venue integration

Event v0 already allowed location semantics. Place v0 now defines the reusable native referent behind venue/location cases where persistent spatial identity matters.

```text
Event != Place
Event venue -> Place where resolved
```

The Event remains occurrence-centred; Place remains spatial identity.

A raw imported location string may exist before a Place is resolved. LifeOS must preserve the source representation/provenance and may later reconcile it to a Place without pretending the Place identity was known at ingestion time.

## Expected versus actual venue

Expected/accepted venue and actual spatial realization remain separate where material.

```text
Event
expected venue -> Place A

Actual occurrence
actual place -> Place B
```

The actual place does not silently rewrite the earlier accepted venue.

Official venue change before occurrence is a change to the Event's accepted spatial context/history, not Event identity replacement by default.

## Virtual events

A meeting link/provider call reference is not Place by default. Virtual participation may have its own integration/product semantics without manufacturing a physical Place.

## Privacy

A visible shared Event venue does not imply Visibility of participants' private Home/work/travel-origin Places or route reasoning.

```text
EVENT v0
verdict unchanged
PASS WITH HARDENING
REOPEN 0
```

Normative reference: `../checkpoints/place-v0-validation.md`.
