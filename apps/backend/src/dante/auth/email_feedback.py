"""Access/Auth projection adapter for shared Email Platform provider feedback."""

from __future__ import annotations

from datetime import datetime

from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

from dante.platform.database.mappings.auth import EmailIdentityRow
from dante.platform.email.feedback import (
    EmailFeedbackStore as SharedEmailFeedbackStore,
)
from dante.platform.email.feedback import (
    NormalizedSesFeedback,
    SesFeedbackError,
    normalize_ses_feedback,
)


class AuthEmailSuppressionProjection:
    """Project strong delivery suppression into Auth-owned recovery eligibility state."""

    async def apply(
        self,
        database_session: AsyncSession,
        *,
        recipient_comparison_key: str,
        observed_at: datetime,
    ) -> None:
        """Restrict recovery delivery without redefining canonical email verification truth."""
        await database_session.execute(
            update(EmailIdentityRow)
            .where(EmailIdentityRow.comparison_key == recipient_comparison_key)
            .values(
                recovery_restriction_code="provider_delivery_disabled",
                recovery_restriction_observed_at=observed_at,
            )
        )


class EmailFeedbackStore(SharedEmailFeedbackStore):
    """Compatibility store preserving the historical Auth projection behavior."""

    def __init__(self) -> None:
        super().__init__(suppression_projection=AuthEmailSuppressionProjection())


__all__ = [
    "AuthEmailSuppressionProjection",
    "EmailFeedbackStore",
    "NormalizedSesFeedback",
    "SesFeedbackError",
    "normalize_ses_feedback",
]
