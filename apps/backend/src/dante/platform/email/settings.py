"""Structural configuration contract owned by the shared Email Platform runtime."""

from __future__ import annotations

from typing import Protocol

from pydantic import SecretStr


class EmailPlatformSettings(Protocol):
    """Read-only validated configuration consumed by shared email infrastructure.

    Bootstrap may compose these fields inside a broader application settings object; the
    platform depends only on this structural contract and never on Access/Auth settings.
    Read-only properties keep concrete enum/value types covariant at the consumer boundary.
    """

    @property
    def email_transport(self) -> object: ...

    @property
    def email_worker_count(self) -> int: ...

    @property
    def email_claim_batch_size(self) -> int: ...

    @property
    def email_claim_lease_seconds(self) -> float: ...

    @property
    def email_poll_interval_seconds(self) -> float: ...

    @property
    def email_retry_base_seconds(self) -> float: ...

    @property
    def email_retry_max_seconds(self) -> float: ...

    @property
    def email_attempt_limit(self) -> int: ...

    @property
    def email_provider_connect_timeout_seconds(self) -> float: ...

    @property
    def email_provider_read_timeout_seconds(self) -> float: ...

    @property
    def email_payload_current_key_id(self) -> str | None: ...

    @property
    def ses_region(self) -> str | None: ...

    @property
    def ses_configuration_set(self) -> str | None: ...

    @property
    def smtp_host(self) -> str: ...

    @property
    def smtp_port(self) -> int: ...

    @property
    def smtp_security(self) -> object: ...

    @property
    def smtp_username(self) -> str | None: ...

    @property
    def smtp_password(self) -> SecretStr | None: ...

    @property
    def email_payload_key_bytes(self) -> dict[str, bytes]: ...

    @property
    def email_sender_address(self) -> str: ...
