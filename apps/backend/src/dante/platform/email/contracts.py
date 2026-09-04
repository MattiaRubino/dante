"""Provider-neutral contracts for the shared DANTE Email Platform."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum
from typing import Protocol
from uuid import UUID


class EmailIntentConflictError(RuntimeError):
    """One idempotency identity was reused for different immutable email work."""


class EmailPayloadError(RuntimeError):
    """Protected email payload cannot be decoded or authenticated safely."""


class ProviderOutcome(StrEnum):
    """Provider result classification with uncertainty preserved explicitly."""

    ACCEPTED = "provider_accepted"
    RETRYABLE_FAILURE = "retryable_failure"
    AMBIGUOUS = "ambiguous"
    DEFINITIVE_FAILURE = "definitive_failure"


@dataclass(frozen=True, slots=True)
class ProviderSendResult:
    """Provider-neutral result of exactly one deliberate wire attempt."""

    outcome: ProviderOutcome
    provider_message_id: str | None = None
    safe_error_code: str | None = None


@dataclass(frozen=True, slots=True)
class ProviderMessage:
    """Rendered last-mile provider input with privacy-minimized correlation."""

    email_intent_ref: UUID
    from_address: str
    to_address: str
    subject: str
    text_body: str
    html_body: str | None
    stream_code: str


class EmailProviderPort(Protocol):
    """Last-mile provider boundary; one call means one wire attempt."""

    provider_code: str

    async def send(self, message: ProviderMessage) -> ProviderSendResult:
        """Attempt one provider send without hidden retry."""
        ...


@dataclass(frozen=True, slots=True)
class ClaimedEmailIntent:
    """One exact PostgreSQL claim owned by a bounded worker lease."""

    email_intent_ref: UUID
    email_attempt_ref: UUID
    claim_token: UUID
    purpose_code: str
    stream_code: str
    template_code: str
    template_revision: str
    locale_code: str
    recipient_address: str
    recipient_comparison_key: str
    sensitive_key_id: str | None
    sensitive_nonce: bytes | None
    sensitive_ciphertext: bytes | None
    attempt_number: int
    expires_at: datetime


@dataclass(frozen=True, slots=True)
class EmailIntentSpec:
    """Consumer-owned immutable content semantics admitted by the shared outbox."""

    purpose_code: str
    template_code: str
    payload: dict[str, str | int]
    recipient_address: str
    recipient_comparison_key: str


@dataclass(frozen=True, slots=True)
class EncryptedEmailPayload:
    """Short-lived encrypted delivery material bound to one intent."""

    key_id: str
    nonce: bytes
    ciphertext: bytes
    fingerprint: bytes
