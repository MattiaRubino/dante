"""B14-U2 optional Life Area and canonical quick-authoring metadata.

Revision ID: 20260930_94
Revises: 20260929_93

This migration deliberately supersedes the B05 product rule that every newly
created Activity/Event must receive a primary Life Area.  Absence of an
assignment row is now a valid actor-local organizational state, not only a
legacy transition state.

Location, description and per-item color override are canonical attributes of
the Activity/Event authoring descriptor.  They are not Schedule, Context, Tag
or Life Area state.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "20260930_94"
down_revision: str | None = "20260929_93"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_OWNER = "dante_owner"
_RUNTIME = "dante_runtime"
_MIGRATOR = "dante_migrator"

_ACTIVITY_AUTHORING = (
    "dante.create_self_activity_authoring("
    "uuid,text,text,uuid,text,uuid,text,text,text)"
)
_EVENT_AUTHORING = (
    "dante.create_self_event_authoring("
    "uuid,text,text,uuid,text,text[],uuid,text,text,text)"
)


def _execute(sql: str) -> None:
    op.execute(sa.text(sql))


def _add_descriptor_metadata(table: str) -> None:
    op.add_column(table, sa.Column("description", sa.Text(), nullable=True), schema="dante")
    op.add_column(table, sa.Column("location", sa.Text(), nullable=True), schema="dante")
    op.add_column(table, sa.Column("color_code", sa.Text(), nullable=True), schema="dante")
    op.create_check_constraint(
        op.f(f"ck_{table}_description"),
        table,
        "description IS NULL OR (description=btrim(description) AND description<>'')",
        schema="dante",
    )
    op.create_check_constraint(
        op.f(f"ck_{table}_location"),
        table,
        "location IS NULL OR (location=btrim(location) AND location<>'')",
        schema="dante",
    )
    op.create_check_constraint(
        op.f(f"ck_{table}_color_code"),
        table,
        "color_code IS NULL OR color_code ~ '^#[0-9A-F]{6}$'",
        schema="dante",
    )


def upgrade() -> None:
    """Expose bounded authoring wrappers with optional actor-local organization."""
    _add_descriptor_metadata("activity_intention")
    _add_descriptor_metadata("event_expectation")

    _execute(r"""
        CREATE FUNCTION dante.create_self_activity_authoring(
            requested_self_person_ref uuid,
            requested_operation_id text,
            requested_intent_fingerprint text,
            requested_activity_ref uuid,
            requested_title text,
            requested_life_area_ref uuid,
            requested_description text,
            requested_location text,
            requested_color_code text
        )
        RETURNS TABLE(
            activity_ref uuid,
            title text,
            created_at timestamptz,
            life_area_ref uuid,
            assignment_revision bigint,
            description text,
            location text,
            color_code text,
            replayed boolean
        )
        LANGUAGE plpgsql SECURITY DEFINER VOLATILE PARALLEL UNSAFE
        SET search_path = pg_catalog, dante, pg_temp
        AS $function$
        #variable_conflict error
        DECLARE
            normalized_description text := NULLIF(btrim(requested_description), '');
            normalized_location text := NULLIF(btrim(requested_location), '');
            normalized_color text := NULLIF(upper(btrim(requested_color_code)), '');
            created_ref uuid;
            created_title text;
            created_at_value timestamptz;
            create_replayed boolean;
            assigned_area_ref uuid;
            assigned_revision bigint;
            assignment_replayed boolean;
            assigned_at_value timestamptz;
        BEGIN
            IF normalized_color IS NOT NULL AND normalized_color !~ '^#[0-9A-F]{6}$' THEN
                RAISE EXCEPTION USING ERRCODE='23514',
                    CONSTRAINT='ck_activity_intention_color_code',
                    MESSAGE='Activity color override rejected';
            END IF;

            SELECT created.activity_ref, created.title, created.created_at, created.replayed
              INTO created_ref, created_title, created_at_value, create_replayed
              FROM dante.create_self_activity(
                  requested_self_person_ref,
                  requested_operation_id,
                  requested_intent_fingerprint,
                  requested_activity_ref,
                  requested_title
              ) AS created;

            IF NOT create_replayed THEN
                UPDATE dante.activity_intention AS intention
                   SET description=normalized_description,
                       location=normalized_location,
                       color_code=normalized_color
                 WHERE intention.activity_ref=created_ref
                   AND intention.self_person_ref=requested_self_person_ref;
                IF NOT FOUND THEN
                    RAISE EXCEPTION USING ERRCODE='XX001',
                        MESSAGE='Activity authoring metadata lost canonical Activity';
                END IF;
            END IF;

            IF requested_life_area_ref IS NOT NULL THEN
                SELECT assigned.life_area_ref,
                       assigned.assignment_revision,
                       assigned.assigned_at,
                       assigned.replayed
                  INTO assigned_area_ref,
                       assigned_revision,
                       assigned_at_value,
                       assignment_replayed
                  FROM dante.assign_self_activity_life_area(
                      requested_self_person_ref,
                      requested_operation_id,
                      requested_intent_fingerprint,
                      created_ref,
                      requested_life_area_ref,
                      0
                  ) AS assigned;
                IF create_replayed IS DISTINCT FROM assignment_replayed THEN
                    RAISE EXCEPTION USING ERRCODE='XX001',
                        MESSAGE='Activity creation and optional Life Area assignment replay diverged';
                END IF;
            ELSE
                assigned_area_ref := NULL;
                assigned_revision := NULL;
            END IF;

            RETURN QUERY
            SELECT intention.activity_ref,
                   intention.title,
                   intention.created_at,
                   assigned_area_ref,
                   assigned_revision,
                   intention.description,
                   intention.location,
                   intention.color_code,
                   create_replayed
              FROM dante.activity_intention AS intention
             WHERE intention.activity_ref=created_ref
               AND intention.self_person_ref=requested_self_person_ref;
            IF NOT FOUND THEN
                RAISE EXCEPTION USING ERRCODE='XX001',
                    MESSAGE='Activity authoring result lost canonical Activity';
            END IF;
        END;
        $function$;
    """)

    _execute(r"""
        CREATE FUNCTION dante.create_self_event_authoring(
            requested_self_person_ref uuid,
            requested_operation_id text,
            requested_intent_fingerprint text,
            requested_event_ref uuid,
            requested_title text,
            requested_agenda_parts text[],
            requested_life_area_ref uuid,
            requested_description text,
            requested_location text,
            requested_color_code text
        )
        RETURNS TABLE(
            event_ref uuid,
            title text,
            created_at timestamptz,
            agenda_revision bigint,
            agenda_parts text[],
            life_area_ref uuid,
            assignment_revision bigint,
            description text,
            location text,
            color_code text,
            replayed boolean
        )
        LANGUAGE plpgsql SECURITY DEFINER VOLATILE PARALLEL UNSAFE
        SET search_path = pg_catalog, dante, pg_temp
        AS $function$
        #variable_conflict error
        DECLARE
            normalized_description text := NULLIF(btrim(requested_description), '');
            normalized_location text := NULLIF(btrim(requested_location), '');
            normalized_color text := NULLIF(upper(btrim(requested_color_code)), '');
            created_ref uuid;
            created_title text;
            created_at_value timestamptz;
            created_agenda_revision bigint;
            created_agenda_parts text[];
            create_replayed boolean;
            assigned_area_ref uuid;
            assigned_revision bigint;
            assignment_replayed boolean;
            assigned_at_value timestamptz;
        BEGIN
            IF normalized_color IS NOT NULL AND normalized_color !~ '^#[0-9A-F]{6}$' THEN
                RAISE EXCEPTION USING ERRCODE='23514',
                    CONSTRAINT='ck_event_expectation_color_code',
                    MESSAGE='Event color override rejected';
            END IF;

            SELECT created.event_ref,
                   created.title,
                   created.created_at,
                   created.agenda_revision,
                   created.agenda_parts,
                   created.replayed
              INTO created_ref,
                   created_title,
                   created_at_value,
                   created_agenda_revision,
                   created_agenda_parts,
                   create_replayed
              FROM dante.create_self_event_with_agenda(
                  requested_self_person_ref,
                  requested_operation_id,
                  requested_intent_fingerprint,
                  requested_event_ref,
                  requested_title,
                  requested_agenda_parts
              ) AS created;

            IF NOT create_replayed THEN
                UPDATE dante.event_expectation AS expectation
                   SET description=normalized_description,
                       location=normalized_location,
                       color_code=normalized_color
                 WHERE expectation.event_ref=created_ref
                   AND expectation.self_person_ref=requested_self_person_ref;
                IF NOT FOUND THEN
                    RAISE EXCEPTION USING ERRCODE='XX001',
                        MESSAGE='Event authoring metadata lost canonical Event';
                END IF;
            END IF;

            IF requested_life_area_ref IS NOT NULL THEN
                SELECT assigned.life_area_ref,
                       assigned.assignment_revision,
                       assigned.assigned_at,
                       assigned.replayed
                  INTO assigned_area_ref,
                       assigned_revision,
                       assigned_at_value,
                       assignment_replayed
                  FROM dante.assign_self_event_life_area(
                      requested_self_person_ref,
                      requested_operation_id,
                      requested_intent_fingerprint,
                      created_ref,
                      requested_life_area_ref,
                      0
                  ) AS assigned;
                IF create_replayed IS DISTINCT FROM assignment_replayed THEN
                    RAISE EXCEPTION USING ERRCODE='XX001',
                        MESSAGE='Event creation and optional Life Area assignment replay diverged';
                END IF;
            ELSE
                assigned_area_ref := NULL;
                assigned_revision := NULL;
            END IF;

            RETURN QUERY
            SELECT expectation.event_ref,
                   expectation.title,
                   expectation.created_at,
                   created_agenda_revision,
                   created_agenda_parts,
                   assigned_area_ref,
                   assigned_revision,
                   expectation.description,
                   expectation.location,
                   expectation.color_code,
                   create_replayed
              FROM dante.event_expectation AS expectation
             WHERE expectation.event_ref=created_ref
               AND expectation.self_person_ref=requested_self_person_ref;
            IF NOT FOUND THEN
                RAISE EXCEPTION USING ERRCODE='XX001',
                    MESSAGE='Event authoring result lost canonical Event';
            END IF;
        END;
        $function$;
    """)

    for signature in (_ACTIVITY_AUTHORING, _EVENT_AUTHORING):
        _execute(f"ALTER FUNCTION {signature} OWNER TO {_OWNER}")
        _execute(
            f"REVOKE ALL PRIVILEGES ON FUNCTION {signature} "
            f"FROM PUBLIC, {_RUNTIME}, {_MIGRATOR}"
        )
        _execute(f"GRANT EXECUTE ON FUNCTION {signature} TO {_RUNTIME}")

    # Canonical descriptor tables remain inaccessible to runtime roles; writes
    # happen only through the bounded SECURITY DEFINER authoring functions.
    for table in ("activity_intention", "event_expectation"):
        _execute(
            f"REVOKE ALL PRIVILEGES ON TABLE dante.{table} "
            f"FROM PUBLIC, {_RUNTIME}, {_MIGRATOR}"
        )


def downgrade() -> None:
    """Never erase accepted U2 authoring metadata or unassigned creation semantics."""
    raise RuntimeError("B14-U2 authoring persistence requires a reviewed forward migration")
