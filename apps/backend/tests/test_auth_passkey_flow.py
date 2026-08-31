"""Focused pure/application proof for M5-F passkey lifecycle rules."""

from base64 import urlsafe_b64encode
from datetime import UTC, datetime
from typing import Any, cast
from uuid import uuid7

import pytest
from pydantic import SecretStr, ValidationError
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from dante.auth.contracts import AuthInputError, PasskeyVerificationFailedError
from dante.auth.lifecycle_runtime import AuthLifecycleRuntime
from dante.auth.passkey_flow import PasskeyFlowService
from dante.auth.proofs import FlowProofPurpose, flow_proof_verifier_from_raw
from dante.auth.provider_flow_runtime import create_provider_flow_runtime
from dante.auth.service import AuthRuntime
from dante.auth.webauthn import WebAuthnAssertionEvidence, WebAuthnPolicy
from dante.platform.config.auth import AuthSettings
from dante.platform.config.auth_provider import AuthProviderSettings, WebAuthnSettings
from dante.platform.database.mappings.auth import PasskeyCredentialRow
from dante.platform.database.runtime import DatabaseRuntime

_KEY_ID = "test-passkey-runtime-v1"


def _encoded(raw: bytes) -> str:
    return urlsafe_b64encode(raw).rstrip(b"=").decode("ascii")


def _credential(*, sign_count: int = 8, backup_eligible: bool = True) -> PasskeyCredentialRow:
    now = datetime.now(UTC)
    return PasskeyCredentialRow(
        passkey_credential_ref=uuid7(),
        account_ref=uuid7(),
        credential_id=b"credential-id",
        credential_public_key=b"cose-key",
        cose_algorithm=-7,
        sign_count=sign_count,
        backup_eligible=backup_eligible,
        backup_state=False,
        transports=[],
        label="Laptop",
        status_code="active",
        created_at=now,
        updated_at=now,
        last_used_at=None,
        revoked_at=None,
        revocation_reason_code=None,
    )


def _assertion(*, sign_count: int, backup_eligible: bool = True) -> WebAuthnAssertionEvidence:
    return WebAuthnAssertionEvidence(
        credential_id=b"credential-id",
        user_handle=b"u" * 32,
        sign_count=sign_count,
        backup_eligible=backup_eligible,
        backup_state=True,
        challenge=b"a" * 32,
        origin="https://dante.test",
    )


def _runtime_settings(*, webauthn_enabled: bool) -> AuthSettings:
    return AuthSettings(
        canonical_web_origin="https://dante.test",
        password_current_pepper_key_id=_KEY_ID,
        password_peppers={_KEY_ID: SecretStr(_encoded(b"p" * 32))},
        csrf_key=SecretStr(_encoded(b"c" * 32)),
        signup_otp_current_key_id=_KEY_ID,
        signup_otp_keys={_KEY_ID: SecretStr(_encoded(b"o" * 32))},
        smtp_host="127.0.0.1",
        smtp_port=9,
        smtp_from_address="no-reply@dante.test",
        kdf_max_concurrency=1,
        signin_rate_capacity=10,
        signin_rate_window_seconds=60,
        provider=AuthProviderSettings(
            webauthn=WebAuthnSettings(
                enabled=webauthn_enabled,
                rp_id="dante.test",
                expected_origins=("https://dante.test",),
            )
        ),
    )


class _NoDatabase:
    def __call__(self) -> AsyncSession:
        raise AssertionError("runtime composition must remain lazy over PostgreSQL")


class _DisabledAuthRuntime:
    provider_runtime: Any = None
    apple_grant_cipher: Any = None

    @property
    def webauthn_policy(self) -> WebAuthnPolicy | None:
        raise AssertionError("disabled WebAuthn must not read the policy")


class _EnabledAuthRuntime:
    provider_runtime: Any = None
    apple_grant_cipher: Any = None

    def __init__(self, policy: WebAuthnPolicy) -> None:
        self.webauthn_policy = policy


def _database_runtime() -> DatabaseRuntime:
    runtime = type("NoDatabaseRuntime", (), {})()
    runtime.session_factory = cast(async_sessionmaker[AsyncSession], _NoDatabase())
    return cast(DatabaseRuntime, runtime)


def test_webauthn_challenge_lifetime_is_capped_at_five_minutes() -> None:
    with pytest.raises(ValidationError, match="five minutes"):
        WebAuthnSettings(challenge_lifetime_seconds=301)


def test_webauthn_rp_and_origins_are_https_and_same_rp_family() -> None:
    settings = WebAuthnSettings(
        rp_id="DANTE.TEST",
        expected_origins=("https://dante.test", "https://app.dante.test"),
    )
    assert settings.rp_id == "dante.test"

    with pytest.raises(ValidationError, match="HTTPS"):
        WebAuthnSettings(
            rp_id="dante.test",
            expected_origins=("http://dante.test",),
        )
    with pytest.raises(ValidationError, match="subdomain|RP ID"):
        WebAuthnSettings(
            rp_id="dante.test",
            expected_origins=("https://evil.test",),
        )
    with pytest.raises(ValidationError, match="IP address"):
        WebAuthnSettings(
            rp_id="127.0.0.1",
            expected_origins=("https://127.0.0.1",),
        )


def test_webauthn_origins_are_serialized_like_browser_origins_before_exact_matching() -> None:
    settings = WebAuthnSettings(
        rp_id="DANTE.TEST",
        expected_origins=("HTTPS://DANTE.TEST:443/", "https://APP.DANTE.TEST:8443"),
    )
    assert settings.expected_origins == (
        "https://dante.test",
        "https://app.dante.test:8443",
    )

    with pytest.raises(ValidationError, match="unique"):
        WebAuthnSettings(
            rp_id="dante.test",
            expected_origins=("https://dante.test", "HTTPS://DANTE.TEST:443/"),
        )


def test_passkey_runtime_is_absent_without_touching_policy_when_webauthn_is_disabled() -> None:
    runtime = create_provider_flow_runtime(
        settings=_runtime_settings(webauthn_enabled=False),
        database_runtime=_database_runtime(),
        auth_runtime=cast(AuthRuntime, _DisabledAuthRuntime()),
        lifecycle_runtime=cast(AuthLifecycleRuntime, object()),
    )

    assert runtime.passkey_service is None
    assert runtime.service is None
    assert runtime.apple_service is None


def test_passkey_runtime_reuses_the_single_process_policy_when_webauthn_is_enabled() -> None:
    settings = _runtime_settings(webauthn_enabled=True)
    policy = WebAuthnPolicy.from_settings(settings.provider.webauthn)
    runtime = create_provider_flow_runtime(
        settings=settings,
        database_runtime=_database_runtime(),
        auth_runtime=cast(AuthRuntime, _EnabledAuthRuntime(policy)),
        lifecycle_runtime=cast(AuthLifecycleRuntime, object()),
    )

    assert runtime.passkey_service is not None
    assert runtime.passkey_service._policy is policy
    assert runtime.service is None
    assert runtime.apple_service is None


def test_passkey_label_and_transport_hints_are_bounded_without_freezing_vocabulary() -> None:
    assert PasskeyFlowService._normalize_label("My security key") == "My security key"
    assert PasskeyFlowService._normalize_transports(("usb", "hybrid", "future-transport")) == (
        "usb",
        "hybrid",
        "future-transport",
    )
    assert PasskeyFlowService._normalize_transports(("usb", "usb")) == ("usb",)

    with pytest.raises(AuthInputError):
        PasskeyFlowService._normalize_label(" passkey ")
    with pytest.raises(AuthInputError):
        PasskeyFlowService._normalize_transports(tuple(str(index) for index in range(9)))


def test_raw_webauthn_challenge_verifier_is_exact_width_and_purpose_separated() -> None:
    challenge = b"x" * 32
    webauthn = flow_proof_verifier_from_raw(
        purpose=FlowProofPurpose.WEBAUTHN_CHALLENGE,
        raw_secret=challenge,
    )
    provider = flow_proof_verifier_from_raw(
        purpose=FlowProofPurpose.PROVIDER_STATE,
        raw_secret=challenge,
    )

    assert webauthn is not None
    assert provider is not None
    assert webauthn != provider
    assert flow_proof_verifier_from_raw(
        purpose=FlowProofPurpose.WEBAUTHN_CHALLENGE,
        raw_secret=b"x" * 31,
    ) is None


def test_verified_assertion_never_decreases_counter_and_updates_current_backup_state() -> None:
    credential = _credential(sign_count=8)
    mutation_at = datetime.now(UTC)

    PasskeyFlowService._apply_assertion_state(
        credential,
        evidence=_assertion(sign_count=3),
        mutation_at=mutation_at,
    )

    assert credential.sign_count == 8
    assert credential.backup_state is True
    assert credential.last_used_at == mutation_at
    assert credential.updated_at == mutation_at


def test_assertion_cannot_change_immutable_backup_eligibility() -> None:
    credential = _credential(backup_eligible=False)

    with pytest.raises(PasskeyVerificationFailedError):
        PasskeyFlowService._apply_assertion_state(
            credential,
            evidence=_assertion(sign_count=9, backup_eligible=True),
            mutation_at=datetime.now(UTC),
        )
