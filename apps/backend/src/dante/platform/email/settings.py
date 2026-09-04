"""Structural configuration contract owned by the shared Email Platform runtime."""

from __future__ import annotations

from typing import Protocol

from pydantic import SecretStr


class EmailPlatformSettings(Protocol):
    """Minimum validated configuration consumed by shared email infrastructure.

    Bootstrap may compose these fields inside a broader application settings object; the
    platform depends only on this structural contract and never on Access/Auth settings.
    """

    email_transport: object
    email_worker_count: int
    email_claim_batch_size: int
    email_claim_lease_seconds: float
    email_poll_interval_seconds: float
    email_retry_base_seconds: float
    email_retry_max_seconds: float
    email_attempt_limit: int
    email_provider_connect_timeout_seconds: float
    email_provider_read_timeout_seconds: float
    email_payload_current_key_id: str | None
    ses_region: str | None
    ses_configuration_set: str | None

    smtp_host: str
    smtp_port: int
    smtp_security: object
    smtp_username: str | None
    smtp_password: SecretStr | None

    @property
    def email_payload_key_bytes(self) -> dict[str, bytes]: ...

    @property
    def email_sender_address(self) -> str: ...
