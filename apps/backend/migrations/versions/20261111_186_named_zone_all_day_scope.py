"""Resolve all-day named-zone Occurrences at civil midnight for following edits.

The previous scoped-edit resolver treated an all-day calendar coordinate as
an unresolved *timed* named-zone coordinate. Preserve the strict refusal for
unresolved timed coordinates while accepting the documented all-day shape.
The already-applied migration that introduced the function stays immutable.
"""

from collections.abc import Sequence

from alembic import op

revision: str = "20261111_186"
down_revision: str | None = "20261110_185"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


_COORDINATE_INSTANT = r"""
CREATE OR REPLACE FUNCTION dante.occurrence_edit_coordinate_instant(
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
    -- Timed named-zone coordinates must be resolved by the DST-aware generator.
    -- All-day named-zone coordinates have no wall time or resolved instant by design.
    IF coord.clock_basis_code='named_zone'
       AND (coord.generated_wall_time IS NOT NULL OR coord.generated_date IS NULL) THEN
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


def upgrade() -> None:
    db = op.get_bind()
    db.exec_driver_sql(_COORDINATE_INSTANT)
    signature = "dante.occurrence_edit_coordinate_instant(uuid,uuid,text)"
    db.exec_driver_sql(f"ALTER FUNCTION {signature} OWNER TO dante_owner")
    db.exec_driver_sql(
        f"REVOKE ALL ON FUNCTION {signature} FROM PUBLIC,dante_runtime,dante_migrator"
    )
    db.exec_driver_sql(f"GRANT EXECUTE ON FUNCTION {signature} TO dante_runtime")


def downgrade() -> None:
    raise RuntimeError("20261111_186 is forward-only")
