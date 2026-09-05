"""Compatibility imports for Email Platform contracts now owned by `dante.platform.email`."""

from dante.platform.email.contracts import (
    ClaimedEmailIntent,
    EmailIntentConflictError,
    EmailIntentSpec,
    EmailPayloadError,
    EmailProviderPort,
    EncryptedEmailPayload,
    ProviderMessage,
    ProviderOutcome,
    ProviderSendResult,
)

__all__ = [
    "ClaimedEmailIntent",
    "EmailIntentConflictError",
    "EmailIntentSpec",
    "EmailPayloadError",
    "EmailProviderPort",
    "EncryptedEmailPayload",
    "ProviderMessage",
    "ProviderOutcome",
    "ProviderSendResult",
]
