# DANTE Documentation Archive

- **Status:** NON-AUTHORITATIVE
- **Purpose:** historical material that remains useful to inspect directly in the working tree

Nothing in this directory is current project authority unless a current document explicitly says otherwise.

Use current product, architecture, database, engineering and project-status documentation for present truth.

The archive is intentionally selective. It is not a backup mirror of the repository and it must not accumulate files merely because they are old.

Git history remains the complete recoverable historical backup.

## What belongs here

Material may be archived only when it is no longer current but still has continuing inspection value, for example:

- meaningful historical operational evidence;
- completed workstream/branch records that are still useful beyond ordinary Git/PR history;
- historical research or validation material whose original context matters.

## What does not belong here

Do not archive:

- active/current specifications;
- live or session handoffs from an active branch;
- backup copies made before editing a file;
- pure duplicates;
- obsolete files whose only remaining value is already fully recoverable through Git.

## Authority rule

```text
CURRENT DOCS / CODE / TESTS / DB SYSTEM OF RECORD
    outrank
ARCHIVED HISTORICAL MATERIAL
```

If an archived file conflicts with current authority, the current authority wins.

See `docs/development/documentation-lifecycle-policy.md` for the normative lifecycle and knowledge-coverage rules.
