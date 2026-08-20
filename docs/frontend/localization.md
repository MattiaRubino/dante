# DANTE — Frontend Localization Contract

**Status:** v0 — active rule for new/touched pre-frontend UI.

## Goals

- user-facing copy is addressable by stable locale keys;
- Italian and English wording can evolve without renaming technical UI IDs;
- future production frontend/mobile can migrate the same semantic key structure without inheriting prototype HTML coupling.

## Locale files

- `prototypes/frontend/shared/locales/it-IT.json`
- `prototypes/frontend/shared/locales/en-US.json`

Current prototype default language: `it-IT`.

## Key convention

Use semantic keys:

```text
home.contextRail.capture.title
home.contextRail.resolution.title
home.actions.confirm
access.signin.title
access.network.offlineTitle
```

Avoid keys that encode current literal text.

## Operational rule

For every **new or touched** user-facing string:

1. create/reuse a locale key;
2. register it in both current locale files;
3. keep technical identifiers independent of displayed language;
4. record naming status in `terminology.md` when the string is a product noun/label.

The standalone prototypes still contain embedded dictionaries so exact archived artifacts remain self-contained. `prototypes/frontend/shared/locales/` is the durable production-migration registry.

## Access namespace — cross-platform

Desktop A3.4 and Mobile M1.2 share the `access.*` semantic namespace. M1.2 + PRG-0 extends the durable Access dictionary to **128 keys per locale** with exact Italian/English parity.

The shared files contain:

```text
18 existing home.* keys   preserved unchanged
128 access.* keys         current Access production-migration copy
146 total keys / locale
```

Examples:

```text
prototype key              shared key
signin.title               access.signin.title
signup.title               access.signup.title
verify.title               access.verify.title
setupStart.title           access.setupStart.title
network.offlineTitle       access.network.offlineTitle
network.offlineBody        access.network.offlineBody
network.retry              access.network.retry
```

## Password-copy transition

The immutable A3.4 archive still contains its historical `15+` review wording and must remain byte-identical.

Future implementation authority is now the Mobile M1.2 / shared-locale copy:

```text
IT
access.password.guideTitle  = Lunghezza minima
access.password.proposal    = 12+ caratteri

EN
access.password.guideTitle  = Minimum length
access.password.proposal    = 12+ characters
```

This is an intentional product/security policy transition, not accidental translation drift.

## Mobile transport copy

M1.2 adds localized offline transport-state copy under `access.network.*`. Offline is not a canonical account state and must not be translated into an invalid-credential message.

## Rename cost target

A pure wording change should normally be:

```text
locale value change
+ terminology/changelog update if it is a product term
+ rebuild
```

It must not require semantic rewiring.

## Translation policy

English entries are working product translations, not proof of final marketing copy. When a term is `WORKING`, both languages can change while the technical ID remains stable.

Security-relevant copy changes such as password minimum, recovery neutrality or provider scope separation are **not** treated as cosmetic translation changes; they require the relevant contract/changelog/security review.
