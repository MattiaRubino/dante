# B2 Home Edge Attachment v26 archive

This directory preserves the deterministic implementation layer for the user-reviewed **B2 Home Edge Attachment v26** checkpoint.

Base authority:

- B2 Home Shell + Timeline Quick Add v25;
- B2 Home Visual Skin v24;
- B2 Home Branding v23;
- B2 Central Stage v22 no persistent add.

Files:

```text
edge-v25-to-v26.js
```

Transform integrity:

```text
size       2827 bytes
SHA-256    55b1ef7bdf3215a61e9d8aa4215ed6f93f81d98ee458d4ec7a852a37d99d6812
```

The layer performs only the accepted edge-attachment delta:

- expanded AI card reaches the left application edge while preserving its existing right-side geometry;
- collapsed `.home-ai-rail` reaches the left edge, with only the attached left corners squared;
- timeline `lifeos-today` removes only its left outer margin;
- the real Shadow DOM `.today` surface squares only its two left corners;
- the timeline right margin and right-side rounding remain unchanged;
- the application shell is allowed to use the full available width.

Exact runtime targets are the real prototype nodes:

```text
.ai-card.ai-chat-pro
.home-ai-rail
lifeos-today
lifeos-today.shadowRoot .today
```

It does not change v25 app-bar/timeline-quick-add semantics, v24 atmosphere/palette, v23 identity, v22 central-stage behavior, Mondi/Segnali data or behavior, Context Rail semantics, backend contracts or persistence.

User-reviewed local evidence:

```text
DANTE_Home_v38_VERIFIED_OPEN_COLLAPSED_TIMELINE.html
size       83055 bytes
SHA-256    07fab6068427a972f5201454e780d2b7a66db0e10ef9e0f5e80be7be7c5d9f22
```

QA evidence before checkpoint save:

```text
user visual review of v38 preview                PASS
transform JavaScript syntax                      PASS (node --check)
transform mock-structure execution               PASS
component geometry Chromium 1100/1366/1600/1920 PASS
Mondi/stage/orientation geometry mutations       NONE
```

The review wrapper itself is not duplicated here; this archive stores the compact deterministic v25 -> v26 transform that carries the durable checkpoint delta.
