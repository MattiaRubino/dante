"""Patch first-Event hard deletion without reverting later lifecycle migrations.

Revision ID: 20261107_176
Revises: 20261107_175

The existing SQL routines are amended in place with deterministic guards.
Reality-Policy fingerprinting from revision 158 is retained unchanged.
"""

from collections.abc import Sequence

from alembic import op

revision: str = "20261107_176"
down_revision: str | None = "20261107_175"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def _patch_function(signature: str, patches: tuple[tuple[str, str], ...]) -> None:
    db = op.get_bind()
    definition = db.exec_driver_sql(
        "SELECT pg_get_functiondef(%s::regprocedure)",
        (f"dante.{signature}",),
    ).scalar_one()
    if "SECURITY DEFINER" not in definition:
        raise RuntimeError(f"Untrusted temporal lifecycle definition: {signature}")
    for before, after in patches:
        if definition.count(before) != 1:
            raise RuntimeError(f"Unexpected temporal lifecycle definition: {signature}")
        definition = definition.replace(before, after)
    db.exec_driver_sql(definition.replace("%", "%%"))
    db.exec_driver_sql(f"ALTER FUNCTION dante.{signature} OWNER TO dante_owner")
    db.exec_driver_sql(
        f"REVOKE ALL ON FUNCTION dante.{signature} FROM PUBLIC,dante_runtime,dante_migrator"
    )
    db.exec_driver_sql(f"GRANT EXECUTE ON FUNCTION dante.{signature} TO dante_runtime")


def upgrade() -> None:
    baseline = op.get_bind().exec_driver_sql(
        "SELECT pg_get_functiondef(%s::regprocedure)",
        ("dante.get_self_temporal_hard_delete_fingerprint(uuid,uuid,text)",),
    ).scalar_one()
    if "policy_state text" not in baseline or (
        "reality_review_policy_current_history" not in baseline
    ):
        raise RuntimeError(
            "Missing authoritative Reality-Policy protection from migration 158"
        )
    _patch_function(
        "get_self_temporal_hard_delete_fingerprint(uuid,uuid,text)",
        _PREVIEW_PATCHES,
    )
    _patch_function(
        "delete_self_temporal_hard(uuid,uuid,text,text)", _DELETE_PATCHES
    )
    _patch_function(
        "list_self_event_deletion_occurrences(uuid,uuid)", _CHOICE_PATCHES
    )


def downgrade() -> None:
    raise RuntimeError("20261107_176 is forward-only")


_PREVIEW_PATCHES: tuple[tuple[str, str], ...] = (
    (
        "BEGIN",
        "        first_event uuid; first_source uuid; first_occurrence uuid;\n        first_event_fingerprint text;\nBEGIN",
    ),
    (
        "    SELECT owned.event_ref INTO source FROM dante.event_expectation AS owned",
        "    -- A physical first Event belongs to the recurring source, not to\n    -- another standalone series rooted at its own native identity.\n    SELECT seed.source_event_ref INTO source\n      FROM dante.event_recurring_seed AS seed\n     WHERE seed.event_ref=requested_ref\n       AND seed.self_person_ref=requested_actor;\n    IF source IS NULL THEN\n      SELECT owned.event_ref INTO source FROM dante.event_expectation AS owned",
    ),
    (
        "    IF source IS NULL THEN\n      SELECT generation.source_native_ref INTO source",
        "    END IF;\n    IF source IS NULL THEN\n      SELECT generation.source_native_ref INTO source",
    ),
    (
        "  IF requested_scope LIKE 'activity_%' THEN",
        "  IF requested_scope='event_series'\n     AND NOT EXISTS (\n         SELECT 1 FROM dante.get_self_event_recurrence(requested_actor,source)\n     ) THEN\n    RAISE EXCEPTION USING ERRCODE='23503',\n        CONSTRAINT='temporal_hard_unavailable',\n        MESSAGE='Event is not a recurring source';\n  END IF;\n  IF requested_scope LIKE 'activity_%' THEN",
    ),
    (
        "  body:=requested_scope||':'||requested_ref::text||':'||source::text||':'||",
        "  IF requested_scope='event_once' THEN\n    SELECT seed.source_event_ref, seed.first_occurrence_ref\n      INTO first_source, first_occurrence\n      FROM dante.event_recurring_seed AS seed\n     WHERE seed.event_ref=source AND seed.self_person_ref=requested_actor;\n  ELSIF requested_scope IN ('event_instance','event_series') THEN\n    SELECT seed.event_ref INTO first_event\n      FROM dante.event_recurring_seed AS seed\n     WHERE seed.source_event_ref=source AND seed.self_person_ref=requested_actor\n       AND (requested_scope='event_series'\n            OR seed.first_occurrence_ref=instance);\n  END IF;\n  IF first_event IS NOT NULL THEN\n    first_event_fingerprint:=dante.get_self_temporal_hard_delete_fingerprint(\n        requested_actor,first_event,'event_once'\n    );\n  END IF;\n  body:=requested_scope||':'||requested_ref::text||':'||source::text||':'||",
    ),
    (
        "        COALESCE(activity_state,'')||':'||COALESCE(occurrence_state,'')||':'||",
        "        COALESCE(first_source::text,'')||':'||\n        COALESCE(first_occurrence::text,'')||':'||\n        COALESCE(first_event_fingerprint,'')||':'||\n        COALESCE(activity_state,'')||':'||COALESCE(occurrence_state,'')||':'||",
    ),
)

_DELETE_PATCHES: tuple[tuple[str, str], ...] = (
    (
        "        has_target boolean;",
        "        has_target boolean; first_event uuid; first_source uuid; first_occurrence uuid;",
    ),
    (
        "    SELECT owned.event_ref INTO source",
        "    IF requested_scope='event_series' THEN\n      SELECT seed.source_event_ref INTO source\n        FROM dante.event_recurring_seed AS seed\n       WHERE seed.event_ref=requested_ref\n         AND seed.self_person_ref=requested_actor;\n    END IF;\n    IF source IS NULL THEN\n      SELECT owned.event_ref INTO source",
    ),
    (
        "    IF source IS NULL AND requested_scope='event_series' THEN",
        "    END IF;\n    IF source IS NULL AND requested_scope='event_series' THEN",
    ),
    (
        "  -- All producer materialization of this source holds the same advisory lock",
        "  IF requested_scope='event_once' THEN\n    SELECT seed.source_event_ref,seed.first_occurrence_ref\n      INTO first_source,first_occurrence\n      FROM dante.event_recurring_seed AS seed\n     WHERE seed.event_ref=source AND seed.self_person_ref=requested_actor;\n    IF first_source IS NOT NULL THEN\n      -- Lock the recurring source before deleting its first physical Event.\n      PERFORM pg_advisory_xact_lock(hashtextextended(\n        'dante:recurrence-materialization:'||first_source::text,0\n      ));\n    END IF;\n  END IF;\n  -- All producer materialization of this source holds the same advisory lock",
    ),
    (
        "  current_fingerprint:=dante.get_self_temporal_hard_delete_fingerprint(",
        "  IF requested_scope IN ('event_instance','event_series') THEN\n    SELECT seed.event_ref INTO first_event\n      FROM dante.event_recurring_seed AS seed\n     WHERE seed.source_event_ref=source\n       AND seed.self_person_ref=requested_actor\n       AND (requested_scope='event_series'\n            OR seed.first_occurrence_ref=occurrence);\n  END IF;\n  current_fingerprint:=dante.get_self_temporal_hard_delete_fingerprint(",
    ),
    (
        "  IF requested_scope IN ('activity_instance','event_instance') THEN\n    -- A technical skip receipt remains to prevent occurrence resurrection.",
        "  IF requested_scope='event_once' AND first_occurrence IS NOT NULL THEN\n    -- A physical first Event must not regenerate after deletion. Preserve an\n    -- existing skip receipt, but delete the original native graph.\n    IF NOT EXISTS (\n        SELECT 1 FROM dante.occurrence_skip AS skipped\n         WHERE skipped.occurrence_ref=first_occurrence\n    ) THEN\n      exclusion_operation:='temporal:hard-delete:'||first_occurrence::text;\n      PERFORM 1 FROM dante.skip_self_occurrence(\n        requested_actor,exclusion_operation,\n        encode(pg_catalog.sha256(pg_catalog.convert_to(exclusion_operation,'UTF8')),'hex'),\n        first_occurrence,'Eliminazione definitiva istanza'\n      );\n      affected:=affected+1;\n    END IF;\n  ELSIF requested_scope IN ('activity_instance','event_instance') THEN\n    -- Preserve existing Activity/Event instance skip and replay semantics.",
    ),
    (
        "    affected:=affected+1; -- The durable exclusion is one accepted mutation.",
        "    affected:=affected+1;",
    ),
    (
        "    affected:=affected+dante.delete_self_temporal_root_graph(\n       requested_actor,source,'event'",
        "    IF requested_scope='event_series' AND first_event IS NOT NULL THEN\n      -- Traverse the physical original as a separate native root. Outbound\n      -- FK references from its seed are not followed by the graph deleter.\n      affected:=affected+dante.delete_self_temporal_root_graph(\n          requested_actor,first_event,'event'\n      );\n    END IF;\n    affected:=affected+dante.delete_self_temporal_root_graph(\n       requested_actor,source,'event'",
    ),
    (
        "    affected:=affected+dante.delete_self_temporal_root_graph(\n       requested_actor,occurrence,'event_occurrence_content'",
        "    IF first_event IS NOT NULL THEN\n      affected:=affected+dante.delete_self_temporal_root_graph(\n          requested_actor,first_event,'event'\n      );\n    END IF;\n    affected:=affected+dante.delete_self_temporal_root_graph(\n       requested_actor,occurrence,'event_occurrence_content'",
    ),
)

_CHOICE_PATCHES: tuple[tuple[str, str], ...] = (
    (
        "      LEFT JOIN dante.schedule AS schedule",
        "      LEFT JOIN dante.event_recurring_seed AS seed\n        ON seed.source_event_ref=owned.event_ref\n       AND seed.first_occurrence_ref=generation.occurrence_ref\n       AND seed.self_person_ref=requested_actor\n      LEFT JOIN dante.schedule AS direct_schedule\n        ON direct_schedule.subject_native_ref=generation.occurrence_ref\n      LEFT JOIN dante.schedule AS original_schedule\n        ON original_schedule.subject_native_ref=seed.event_ref\n      LEFT JOIN dante.schedule AS schedule",
    ),
    (
        "        ON schedule.subject_native_ref=generation.occurrence_ref",
        "        ON schedule.schedule_ref=COALESCE(\n            direct_schedule.schedule_ref,original_schedule.schedule_ref\n        )",
    ),
)
