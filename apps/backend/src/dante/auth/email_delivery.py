"""Typed application boundary for Auth/security email commands."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol, override
from uuid import UUID

from pydantic import SecretStr


class EmailDispatchCapacityError(RuntimeError):
    """Canonical durable delivery is unavailable for a deliverable email command."""


@dataclass(frozen=True, slots=True)
class SignupVerificationEmail:
    """Out-of-band six-digit password-signup verification message."""

    to_address: str
    code: SecretStr
    expires_minutes: int


@dataclass(frozen=True, slots=True)
class ProviderEnrollmentVerificationEmail:
    """Out-of-band six-digit provider-enrollment mailbox verification message."""

    to_address: str
    code: SecretStr
    expires_minutes: int


@dataclass(frozen=True, slots=True)
class PasswordRecoveryEmail:
    """Out-of-band high-entropy password-recovery bearer message."""

    to_address: str
    password_recovery_ref: UUID
    secret: SecretStr


@dataclass(frozen=True, slots=True)
class PasswordResetNotificationEmail:
    """Security notification emitted after a durable recovery reset."""

    to_address: str


@dataclass(frozen=True, slots=True)
class NoopEmail:
    """Equivalent neutral work for deliberately undisclosed recovery paths."""

    reason: str = "neutral_recovery"


type DeliverableEmail = (
    SignupVerificationEmail
    | ProviderEnrollmentVerificationEmail
    | PasswordRecoveryEmail
    | PasswordResetNotificationEmail
)
type EmailCommand = DeliverableEmail | NoopEmail


class EmailDeliveryPort(Protocol):
    """Application-facing boundary; enqueue never performs provider network I/O."""

    async def enqueue(self, command: EmailCommand) -> None:
        """Admit one command or fail immediately when durable delivery is unavailable."""
        ...


class UnavailableEmailDelivery(EmailDeliveryPort):
    """Fail-closed fallback used only when the durable Email Platform is disabled."""

    @override
    async def enqueue(self, command: EmailCommand) -> None:
        if isinstance(command, NoopEmail):
            return
        raise EmailDispatchCapacityError("durable email platform is unavailable")
