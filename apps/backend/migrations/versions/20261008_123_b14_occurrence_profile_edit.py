"""B14-M1: append-only accepted occurrence profile edits (single or following).

Read-only B06 authority remains unchanged. A selected occurrence is always in
scope. The other past occurrences are never rewritten. A following edit also
applies to future occurrences generated after acceptance via a dated policy.
"""
from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import JSONB

revision: str = "20261008_123"
down_revision: str | None = "20261008_122"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

def upgrade() -> None:
    op.create_table(
        "occurrence_profile_edit",
        sa.Column("self_person_ref", sa.Uuid(), nullable=False),
        sa.Column("operation_id", sa.Text(), nullable=False),
        sa.Column("source_native_ref", sa.Uuid(), nullable=False),
        sa.Column("selected_occurrence_ref", sa.Uuid(), nullable=False),
        sa.Column("revision", sa.BigInteger(), nullable=False),
        sa.Column("expected_revision", sa.BigInteger(), nullable=False),
        sa.Column("expected_recurrence_state_ref", sa.Uuid()),
        sa.Column("scope_code", sa.Text(), nullable=False),
        sa.Column("effective_zone_id", sa.Text(), nullable=False),
        sa.Column("anchor_at", sa.DateTime(timezone=True)),
        sa.Column("accepted_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("profile_patch", JSONB(), nullable=False),
        sa.Column("target_occurrence_refs", sa.ARRAY(sa.Uuid()), nullable=False),
        sa.PrimaryKeyConstraint("self_person_ref","operation_id",
                                name="pk_occurrence_profile_edit"),
        sa.UniqueConstraint("source_native_ref","revision",
                            name="uq_occurrence_profile_edit_source_revision"),
        sa.ForeignKeyConstraint(["self_person_ref"],["dante.person.person_ref"],
                                name="fk_occurrence_profile_edit_person"),
        sa.ForeignKeyConstraint(["source_native_ref"],["dante.native_address.native_ref"],
                                name="fk_occurrence_profile_edit_source"),
        sa.ForeignKeyConstraint(["selected_occurrence_ref"],["dante.occurrence.occurrence_ref"],
                                name="fk_occurrence_profile_edit_occurrence"),
        sa.CheckConstraint("revision>=1 AND expected_revision>=0",
                           name=op.f("ck_occurrence_profile_edit_revision")),
        sa.CheckConstraint("operation_id=btrim(operation_id) AND operation_id<>'' "
                           "AND char_length(operation_id)<=200",
                           name=op.f("ck_occurrence_profile_edit_operation")),
        sa.CheckConstraint("scope_code IN ('only_this','this_and_following')",
                           name=op.f("ck_occurrence_profile_edit_scope")),
        sa.CheckConstraint("jsonb_typeof(profile_patch)='object' AND "
                           "profile_patch<>'{}'::jsonb",
                           name=op.f("ck_occurrence_profile_edit_patch")),
        schema="dante"
    )
    db=op.get_bind()
    db.exec_driver_sql("ALTER TABLE dante.occurrence_profile_edit OWNER TO dante_owner")
    db.exec_driver_sql("REVOKE ALL ON dante.occurrence_profile_edit "
                       "FROM PUBLIC,dante_runtime,dante_migrator")
    for ddl in (_COORDINATE_INSTANT,_PROFILE_PATCH,_ACTIVITY_ORIGIN,_EDIT_STATE,_ACCEPT_EDIT):
        db.execute(sa.text(ddl))
    for signature in (
        "occurrence_edit_coordinate_instant(uuid,uuid,text)",
        "get_self_occurrence_profile_patch(uuid,uuid)",
        "get_self_materialized_activity_occurrence(uuid,uuid)",
        "get_self_occurrence_edit_revision(uuid,uuid)",
        "accept_self_occurrence_profile_edit(uuid,uuid,text,bigint,uuid,text,text,jsonb)",
    ):
        db.exec_driver_sql(f"ALTER FUNCTION dante.{signature} OWNER TO dante_owner")
        db.exec_driver_sql(f"REVOKE ALL ON FUNCTION dante.{signature} "
                           "FROM PUBLIC,dante_runtime,dante_migrator")
        db.exec_driver_sql(f"GRANT EXECUTE ON FUNCTION dante.{signature} TO dante_runtime")

def downgrade() -> None:
    raise RuntimeError("Accepted occurrence edit history is forward-only")


_COORDINATE_INSTANT = r"""
CREATE FUNCTION dante.occurrence_edit_coordinate_instant(
    actor uuid, requested_occurrence uuid, effective_zone text
) RETURNS timestamptz
LANGUAGE plpgsql SECURITY DEFINER STABLE PARALLEL RESTRICTED
SET search_path=pg_catalog,dante,pg_temp AS $$
#variable_conflict error
DECLARE coord record; civil timestamp; resolved timestamptz; zone text;
BEGIN
    IF effective_zone IS NULL OR effective_zone<>btrim(effective_zone)
       OR effective_zone='' OR char_length(effective_zone)>200
       OR NOT EXISTS(SELECT 1 FROM pg_catalog.pg_timezone_names z
                     WHERE z.name=effective_zone) THEN
        RAISE EXCEPTION USING ERRCODE='22023',
            CONSTRAINT='occurrence_edit_invalid_zone',
            MESSAGE='Invalid effective timezone';
    END IF;
    SELECT * INTO coord FROM dante.get_self_occurrence(actor,requested_occurrence);
    IF NOT FOUND THEN
        RAISE EXCEPTION USING ERRCODE='23503',
            CONSTRAINT='occurrence_edit_unavailable',
            MESSAGE='Occurrence outside self scope';
    END IF;
    IF coord.origin_code='explicit_extra' THEN RETURN NULL; END IF;
    IF coord.resolved_at IS NOT NULL THEN RETURN coord.resolved_at; END IF;
    IF coord.expected_at IS NOT NULL THEN RETURN coord.expected_at; END IF;
    IF coord.clock_basis_code='named_zone' THEN
        RAISE EXCEPTION USING ERRCODE='22023',
            CONSTRAINT='occurrence_edit_unresolved_zone',
            MESSAGE='Unresolved named-zone coordinate';
    END IF;
    IF coord.generated_date IS NOT NULL THEN
        civil:=coord.generated_date+COALESCE(coord.generated_wall_time,'00:00'::time);
        zone:=CASE WHEN coord.clock_basis_code='absolute_utc' THEN 'UTC'
                   ELSE effective_zone END;
    ELSIF coord.period_start_date IS NOT NULL THEN
        civil:=coord.period_start_date::timestamp; zone:=effective_zone;
    ELSE
        RAISE EXCEPTION USING ERRCODE='22023',
            CONSTRAINT='occurrence_edit_unordered_coordinate',
            MESSAGE='Unordered Occurrence coordinate';
    END IF;
    resolved:=civil AT TIME ZONE zone;
    IF (resolved AT TIME ZONE zone) IS DISTINCT FROM civil THEN
        RAISE EXCEPTION USING ERRCODE='22023',
            CONSTRAINT='occurrence_edit_dst_gap',
            MESSAGE='Invalid local DST time';
    END IF;
    RETURN resolved;
END;
$$;
"""

_PROFILE_PATCH = r"""
CREATE FUNCTION dante.get_self_occurrence_profile_patch(
    actor uuid, requested_occurrence uuid
) RETURNS jsonb
LANGUAGE plpgsql SECURITY DEFINER STABLE PARALLEL RESTRICTED
SET search_path=pg_catalog,dante,pg_temp AS $$
#variable_conflict error
DECLARE bound_source uuid; combined jsonb;
BEGIN
    SELECT o.source_native_ref INTO bound_source
      FROM dante.get_self_occurrence(actor,requested_occurrence) o;
    IF NOT FOUND THEN
        RAISE EXCEPTION USING ERRCODE='23503',
            CONSTRAINT='occurrence_edit_unavailable',
            MESSAGE='Occurrence outside self scope';
    END IF;
    SELECT jsonb_object_agg(field.key,field.value ORDER BY edits.revision)
      INTO combined
      FROM dante.occurrence_profile_edit edits
      CROSS JOIN LATERAL jsonb_each(edits.profile_patch) field
     WHERE edits.self_person_ref=actor
       AND edits.source_native_ref=bound_source
       AND (
           edits.selected_occurrence_ref=requested_occurrence
           OR (
               edits.scope_code='this_and_following'
               AND dante.occurrence_edit_coordinate_instant(
                   actor,requested_occurrence,edits.effective_zone_id
               ) > GREATEST(edits.anchor_at,edits.accepted_at)
           )
       );
    RETURN COALESCE(combined,'{}'::jsonb);
END;
$$;
"""

_ACCEPT_EDIT = r"""
CREATE FUNCTION dante.accept_self_occurrence_profile_edit(
    actor uuid, selected_ref uuid, requested_operation text,
    requested_expected_revision bigint, requested_expected_state uuid,
    requested_scope text, requested_zone text, requested_patch jsonb
) RETURNS TABLE(
    revision bigint, source_native_ref uuid, selected_occurrence_ref uuid,
    target_occurrence_refs uuid[], accepted_at timestamptz, replayed boolean
)
LANGUAGE plpgsql SECURITY DEFINER VOLATILE PARALLEL UNSAFE
SET search_path=pg_catalog,dante,pg_temp AS $$
#variable_conflict error
DECLARE anchor_row record;
        existing dante.occurrence_profile_edit%ROWTYPE;
        source_ref uuid; is_routine boolean; current_revision bigint;
        current_state uuid; anchor timestamptz; accepted timestamptz;
        candidate record; instant timestamptz;
        targets uuid[]; patch_key text; patch_value jsonb;
BEGIN
    IF requested_operation IS NULL OR requested_operation<>btrim(requested_operation)
       OR requested_operation='' OR char_length(requested_operation)>200
       OR requested_expected_revision IS NULL OR requested_expected_revision<0
       OR requested_scope IS NULL
       OR requested_scope NOT IN ('only_this','this_and_following')
       OR requested_patch IS NULL OR jsonb_typeof(requested_patch)<>'object'
       OR requested_patch='{}'::jsonb THEN
        RAISE EXCEPTION USING ERRCODE='22023',
            CONSTRAINT='occurrence_edit_invalid',
            MESSAGE='Invalid scoped edit request';
    END IF;
    FOR patch_key,patch_value IN SELECT key,value FROM jsonb_each(requested_patch) LOOP
        IF patch_key NOT IN ('title','description','location','color_code')
           OR (patch_key='title' AND (
               jsonb_typeof(patch_value)<>'string'
               OR btrim(patch_value #>> '{}')=''
               OR char_length(patch_value #>> '{}')>300
               OR btrim(patch_value #>> '{}')<>(patch_value #>> '{}')))
           OR (patch_key IN ('description','location') AND
               patch_value<>'null'::jsonb AND (
                  jsonb_typeof(patch_value)<>'string'
                  OR btrim(patch_value #>> '{}')=''
                  OR btrim(patch_value #>> '{}')<>(patch_value #>> '{}')))
           OR (patch_key='color_code' AND patch_value<>'null'::jsonb AND
               (jsonb_typeof(patch_value)<>'string'
                OR (patch_value #>> '{}') !~ '^#[0-9A-F]{6}$')) THEN
            RAISE EXCEPTION USING ERRCODE='22023',
                CONSTRAINT='occurrence_edit_invalid_patch',
                MESSAGE='Unsupported or invalid editable metadata field';
        END IF;
    END LOOP;
    SELECT * INTO anchor_row FROM dante.get_self_occurrence(actor,selected_ref);
    IF NOT FOUND THEN
        RAISE EXCEPTION USING ERRCODE='23503',
            CONSTRAINT='occurrence_edit_unavailable',
            MESSAGE='Selected occurrence outside self scope';
    END IF;
    source_ref:=anchor_row.source_native_ref;
    SELECT EXISTS (
        SELECT 1 FROM dante.routine_intention r
         WHERE r.routine_ref=source_ref AND r.self_person_ref=actor
    ) INTO is_routine;
    IF is_routine THEN
        PERFORM 1 FROM dante.routine_intention r
         WHERE r.routine_ref=source_ref AND r.self_person_ref=actor FOR UPDATE;
    ELSE
        PERFORM 1 FROM dante.event_expectation e
         WHERE e.event_ref=source_ref AND e.self_person_ref=actor FOR UPDATE;
        IF NOT FOUND THEN
            RAISE EXCEPTION USING ERRCODE='23503',
                CONSTRAINT='occurrence_edit_unavailable',
                MESSAGE='Source outside self scope';
        END IF;
    END IF;
    SELECT * INTO existing FROM dante.occurrence_profile_edit e
     WHERE e.self_person_ref=actor AND e.operation_id=requested_operation;
    IF FOUND THEN
        IF existing.selected_occurrence_ref<>selected_ref
           OR existing.expected_revision<>requested_expected_revision
           OR existing.expected_recurrence_state_ref IS DISTINCT FROM requested_expected_state
           OR existing.scope_code<>requested_scope
           OR existing.effective_zone_id IS DISTINCT FROM requested_zone
           OR existing.profile_patch IS DISTINCT FROM requested_patch THEN
            RAISE EXCEPTION USING ERRCODE='23505',
                CONSTRAINT='pk_occurrence_profile_edit',
                MESSAGE='Operation reused for different scoped edit';
        END IF;
        revision:=existing.revision;
        source_native_ref:=existing.source_native_ref;
        selected_occurrence_ref:=existing.selected_occurrence_ref;
        target_occurrence_refs:=existing.target_occurrence_refs;
        accepted_at:=existing.accepted_at;
        replayed:=true;
        RETURN NEXT; RETURN;
    END IF;
    SELECT COALESCE(MAX(e.revision),0) INTO current_revision
      FROM dante.occurrence_profile_edit e
     WHERE e.source_native_ref=source_ref;
    IF current_revision<>requested_expected_revision THEN
        RAISE EXCEPTION USING ERRCODE='23505',
            CONSTRAINT='occurrence_edit_stale',
            MESSAGE='Source edit revision changed';
    END IF;
    IF is_routine THEN
        SELECT material_state_ref INTO current_state
          FROM dante.get_self_routine_recurrence(actor,source_ref);
    ELSE
        SELECT material_state_ref INTO current_state
          FROM dante.get_self_event_recurrence(actor,source_ref);
    END IF;
    IF current_state IS DISTINCT FROM requested_expected_state THEN
        RAISE EXCEPTION USING ERRCODE='23505',
            CONSTRAINT='occurrence_edit_recurrence_stale',
            MESSAGE='Recurrence changed since preview';
    END IF;
    accepted:=clock_timestamp();
    targets:=ARRAY[selected_ref];
    IF requested_scope='this_and_following' THEN
        IF anchor_row.origin_code<>'recurrence_generated' THEN
            RAISE EXCEPTION USING ERRCODE='22023',
                CONSTRAINT='occurrence_edit_not_generated',
                MESSAGE='Following scope requires a generated selected instance';
        END IF;
        anchor:=dante.occurrence_edit_coordinate_instant(actor,selected_ref,requested_zone);
    ELSE
        anchor:=NULL;
    END IF;

    -- This is the same fully materialized, bounded inventory as M1-B.
    -- Its SELECT and all validations happen within this one source lock.
    FOR candidate IN
        SELECT * FROM dante.list_self_recurrence_edit_occurrences(actor,selected_ref)
    LOOP
        IF requested_scope='only_this'
           OR candidate.occurrence_ref=selected_ref
           OR candidate.origin_code<>'recurrence_generated' THEN
            CONTINUE;
        END IF;
        instant:=dante.occurrence_edit_coordinate_instant(
            actor,candidate.occurrence_ref,requested_zone
        );
        IF instant<=GREATEST(anchor,accepted) THEN CONTINUE; END IF;
        IF candidate.skipped OR EXISTS (
            SELECT 1 FROM dante.occurrence_profile_edit e
             WHERE e.source_native_ref=source_ref
               AND e.selected_occurrence_ref=candidate.occurrence_ref
               AND e.scope_code='only_this'
        ) OR EXISTS (
            SELECT 1 FROM dante.actual a
             WHERE a.subject_native_ref=candidate.occurrence_ref
        ) OR EXISTS (
            SELECT 1 FROM dante.routine_occurrence_activity_instance link
              JOIN dante.activity_intention activity
                ON activity.activity_ref=link.activity_ref
             WHERE link.occurrence_ref=candidate.occurrence_ref
               AND (activity.profile_revision>0 OR EXISTS (
                   SELECT 1 FROM dante.actual a
                    WHERE a.subject_native_ref=activity.activity_ref
               ))
        ) THEN
            RAISE EXCEPTION USING ERRCODE='23505',
                CONSTRAINT='occurrence_edit_future_conflict',
                MESSAGE='A following future instance has protected changes or facts';
        END IF;
        targets:=array_append(targets,candidate.occurrence_ref);
    END LOOP;
    INSERT INTO dante.occurrence_profile_edit(
        self_person_ref,operation_id,source_native_ref,selected_occurrence_ref,
        revision,expected_revision,expected_recurrence_state_ref,scope_code,
        effective_zone_id,anchor_at,accepted_at,profile_patch,
        target_occurrence_refs
    ) VALUES (
        actor,requested_operation,source_ref,selected_ref,
        current_revision+1,current_revision,current_state,requested_scope,
        requested_zone,anchor,accepted,requested_patch,targets
    );
    revision:=current_revision+1;
    source_native_ref:=source_ref;
    selected_occurrence_ref:=selected_ref;
    target_occurrence_refs:=targets;
    accepted_at:=accepted;
    replayed:=false;
    RETURN NEXT;
END;
$$;
"""

_ACTIVITY_ORIGIN = r"""
CREATE FUNCTION dante.get_self_materialized_activity_occurrence(
    actor uuid, requested_activity uuid
) RETURNS uuid
LANGUAGE sql SECURITY DEFINER STABLE PARALLEL SAFE
SET search_path=pg_catalog,dante,pg_temp AS $$
    SELECT link.occurrence_ref
      FROM dante.routine_occurrence_activity_instance link
      JOIN dante.activity_intention activity
        ON activity.activity_ref=link.activity_ref
     WHERE activity.activity_ref=requested_activity
       AND activity.self_person_ref=actor
       AND link.self_person_ref=actor
$$;
"""

_EDIT_STATE = r"""
CREATE FUNCTION dante.get_self_occurrence_edit_revision(
    actor uuid, requested_occurrence uuid
) RETURNS TABLE(
    edit_revision bigint,
    source_native_ref uuid,
    recurrence_state_ref uuid
)
LANGUAGE plpgsql SECURITY DEFINER STABLE PARALLEL RESTRICTED
SET search_path=pg_catalog,dante,pg_temp AS $$
#variable_conflict error
DECLARE bound_source uuid; current_ref uuid;
BEGIN
    SELECT item.source_native_ref INTO bound_source
      FROM dante.get_self_occurrence(actor,requested_occurrence) item;
    IF NOT FOUND THEN
        RAISE EXCEPTION USING ERRCODE='23503',
            CONSTRAINT='occurrence_edit_unavailable',
            MESSAGE='Occurrence outside self scope';
    END IF;
    IF EXISTS(SELECT 1 FROM dante.routine_intention r
               WHERE r.routine_ref=bound_source AND r.self_person_ref=actor) THEN
        SELECT r.material_state_ref INTO current_ref
          FROM dante.get_self_routine_recurrence(actor,bound_source) r;
    ELSE
        SELECT r.material_state_ref INTO current_ref
          FROM dante.get_self_event_recurrence(actor,bound_source) r;
    END IF;
    RETURN QUERY SELECT
        (SELECT COALESCE(MAX(e.revision),0)
           FROM dante.occurrence_profile_edit e
          WHERE e.source_native_ref=bound_source),
        bound_source,current_ref;
END;
$$;
"""
