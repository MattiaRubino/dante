<!-- LIFEOS-CANONICAL-CONTINUATION document="subject.md" follows="subject-part-2.md" -->
> **Canonical continuation of the single logical Subject document.** Earlier Subject semantics remain preserved; this physical continuation records Place integration only.

# 2026-08-16 — Place integration

Place v0 supplies one native referent that may play Subject role where a descriptive record is primarily about a place.

```text
Place P
    ↑ Subject role
Observation
room temperature = 21.6 °C
```

Canonical boundary:

```text
Place != Subject
Place may play Subject role
Subject role does not manufacture Place identity
```

A record may also use a Place as context/focus without making the Place its primary Subject. Do not overload Subject as generic `located_at` or `related_to`.

Examples:

```text
Observation about Person Anna
context = Place Office

Observation about Place Office
subject = Place Office
```

These answer different questions.

Address/provider/coordinate data does not become Subject identity when the actual aboutness is the persistent Place referent.

Subject v0 remains **PASS WITH HARDENING, REOPEN = 0**.

Normative reference: `../checkpoints/place-v0-validation.md`.
