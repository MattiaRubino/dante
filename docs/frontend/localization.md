# DANTE — Frontend Localization Contract

**Status:** v0 — active rule for new/touched pre-frontend UI.

## Goals

- user-facing copy is addressable by stable locale keys;
- Italian and English wording can evolve without renaming technical UI IDs;
- future production frontend can migrate the same semantic key structure without inheriting prototype HTML coupling.

## Locale files

- `prototypes/frontend/shared/locales/it-IT.json`
- `prototypes/frontend/shared/locales/en-US.json`

Current prototype default language: `it-IT`.

## Key convention

Use semantic keys:

```text
home.contextRail.capture.title
home.contextRail.capture.subtitle
home.contextRail.resolution.title
home.actions.confirm
```

Avoid keys that encode the current literal text:

```text
bad: home.cattura
bad: button.conferma89euro
```

## Operational rule

For every **new or touched** user-facing string:

1. create/reuse a locale key;
2. register it in both current locale files;
3. keep technical identifiers independent of the displayed language;
4. record naming status in `terminology.md` when the string is a product noun/label.

The current monolithic standalone artifact still contains historical inline copy. This is transitional debt, not permission to add more untracked strings. As modules are touched, their user-facing copy must be migrated toward the locale registry.

## Access A3.4 namespace

The selected Access A3.4 review artifact contains complete Italian/English dictionaries internally so the standalone can switch locale without external dependencies. The same reviewed values are mirrored into the shared locale files with an `access.` prefix for future production migration.

Examples:

```text
prototype key              shared key
signin.title               access.signin.title
signup.title               access.signup.title
verify.title               access.verify.title
setupStart.title           access.setupStart.title
```

The embedded prototype dictionary remains a self-contained review mechanism; `prototypes/frontend/shared/locales/` is the durable locale registry. Production React/runtime code should consume the shared namespace rather than depending on the prototype's inline object.

Access A3.4 currently mirrors 125 keys for each locale and keeps Italian/English parity.

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
