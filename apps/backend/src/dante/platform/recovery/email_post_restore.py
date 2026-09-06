"""Fail-closed Email Platform reconciliation before application reopen.

This operator is intentionally provider-free.  It connects only as the bounded
``dante_runtime`` role, quarantines restored sendable EmailIntent work, verifies
the resulting database state in the same transaction, and exits non-zero on any
unsafe remainder.  Email workers must remain stopped while it runs.
"""

from __future__ import annotations

import asyncio
import json
import os
import sys
from dataclasses import asdict, dataclass

from pydantic import SecretStr
from sqlalchemy import func, or_, select

from dante.platform.config.database import DatabaseSettings
from dante.platform.database.mappings.email_delivery import (
    EmailDeliveryAttemptRow,
    EmailDeliveryIntentRow,
)
from dante.platform.database.runtime import DatabaseRuntime, create_database_runtime
from dante.platform.email.recovery import quarantine_restored_email_delivery

_RESTORED_SENDABLE_STATES = ("pending", "claimed", "retryable_failure")


class EmailPostRestoreReconciliationError(RuntimeError):
    """Raised when restored Email Platform state is not safe to reopen."""


@dataclass(frozen=True, slots=True)
class EmailPostRestoreReconciliationResult:
    """Verified result of one isolated post-restore reconciliation."""

    quarantined_intent_count: int
    ambiguous_attempt_count: int
    remaining_sendable_intent_count: int
    unsafe_quarantined_intent_count: int
    in_progress_quarantined_attempt_count: int


async def reconcile_restored_email_delivery(
    database_runtime: DatabaseRuntime,
) -> EmailPostRestoreReconciliationResult:
    """Quarantine + verify restored Email work before workers may resume."""

    async with database_runtime.session_factory() as session, session.begin():
        transition = await quarantine_restored_email_delivery(session)

        remaining_sendable = int(
            await session.scalar(
                select(func.count())
                .select_from(EmailDeliveryIntentRow)
                .where(EmailDeliveryIntentRow.dispatch_state_code.in_(_RESTORED_SENDABLE_STATES))
            )
            or 0
        )
        unsafe_quarantined = int(
            await session.scalar(
                select(func.count())
                .select_from(EmailDeliveryIntentRow)
                .where(
                    EmailDeliveryIntentRow.dispatch_state_code == "recovery_quarantined",
                    or_(
                        EmailDeliveryIntentRow.claim_token.is_not(None),
                        EmailDeliveryIntentRow.claimed_until.is_not(None),
                        EmailDeliveryIntentRow.next_attempt_at.is_not(None),
                        EmailDeliveryIntentRow.sensitive_key_id.is_not(None),
                        EmailDeliveryIntentRow.sensitive_nonce.is_not(None),
                        EmailDeliveryIntentRow.sensitive_ciphertext.is_not(None),
                        EmailDeliveryIntentRow.sensitive_wiped_at.is_(None),
                        EmailDeliveryIntentRow.terminal_at.is_(None),
                    ),
                )
            )
            or 0
        )
        in_progress_quarantined_attempts = int(
            await session.scalar(
                select(func.count())
                .select_from(EmailDeliveryAttemptRow)
                .join(
                    EmailDeliveryIntentRow,
                    EmailDeliveryIntentRow.email_intent_ref
                    == EmailDeliveryAttemptRow.email_intent_ref,
                )
                .where(
                    EmailDeliveryIntentRow.dispatch_state_code == "recovery_quarantined",
                    EmailDeliveryAttemptRow.result_code == "in_progress",
                )
            )
            or 0
        )

        result = EmailPostRestoreReconciliationResult(
            quarantined_intent_count=transition.quarantined_intent_count,
            ambiguous_attempt_count=transition.ambiguous_attempt_count,
            remaining_sendable_intent_count=remaining_sendable,
            unsafe_quarantined_intent_count=unsafe_quarantined,
            in_progress_quarantined_attempt_count=in_progress_quarantined_attempts,
        )

        if remaining_sendable:
            raise EmailPostRestoreReconciliationError(
                f"{remaining_sendable} restored EmailIntent rows remain sendable"
            )
        if unsafe_quarantined:
            raise EmailPostRestoreReconciliationError(
                f"{unsafe_quarantined} quarantined EmailIntent rows retain unsafe state"
            )
        if in_progress_quarantined_attempts:
            raise EmailPostRestoreReconciliationError(
                f"{in_progress_quarantined_attempts} quarantined Email attempts remain in_progress"
            )

        return result


def _runtime_settings_from_environment() -> DatabaseSettings:
    """Load only the bounded database identity needed by the recovery operator."""

    try:
        host = os.environ["DANTE_DATABASE__HOST"]
        name = os.environ["DANTE_DATABASE__NAME"]
        password = os.environ["DANTE_RUNTIME__PASSWORD"]
    except KeyError as exc:
        raise EmailPostRestoreReconciliationError(
            f"missing required recovery environment variable: {exc.args[0]}"
        ) from exc

    try:
        port = int(os.environ.get("DANTE_DATABASE__PORT", "5432"))
    except ValueError as exc:
        raise EmailPostRestoreReconciliationError(
            "DANTE_DATABASE__PORT must be an integer"
        ) from exc

    return DatabaseSettings(
        host=host,
        port=port,
        name=name,
        user="dante_runtime",
        password=SecretStr(password),
        pool_size=1,
        max_overflow=0,
        pool_timeout_seconds=10,
        readiness_timeout_seconds=2,
    )


async def _run_operator() -> EmailPostRestoreReconciliationResult:
    runtime = create_database_runtime(_runtime_settings_from_environment())
    try:
        if not await runtime.is_ready():
            raise EmailPostRestoreReconciliationError(
                "restored database is not ready as exact dante_runtime identity"
            )
        return await reconcile_restored_email_delivery(runtime)
    finally:
        await runtime.dispose()


def main() -> None:
    """CLI entry point used by the recovery runbook/CP08 harness."""

    result = asyncio.run(_run_operator())
    sys.stdout.write(json.dumps(asdict(result), sort_keys=True) + "\n")


if __name__ == "__main__":
    main()


__all__ = [
    "EmailPostRestoreReconciliationError",
    "EmailPostRestoreReconciliationResult",
    "reconcile_restored_email_delivery",
]
