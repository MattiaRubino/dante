"""Server-side resolution for raw provider continuation capabilities."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from dante.auth.contracts import (
    AuthIntegrityError,
    AuthServiceUnavailableError,
    ProviderEnrollmentInvalidOrExpiredError,
    ProviderLinkInvalidOrExpiredError,
)
from dante.auth.proofs import FlowProofPurpose, flow_proof_verifier
from dante.platform.database.mappings.auth import ExternalLinkChallengeRow, ExternalSignupChallengeRow

_ALLOWED_PROVIDER_CODES = frozenset({"google", "apple"})


@dataclass(frozen=True, slots=True)
class ProviderEnrollmentContinuation:
    """Safe server-side metadata resolved from one enrollment capability."""

    external_signup_ref: UUID
    provider_code: str
    expires_at: datetime


@dataclass(frozen=True, slots=True)
class ProviderLinkContinuation:
    """Safe server-side metadata resolved from one provider-link capability."""

    external_link_challenge_ref: UUID
    provider_code: str
    expires_at: datetime


class ProviderContinuationService:
    """Resolve opaque flow cookies without exposing refs or provider metadata in cookies."""

    def __init__(self, *, session_factory: async_sessionmaker[AsyncSession]) -> None:
        self._session_factory = session_factory

    async def resolve_enrollment(self, continuation_secret: str) -> ProviderEnrollmentContinuation:
        verifier = flow_proof_verifier(
            purpose=FlowProofPurpose.PROVIDER_ENROLLMENT,
            encoded_secret=continuation_secret,
        )
        if verifier is None:
            raise ProviderEnrollmentInvalidOrExpiredError()
        now = datetime.now(UTC)
        try:
            async with self._session_factory() as database_session, database_session.begin():
                row = await database_session.scalar(
                    select(ExternalSignupChallengeRow).where(
                        ExternalSignupChallengeRow.continuation_verifier == verifier,
                        ExternalSignupChallengeRow.expires_at > now,
                    )
                )
        except SQLAlchemyError as exc:
            raise AuthServiceUnavailableError(retryable=True) from exc
        if row is None:
            raise ProviderEnrollmentInvalidOrExpiredError()
        if row.provider_code not in _ALLOWED_PROVIDER_CODES:
            raise AuthIntegrityError("provider enrollment owns unknown provider vocabulary")
        return ProviderEnrollmentContinuation(
            external_signup_ref=row.external_signup_ref,
            provider_code=row.provider_code,
            expires_at=row.expires_at,
        )

    async def resolve_link(self, continuation_secret: str) -> ProviderLinkContinuation:
        verifier = flow_proof_verifier(
            purpose=FlowProofPurpose.PROVIDER_LINK,
            encoded_secret=continuation_secret,
        )
        if verifier is None:
            raise ProviderLinkInvalidOrExpiredError()
        now = datetime.now(UTC)
        try:
            async with self._session_factory() as database_session, database_session.begin():
                row = await database_session.scalar(
                    select(ExternalLinkChallengeRow).where(
                        ExternalLinkChallengeRow.continuation_verifier == verifier,
                        ExternalLinkChallengeRow.expires_at > now,
                    )
                )
        except SQLAlchemyError as exc:
            raise AuthServiceUnavailableError(retryable=True) from exc
        if row is None:
            raise ProviderLinkInvalidOrExpiredError()
        if row.provider_code not in _ALLOWED_PROVIDER_CODES:
            raise AuthIntegrityError("provider link owns unknown provider vocabulary")
        return ProviderLinkContinuation(
            external_link_challenge_ref=row.external_link_challenge_ref,
            provider_code=row.provider_code,
            expires_at=row.expires_at,
        )
