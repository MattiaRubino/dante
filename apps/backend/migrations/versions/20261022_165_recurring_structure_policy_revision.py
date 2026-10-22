"""Version recurring structure by governing Recurrence state.

The Create policy remains the immutable baseline for older Occurrences. A series
revision stores its complete Activity/Event structure against the newly accepted
Recurrence MaterialState in the same transaction. The materializer selects by
governing state, so protected older instances never inherit a newer template.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import JSONB

revision: str = "20261022_165"
down_revision: str | None = "20261021_164"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "recurring_structure_policy_revision",
        sa.Column("self_person_ref", sa.Uuid(), nullable=False),
        sa.Column("source_native_ref", sa.Uuid(), nullable=False),
        sa.Column("recurrence_state_ref", sa.Uuid(), nullable=False),
        sa.Column("owner_kind", sa.Text(), nullable=False),
        sa.Column("operation_id", sa.Text(), nullable=False),
        sa.Column("previous_state_ref", sa.Uuid(), nullable=False),
        sa.Column("request_hash", sa.Text(), nullable=False),
        sa.Column("preview_fingerprint", sa.Text(), nullable=False),
        sa.Column("superseded_count", sa.Integer(), nullable=False),
        sa.Column("protected_count", sa.Integer(), nullable=False),
        sa.Column("structure_snapshot", JSONB(), nullable=False),
        sa.Column("accepted_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint(
            "recurrence_state_ref", name="pk_recurring_structure_policy_revision"
        ),
        sa.UniqueConstraint(
            "self_person_ref",
            "operation_id",
            name="uq_recurring_structure_policy_revision_operation",
        ),
        sa.ForeignKeyConstraint(
            ["self_person_ref"],
            ["dante.person.person_ref"],
            name="fk_recurring_structure_policy_revision_person",
        ),
        sa.ForeignKeyConstraint(
            ["source_native_ref"],
            ["dante.native_address.native_ref"],
            name="fk_recurring_structure_policy_revision_source",
        ),
        sa.ForeignKeyConstraint(
            ["recurrence_state_ref"],
            ["dante.material_state_address.material_state_ref"],
            name="fk_recurring_structure_policy_revision_state",
        ),
        sa.CheckConstraint(
            "owner_kind IN ('routine','event')", name="ck_recurring_structure_policy_revision_owner"
        ),
        sa.CheckConstraint(
            "operation_id=btrim(operation_id) AND operation_id<>'' AND char_length(operation_id)<=200",
            name="ck_recurring_structure_policy_revision_operation",
        ),
        sa.CheckConstraint(
            "jsonb_typeof(structure_snapshot)='object' AND structure_snapshot<>'{}'::jsonb",
            name="ck_recurring_structure_policy_revision_snapshot",
        ),
        schema="dante",
    )
    op.create_index(
        "ix_recurring_structure_policy_revision_source",
        "recurring_structure_policy_revision",
        ["source_native_ref", "accepted_at"],
        schema="dante",
    )
    op.create_table(
        "recurring_occurrence_supersession",
        sa.Column("occurrence_ref", sa.Uuid(), nullable=False),
        sa.Column("self_person_ref", sa.Uuid(), nullable=False),
        sa.Column("source_native_ref", sa.Uuid(), nullable=False),
        sa.Column("replacement_state_ref", sa.Uuid(), nullable=False),
        sa.Column("operation_id", sa.Text(), nullable=False),
        sa.Column("accepted_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("occurrence_ref", name="pk_recurring_occurrence_supersession"),
        sa.UniqueConstraint(
            "self_person_ref", "operation_id", name="uq_recurring_occurrence_supersession_operation"
        ),
        sa.ForeignKeyConstraint(
            ["occurrence_ref"],
            ["dante.occurrence.occurrence_ref"],
            name="fk_recurring_occurrence_supersession_occurrence",
        ),
        sa.ForeignKeyConstraint(
            ["self_person_ref"],
            ["dante.person.person_ref"],
            name="fk_recurring_occurrence_supersession_person",
        ),
        sa.ForeignKeyConstraint(
            ["source_native_ref"],
            ["dante.native_address.native_ref"],
            name="fk_recurring_occurrence_supersession_source",
        ),
        sa.ForeignKeyConstraint(
            ["replacement_state_ref"],
            ["dante.material_state_address.material_state_ref"],
            name="fk_recurring_occurrence_supersession_state",
        ),
        schema="dante",
    )
    op.create_index(
        "ix_recurring_occurrence_supersession_source",
        "recurring_occurrence_supersession",
        ["source_native_ref"],
        schema="dante",
    )
    bind = op.get_bind()
    bind.exec_driver_sql(_SET_POLICY)
    bind.exec_driver_sql(_GET_POLICY)
    bind.exec_driver_sql(_GET_RECEIPT)
    bind.exec_driver_sql(_SUPERSEDE)
    bind.exec_driver_sql(_CURRENT_INVENTORY)
    bind.exec_driver_sql(
        "REVOKE ALL ON dante.recurring_structure_policy_revision FROM PUBLIC,dante_runtime,dante_migrator"
    )
    bind.exec_driver_sql(
        "REVOKE ALL ON dante.recurring_occurrence_supersession FROM PUBLIC,dante_runtime,dante_migrator"
    )
    for signature in (
        "set_self_recurring_structure_policy_revision(uuid,text,text,uuid,uuid,uuid,jsonb,text,text,integer,integer)",
        "get_self_recurring_structure_policy_revision(uuid,text,uuid,uuid)",
        "get_self_recurring_structure_policy_operation(uuid,text)",
        "supersede_self_clean_recurring_occurrence(uuid,uuid,uuid,uuid,text,text)",
    ):
        bind.exec_driver_sql(
            f"REVOKE ALL ON FUNCTION dante.{signature} FROM PUBLIC,dante_runtime,dante_migrator"
        )
        bind.exec_driver_sql(f"GRANT EXECUTE ON FUNCTION dante.{signature} TO dante_runtime")


def downgrade() -> None:
    raise RuntimeError("20261022_165 is forward-only")


_SET_POLICY = r"""
CREATE FUNCTION dante.set_self_recurring_structure_policy_revision(
    actor uuid, requested_operation text, requested_owner text,
    requested_source uuid, requested_previous_state uuid,
    requested_state uuid, requested_snapshot jsonb,
    requested_hash text, requested_preview text,
    requested_superseded integer, requested_protected integer
) RETURNS TABLE(accepted_at timestamptz, replayed boolean)
LANGUAGE plpgsql SECURITY DEFINER VOLATILE PARALLEL UNSAFE
SET search_path=pg_catalog,dante,pg_temp AS $$
#variable_conflict error
DECLARE prior dante.recurring_structure_policy_revision%ROWTYPE;
        state_owner uuid; current_state uuid; previous_closed boolean;
BEGIN
    IF requested_operation IS NULL OR requested_operation<>btrim(requested_operation)
       OR requested_operation='' OR char_length(requested_operation)>200
       OR requested_owner IS NULL OR requested_owner NOT IN ('routine','event')
       OR requested_snapshot IS NULL OR jsonb_typeof(requested_snapshot)<>'object'
       OR requested_snapshot='{}'::jsonb OR requested_previous_state IS NULL
       OR requested_state IS NULL OR requested_state=requested_previous_state
       OR requested_hash !~ '^[0-9a-f]{64}$' OR requested_hash IS NULL
       OR requested_preview !~ '^[0-9a-f]{64}$' OR requested_preview IS NULL
       OR requested_superseded IS NULL OR requested_superseded<0
       OR requested_protected IS NULL OR requested_protected<0 THEN
        RAISE EXCEPTION USING ERRCODE='22023',
          CONSTRAINT='recurring_structure_policy_invalid', MESSAGE='Invalid recurring structure revision';
    END IF;
    IF requested_snapshot->'version' IS DISTINCT FROM '1'::jsonb
       OR (requested_owner='routine' AND (
            jsonb_typeof(requested_snapshot->'activity_template') IS DISTINCT FROM 'object'
            OR requested_snapshot->'activity_template'->'version' IS DISTINCT FROM '1'::jsonb
            OR (requested_snapshot->'activity_template' ? 'life_area_ref'
                AND jsonb_typeof(requested_snapshot->'activity_template'->'life_area_ref')
                    NOT IN ('string','null'))
            OR COALESCE(requested_snapshot->>'duration_minutes','') !~ '^[0-9]+$'
            OR (requested_snapshot->>'duration_minutes')::numeric NOT BETWEEN 1 AND 525600
            OR (requested_snapshot->'reminder_lead_minutes' IS DISTINCT FROM 'null'::jsonb
                AND (COALESCE(requested_snapshot->>'reminder_lead_minutes','') !~ '^[0-9]+$'
                  OR (requested_snapshot->>'reminder_lead_minutes')::numeric NOT BETWEEN 0 AND 10080))
          ))
       OR (requested_owner='event' AND (
            COALESCE(requested_snapshot->>'placement_kind','') NOT IN ('timed','all_day')
            OR COALESCE(requested_snapshot->>'reality_mode','') NOT IN
               ('manual','review_on_end','auto_confirm_outcome')
            OR jsonb_typeof(requested_snapshot->'objectives') IS DISTINCT FROM 'array'
            OR (requested_snapshot->>'placement_kind'='timed' AND (
                COALESCE(requested_snapshot->>'duration_minutes','') !~ '^[0-9]+$'
                OR (requested_snapshot->>'duration_minutes')::numeric NOT BETWEEN 1 AND 525600
                OR requested_snapshot->'duration_days' IS DISTINCT FROM 'null'::jsonb))
            OR (requested_snapshot->>'placement_kind'='all_day' AND (
                COALESCE(requested_snapshot->>'duration_days','') !~ '^[0-9]+$'
                OR (requested_snapshot->>'duration_days')::numeric NOT BETWEEN 1 AND 3660
                OR requested_snapshot->'duration_minutes' IS DISTINCT FROM 'null'::jsonb
                OR requested_snapshot->'reminder_lead_minutes' IS DISTINCT FROM 'null'::jsonb))
            OR (requested_snapshot->'reminder_lead_minutes' IS DISTINCT FROM 'null'::jsonb
                AND (COALESCE(requested_snapshot->>'reminder_lead_minutes','') !~ '^[0-9]+$'
                  OR (requested_snapshot->>'reminder_lead_minutes')::numeric NOT BETWEEN 0 AND 10080))
          )) THEN
        RAISE EXCEPTION USING ERRCODE='22023',
          CONSTRAINT='recurring_structure_policy_invalid', MESSAGE='Malformed recurring structure snapshot';
    END IF;
    -- Serialize with the materialization admission lock. Series acceptance
    -- takes this lock before replacing the Recurrence inside its transaction.
    PERFORM pg_advisory_xact_lock(hashtextextended(
        'dante:recurrence-materialization:' || requested_source::text,0));
    IF requested_owner='routine' THEN
        PERFORM 1 FROM dante.routine_intention r
         WHERE r.routine_ref=requested_source AND r.self_person_ref=actor FOR UPDATE;
        IF NOT FOUND THEN
            RAISE EXCEPTION USING ERRCODE='23503',
              CONSTRAINT='recurring_structure_source_unavailable', MESSAGE='Routine outside self scope';
        END IF;
        IF requested_snapshot->'activity_template' ? 'life_area_ref'
           AND requested_snapshot->'activity_template'->'life_area_ref'<>'null'::jsonb
           AND NOT EXISTS (
             SELECT 1 FROM dante.life_area area
              WHERE area.life_area_ref=(requested_snapshot->'activity_template'->>'life_area_ref')::uuid
                AND area.self_person_ref=actor AND NOT area.archived
           ) THEN
            RAISE EXCEPTION USING ERRCODE='23503',
              CONSTRAINT='recurring_structure_life_area_unavailable',
              MESSAGE='Recurring Life Area outside self scope';
        END IF;
        SELECT s.routine_ref INTO state_owner FROM dante.routine_recurrence_state s
         WHERE s.material_state_ref=requested_state;
        SELECT h.material_state_ref INTO current_state
          FROM dante.routine_recurrence_current_history h
         WHERE h.routine_ref=requested_source AND h.current_until_at IS NULL;
        SELECT EXISTS(SELECT 1 FROM dante.routine_recurrence_current_history h
          WHERE h.routine_ref=requested_source
            AND h.material_state_ref=requested_previous_state
            AND h.current_until_at=(SELECT current_from_at
              FROM dante.routine_recurrence_current_history
              WHERE routine_ref=requested_source AND current_until_at IS NULL))
          INTO previous_closed;
    ELSE
        PERFORM 1 FROM dante.event_expectation e
         WHERE e.event_ref=requested_source AND e.self_person_ref=actor FOR UPDATE;
        IF NOT FOUND THEN
            RAISE EXCEPTION USING ERRCODE='23503',
              CONSTRAINT='recurring_structure_source_unavailable', MESSAGE='Event outside self scope';
        END IF;
        IF requested_snapshot ? 'life_area_ref'
           AND requested_snapshot->'life_area_ref'<>'null'::jsonb
           AND NOT EXISTS (
             SELECT 1 FROM dante.life_area area
              WHERE area.life_area_ref=(requested_snapshot->>'life_area_ref')::uuid
                AND area.self_person_ref=actor AND NOT area.archived
           ) THEN
            RAISE EXCEPTION USING ERRCODE='23503',
              CONSTRAINT='recurring_structure_life_area_unavailable',
              MESSAGE='Recurring Event Life Area outside self scope';
        END IF;
        SELECT s.event_ref INTO state_owner FROM dante.event_recurrence_state s
         WHERE s.material_state_ref=requested_state;
        SELECT h.material_state_ref INTO current_state
          FROM dante.event_recurrence_current_history h
         WHERE h.event_ref=requested_source AND h.current_until_at IS NULL;
        SELECT EXISTS(SELECT 1 FROM dante.event_recurrence_current_history h
          WHERE h.event_ref=requested_source
            AND h.material_state_ref=requested_previous_state
            AND h.current_until_at=(SELECT current_from_at
              FROM dante.event_recurrence_current_history
              WHERE event_ref=requested_source AND current_until_at IS NULL))
          INTO previous_closed;
    END IF;
    IF state_owner IS DISTINCT FROM requested_source
       OR current_state IS DISTINCT FROM requested_state OR NOT previous_closed THEN
        RAISE EXCEPTION USING ERRCODE='23505',
          CONSTRAINT='recurring_structure_state_conflict', MESSAGE='Recurrence state changed';
    END IF;
    SELECT * INTO prior FROM dante.recurring_structure_policy_revision p
     WHERE p.self_person_ref=actor AND p.operation_id=requested_operation;
    IF FOUND THEN
        IF prior.owner_kind<>requested_owner
           OR prior.source_native_ref<>requested_source
           OR prior.previous_state_ref<>requested_previous_state
           OR prior.recurrence_state_ref<>requested_state
           OR prior.request_hash<>requested_hash
           OR prior.preview_fingerprint<>requested_preview
           OR prior.superseded_count<>requested_superseded
           OR prior.protected_count<>requested_protected
           OR prior.structure_snapshot<>requested_snapshot THEN
            RAISE EXCEPTION USING ERRCODE='23505',
              CONSTRAINT='recurring_structure_operation_reuse', MESSAGE='Operation intent differs';
        END IF;
        RETURN QUERY SELECT prior.accepted_at,true;
        RETURN;
    END IF;
    INSERT INTO dante.recurring_structure_policy_revision(
        self_person_ref,source_native_ref,recurrence_state_ref,owner_kind,
        operation_id,previous_state_ref,request_hash,preview_fingerprint,
        superseded_count,protected_count,structure_snapshot,accepted_at
    ) VALUES (
        actor,requested_source,requested_state,requested_owner,
        requested_operation,requested_previous_state,requested_hash,requested_preview,
        requested_superseded,requested_protected,requested_snapshot,statement_timestamp()
    ) RETURNING recurring_structure_policy_revision.accepted_at
      INTO accepted_at;
    replayed:=false;
    RETURN NEXT;
END;
$$;
"""


_GET_POLICY = r"""
CREATE FUNCTION dante.get_self_recurring_structure_policy_revision(
    actor uuid, requested_owner text, requested_source uuid, requested_state uuid
) RETURNS TABLE(structure_snapshot jsonb, accepted_at timestamptz)
LANGUAGE plpgsql SECURITY DEFINER STABLE PARALLEL RESTRICTED
SET search_path=pg_catalog,dante,pg_temp AS $$
DECLARE owned boolean;
BEGIN
    IF requested_owner='routine' THEN
        SELECT EXISTS(SELECT 1 FROM dante.routine_intention r
           WHERE r.self_person_ref=actor AND r.routine_ref=requested_source)
           AND EXISTS(SELECT 1 FROM dante.routine_recurrence_state s
           WHERE s.routine_ref=requested_source AND s.material_state_ref=requested_state)
          INTO owned;
    ELSIF requested_owner='event' THEN
        SELECT EXISTS(SELECT 1 FROM dante.event_expectation e
           WHERE e.self_person_ref=actor AND e.event_ref=requested_source)
           AND EXISTS(SELECT 1 FROM dante.event_recurrence_state s
           WHERE s.event_ref=requested_source AND s.material_state_ref=requested_state)
          INTO owned;
    ELSE
        RETURN;
    END IF;
    IF NOT owned THEN RETURN; END IF;
    RETURN QUERY SELECT p.structure_snapshot,p.accepted_at
      FROM dante.recurring_structure_policy_revision p
       WHERE p.self_person_ref=actor AND p.owner_kind=requested_owner
         AND p.source_native_ref=requested_source
         AND p.recurrence_state_ref=requested_state;
END;
$$;
"""


_GET_RECEIPT = r"""
CREATE FUNCTION dante.get_self_recurring_structure_policy_operation(
    actor uuid, requested_operation text
) RETURNS TABLE(
    source_native_ref uuid, recurrence_state_ref uuid,
    previous_state_ref uuid, request_hash text, preview_fingerprint text,
    superseded_count integer, protected_count integer, accepted_at timestamptz
)
LANGUAGE sql SECURITY DEFINER STABLE PARALLEL RESTRICTED
SET search_path=pg_catalog,dante,pg_temp AS $$
    SELECT p.source_native_ref,p.recurrence_state_ref,p.previous_state_ref,
           p.request_hash,p.preview_fingerprint,p.superseded_count,
           p.protected_count,p.accepted_at
      FROM dante.recurring_structure_policy_revision p
     WHERE p.self_person_ref=$1 AND p.operation_id=$2
$$;
"""


_SUPERSEDE = r"""
CREATE FUNCTION dante.supersede_self_clean_recurring_occurrence(
    actor uuid, requested_occurrence uuid, requested_source uuid,
    requested_replacement_state uuid, requested_operation text, requested_zone text
) RETURNS TABLE(accepted_at timestamptz, replayed boolean)
LANGUAGE plpgsql SECURITY DEFINER VOLATILE PARALLEL UNSAFE
SET search_path=pg_catalog,dante,pg_temp AS $$
#variable_conflict error
DECLARE owned record; prior dante.recurring_occurrence_supersession%ROWTYPE;
        current_state uuid;
BEGIN
    IF requested_operation IS NULL OR requested_operation<>btrim(requested_operation)
       OR requested_operation='' OR char_length(requested_operation)>200 THEN
        RAISE EXCEPTION USING ERRCODE='22023',
          CONSTRAINT='recurring_supersession_invalid', MESSAGE='Invalid operation id';
    END IF;
    PERFORM pg_advisory_xact_lock(hashtextextended(
        'dante:recurrence-materialization:' || requested_source::text,0));
    SELECT * INTO owned FROM dante.get_self_occurrence(actor,requested_occurrence);
    IF NOT FOUND OR owned.source_native_ref<>requested_source
       OR owned.origin_code<>'recurrence_generated'
       OR owned.governing_recurrence_state_ref=requested_replacement_state THEN
        RAISE EXCEPTION USING ERRCODE='23503',
          CONSTRAINT='recurring_supersession_unavailable', MESSAGE='Expected instance unavailable';
    END IF;
    SELECT * INTO prior FROM dante.recurring_occurrence_supersession s
     WHERE s.occurrence_ref=requested_occurrence FOR UPDATE;
    IF FOUND THEN
        IF prior.self_person_ref<>actor OR prior.source_native_ref<>requested_source
           OR prior.replacement_state_ref<>requested_replacement_state
           OR prior.operation_id<>requested_operation THEN
            RAISE EXCEPTION USING ERRCODE='23505',
              CONSTRAINT='recurring_supersession_conflict', MESSAGE='Supersession changed';
        END IF;
        RETURN QUERY SELECT prior.accepted_at,true;
        RETURN;
    END IF;
    IF EXISTS(SELECT 1 FROM dante.recurring_occurrence_supersession s
      WHERE s.self_person_ref=actor AND s.operation_id=requested_operation) THEN
        RAISE EXCEPTION USING ERRCODE='23505',
          CONSTRAINT='recurring_supersession_operation_reuse', MESSAGE='Operation reused';
    END IF;
    IF owned.skipped
       OR dante.get_self_occurrence_edit_protection(actor,requested_occurrence) IS NOT NULL
       OR dante.occurrence_edit_coordinate_instant(
            actor,requested_occurrence,requested_zone) <= clock_timestamp() THEN
        RAISE EXCEPTION USING ERRCODE='23505',
          CONSTRAINT='recurring_supersession_protected', MESSAGE='Future instance has facts or edits';
    END IF;
    IF EXISTS(SELECT 1 FROM dante.routine_intention r
       WHERE r.routine_ref=requested_source AND r.self_person_ref=actor) THEN
        SELECT h.material_state_ref INTO current_state
          FROM dante.routine_recurrence_current_history h
         WHERE h.routine_ref=requested_source AND h.current_until_at IS NULL;
    ELSE
        SELECT h.material_state_ref INTO current_state
          FROM dante.event_recurrence_current_history h
          JOIN dante.event_expectation e ON e.event_ref=h.event_ref
         WHERE h.event_ref=requested_source AND e.self_person_ref=actor
           AND h.current_until_at IS NULL;
    END IF;
    IF current_state IS DISTINCT FROM requested_replacement_state THEN
        RAISE EXCEPTION USING ERRCODE='23505',
          CONSTRAINT='recurring_supersession_state_conflict', MESSAGE='Recurrence state changed';
    END IF;
    INSERT INTO dante.recurring_occurrence_supersession(
        occurrence_ref,self_person_ref,source_native_ref,replacement_state_ref,
        operation_id,accepted_at
    ) VALUES (
        requested_occurrence,actor,requested_source,requested_replacement_state,
        requested_operation,statement_timestamp()
    ) RETURNING recurring_occurrence_supersession.accepted_at INTO accepted_at;
    replayed:=false;
    RETURN NEXT;
END;
$$;
"""


_CURRENT_INVENTORY = r"""
CREATE OR REPLACE FUNCTION dante.list_self_recurrence_edit_occurrences(
    requested_self_person_ref uuid, requested_selected_occurrence_ref uuid
) RETURNS TABLE(
    occurrence_ref uuid, source_native_ref uuid,
    governing_recurrence_state_ref uuid, origin_code text, family_code text,
    generated_date date, generated_wall_time time, clock_basis_code text,
    zone_id text, resolved_at timestamptz, expected_at timestamptz,
    period_start_date date, period_end_date_exclusive date, frame_code text,
    quota_zone_id text, position_index integer, skipped boolean,
    skip_reason text, skipped_at timestamptz
)
LANGUAGE plpgsql SECURITY DEFINER STABLE PARALLEL RESTRICTED
SET search_path=pg_catalog,dante,pg_temp AS $$
#variable_conflict error
DECLARE bound_source_ref uuid;
BEGIN
    SELECT picked.source_native_ref INTO bound_source_ref
      FROM dante.get_self_occurrence(
          requested_self_person_ref,requested_selected_occurrence_ref) picked;
    IF bound_source_ref IS NULL OR EXISTS (
        SELECT 1 FROM dante.recurring_occurrence_supersession retired
         WHERE retired.occurrence_ref=requested_selected_occurrence_ref
           AND retired.self_person_ref=requested_self_person_ref
    ) THEN
        RAISE EXCEPTION USING ERRCODE='23503',
          CONSTRAINT='recurrence_edit_occurrence_unavailable',
          MESSAGE='Selected current Occurrence unavailable';
    END IF;
    IF (SELECT count(*) FROM (
        SELECT 1 FROM dante.occurrence_generation candidate
         WHERE candidate.source_native_ref=bound_source_ref
           AND NOT EXISTS (
             SELECT 1 FROM dante.recurring_occurrence_supersession retired
              WHERE retired.occurrence_ref=candidate.occurrence_ref)
         LIMIT 10001
    ) bounded)>10000 THEN
        RAISE EXCEPTION USING ERRCODE='22023',
          CONSTRAINT='recurrence_edit_inventory_limit',
          MESSAGE='More than 10000 current materialized Occurrences';
    END IF;
    RETURN QUERY
    SELECT item.* FROM dante.occurrence_generation generation
      CROSS JOIN LATERAL dante.get_self_occurrence(
        requested_self_person_ref,generation.occurrence_ref) item
     WHERE generation.source_native_ref=bound_source_ref
       AND NOT EXISTS (
         SELECT 1 FROM dante.recurring_occurrence_supersession retired
          WHERE retired.occurrence_ref=generation.occurrence_ref)
     ORDER BY item.occurrence_ref;
END;
$$;
"""
