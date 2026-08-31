"""Real PostgreSQL + real fido2 proof for M5-F passkey lifecycle."""

from __future__ import annotations

import asyncio
from base64 import urlsafe_b64encode
from collections.abc import AsyncIterator, Mapping
from contextlib import asynccontextmanager
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from typing import Any, cast
from uuid import UUID, uuid7

import psycopg
import pytest
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec
from fido2.cose import ES256
from fido2.utils import sha256, websafe_decode, websafe_encode
from fido2.webauthn import (
    Aaguid,
    AttestationObject,
    AttestedCredentialData,
    AuthenticatorData,
    CollectedClientData,
)
from pydantic import SecretStr
from sqlalchemy import func, select
from sqlalchemy.exc import DBAPIError
from sqlalchemy.ext.asyncio import AsyncSession

from dante.auth.authenticator_lifecycle import (
    AuthenticatorLifecycleService,
    MultiAuthenticatorLifecycleService,
)
from dante.auth.contracts import (
    AccountUnavailableError,
    AdmittedSession,
    AuthenticatorRemovalBlockedError,
    AuthIntegrityError,
    AuthServiceUnavailableError,
    AuthStateChangedError,
    IssuedSession,
    PasskeyAlreadyRegisteredError,
    PasskeyChallengeInvalidOrExpiredError,
    PasskeyVerificationFailedError,
    Principal,
)
from dante.auth.lifecycle import KeyedRateLimiter, LifecycleLimiters
from dante.auth.passkey_flow import PasskeyFlowLimiters, PasskeyFlowService
from dante.auth.proofs import SignupOtpCodec
from dante.auth.sessions import generate_session_secret, session_secret_verifier
from dante.auth.webauthn import WebAuthnAssertionEvidence, WebAuthnPolicy
from dante.platform.config.auth import AuthSettings, SmtpSecurity
from dante.platform.config.auth_provider import (
    GOOGLE_ISSUER,
    AuthProviderSettings,
    WebAuthnSettings,
)
from dante.platform.database.mappings.auth import (
    AccountRow,
    AuthSessionRow,
    EmailIdentityRow,
    ExternalIdentityRow,
    PasskeyCredentialRow,
    PasswordCredentialRow,
    WebAuthnAccountRow,
    WebAuthnChallengeRow,
)
from dante.platform.database.runtime import DatabaseRuntime, create_database_runtime

pytestmark = pytest.mark.postgres

_KEY_ID = "test-passkey-v1"
_RP_ID = "dante.test"
_ORIGIN = "https://dante.test"


def _encoded(raw: bytes) -> str:
    return urlsafe_b64encode(raw).rstrip(b"=").decode("ascii")


def _settings() -> AuthSettings:
    return AuthSettings(
        canonical_web_origin=_ORIGIN,
        password_current_pepper_key_id=_KEY_ID,
        password_peppers={_KEY_ID: SecretStr(_encoded(b"p" * 32))},
        csrf_key=SecretStr(_encoded(b"c" * 32)),
        signup_otp_current_key_id=_KEY_ID,
        signup_otp_keys={_KEY_ID: SecretStr(_encoded(b"o" * 32))},
        smtp_host="127.0.0.1",
        smtp_port=9,
        smtp_security=SmtpSecurity.PLAIN,
        smtp_from_address="no-reply@dante.test",
        kdf_max_concurrency=1,
        signin_rate_capacity=100,
        signin_rate_window_seconds=60,
        provider=AuthProviderSettings(
            webauthn=WebAuthnSettings(
                enabled=True,
                rp_id=_RP_ID,
                rp_name="DANTE",
                expected_origins=(_ORIGIN,),
                challenge_lifetime_seconds=300,
                begin_rate_capacity=100,
                begin_rate_window_seconds=60,
                complete_rate_capacity=100,
                complete_rate_window_seconds=60,
                rate_max_keys=256,
            )
        ),
    )


@asynccontextmanager
async def _service(database: Any) -> AsyncIterator[tuple[PasskeyFlowService, DatabaseRuntime]]:
    settings = _settings()
    runtime = create_database_runtime(database.runtime_settings())
    webauthn = settings.provider.webauthn
    service = PasskeyFlowService(
        session_factory=runtime.session_factory,
        settings=settings,
        policy=WebAuthnPolicy.from_settings(webauthn),
        limiters=PasskeyFlowLimiters(
            begin=KeyedRateLimiter(capacity=100, window_seconds=60, max_keys=256),
            complete=KeyedRateLimiter(capacity=100, window_seconds=60, max_keys=256),
        ),
    )
    try:
        yield service, runtime
    finally:
        await runtime.dispose()


@dataclass(frozen=True, slots=True)
class _SessionSeed:
    admitted: AdmittedSession
    secret: SecretStr


@dataclass(frozen=True, slots=True)
class _RegisteredPasskey:
    passkey_credential_ref: UUID
    credential_id: bytes
    user_handle: bytes
    private_key: ec.EllipticCurvePrivateKey
    issued: IssuedSession


async def _seed_account(
    runtime: DatabaseRuntime,
    *,
    email: str,
    password_present: bool,
    session_count: int = 1,
) -> tuple[UUID, UUID, list[_SessionSeed]]:
    account_ref = uuid7()
    email_ref = uuid7()
    now = datetime.now(UTC)
    expires_at = now + timedelta(hours=2)
    sessions: list[_SessionSeed] = []
    rows: list[Any] = [
        AccountRow(
            account_ref=account_ref,
            status_code="active",
            created_at=now,
            disabled_at=None,
        ),
        EmailIdentityRow(
            email_identity_ref=email_ref,
            account_ref=account_ref,
            address=email,
            comparison_key=email.casefold(),
            created_at=now,
            verified_at=now,
            recovery_restriction_code=None,
            recovery_restriction_observed_at=None,
        ),
    ]
    for _ in range(session_count):
        secret = generate_session_secret()
        session_ref = uuid7()
        rows.append(
            AuthSessionRow(
                auth_session_ref=session_ref,
                account_ref=account_ref,
                secret_verifier=session_secret_verifier(secret),
                created_at=now,
                authenticated_at=now,
                recent_auth_at=now,
                last_user_activity_at=now,
                expires_at=expires_at,
                revoked_at=None,
                revocation_reason_code=None,
            )
        )
        sessions.append(
            _SessionSeed(
                admitted=AdmittedSession(
                    principal=Principal(
                        account_ref=account_ref,
                        auth_session_ref=session_ref,
                        authenticated_at=now,
                        recent_auth_at=now,
                    ),
                    expires_at=expires_at,
                    csrf_token=SecretStr("synthetic-csrf"),
                ),
                secret=secret,
            )
        )
    if password_present:
        rows.append(
            PasswordCredentialRow(
                password_credential_ref=uuid7(),
                account_ref=account_ref,
                verifier="$argon2id$v=19$synthetic",
                pepper_key_id=_KEY_ID,
                created_at=now,
                updated_at=now,
            )
        )
    async with runtime.session_factory() as session, session.begin():
        session.add_all(rows)
    return account_ref, email_ref, sessions


async def _seed_provider(
    runtime: DatabaseRuntime,
    *,
    account_ref: UUID,
    email_ref: UUID,
    subject: str,
) -> UUID:
    external_identity_ref = uuid7()
    now = datetime.now(UTC)
    async with runtime.session_factory() as session, session.begin():
        session.add(
            ExternalIdentityRow(
                external_identity_ref=external_identity_ref,
                account_ref=account_ref,
                email_identity_ref=email_ref,
                provider_code="google",
                issuer=GOOGLE_ISSUER,
                subject=subject,
                provider_email_address=f"{subject}@example.com",
                provider_email_private=False,
                status_code="active",
                created_at=now,
                status_changed_at=now,
                last_authenticated_at=now,
                revoked_at=None,
                revocation_reason_code=None,
            )
        )
    return external_identity_ref


def _public_key_options(options: Mapping[str, Any]) -> Mapping[str, Any]:
    public_key = options.get("publicKey")
    assert isinstance(public_key, Mapping)
    return cast(Mapping[str, Any], public_key)


def _registration_values(options: Mapping[str, Any]) -> tuple[bytes, bytes]:
    public_key = _public_key_options(options)
    challenge = public_key.get("challenge")
    user = public_key.get("user")
    assert isinstance(challenge, str)
    assert isinstance(user, Mapping)
    user_id = user.get("id")
    assert isinstance(user_id, str)
    return websafe_decode(challenge), websafe_decode(user_id)


def _authentication_challenge(options: Mapping[str, Any]) -> bytes:
    public_key = _public_key_options(options)
    challenge = public_key.get("challenge")
    assert isinstance(challenge, str)
    return websafe_decode(challenge)


def _registration_response(
    *,
    challenge: bytes,
    credential_id: bytes,
    public_key: ES256,
) -> dict[str, object]:
    credential = AttestedCredentialData.create(Aaguid.NONE, credential_id, public_key)
    auth_data = AuthenticatorData.create(
        sha256(_RP_ID.encode("ascii")),
        AuthenticatorData.FLAG.UP
        | AuthenticatorData.FLAG.UV
        | AuthenticatorData.FLAG.AT
        | AuthenticatorData.FLAG.BE,
        0,
        credential,
    )
    attestation = AttestationObject.create("none", auth_data, {})
    client_data = CollectedClientData.create(
        CollectedClientData.TYPE.CREATE,
        challenge,
        _ORIGIN,
    )
    encoded_id = websafe_encode(credential_id)
    return {
        "id": encoded_id,
        "rawId": encoded_id,
        "type": "public-key",
        "response": {
            "clientDataJSON": client_data.b64,
            "attestationObject": websafe_encode(attestation),
        },
    }


def _authentication_response(
    *,
    challenge: bytes,
    credential_id: bytes,
    user_handle: bytes | None,
    private_key: ec.EllipticCurvePrivateKey,
    counter: int,
    backed_up: bool,
) -> dict[str, object]:
    flags = AuthenticatorData.FLAG.UP | AuthenticatorData.FLAG.UV | AuthenticatorData.FLAG.BE
    if backed_up:
        flags |= AuthenticatorData.FLAG.BS
    auth_data = AuthenticatorData.create(
        sha256(_RP_ID.encode("ascii")),
        flags,
        counter,
    )
    client_data = CollectedClientData.create(
        CollectedClientData.TYPE.GET,
        challenge,
        _ORIGIN,
    )
    signature = private_key.sign(
        auth_data + client_data.hash,
        ec.ECDSA(hashes.SHA256()),
    )
    encoded_id = websafe_encode(credential_id)
    response: dict[str, object] = {
        "clientDataJSON": client_data.b64,
        "authenticatorData": websafe_encode(auth_data),
        "signature": websafe_encode(signature),
    }
    if user_handle is not None:
        response["userHandle"] = websafe_encode(user_handle)
    return {
        "id": encoded_id,
        "rawId": encoded_id,
        "type": "public-key",
        "response": response,
    }


def _admitted(issued: IssuedSession) -> AdmittedSession:
    return AdmittedSession(
        principal=issued.principal,
        expires_at=issued.expires_at,
        csrf_token=issued.csrf_token,
    )


async def _active_passkeys(runtime: DatabaseRuntime, account_ref: UUID) -> list[PasskeyCredentialRow]:
    async with runtime.session_factory() as session, session.begin():
        return list(
            (
                await session.scalars(
                    select(PasskeyCredentialRow)
                    .where(
                        PasskeyCredentialRow.account_ref == account_ref,
                        PasskeyCredentialRow.status_code == "active",
                    )
                    .order_by(PasskeyCredentialRow.passkey_credential_ref)
                )
            ).all()
        )


async def _register_passkey(
    service: PasskeyFlowService,
    runtime: DatabaseRuntime,
    *,
    current: _SessionSeed,
    credential_id: bytes,
    label: str = "Passkey",
) -> _RegisteredPasskey:
    private_key = ec.generate_private_key(ec.SECP256R1())
    public_key = ES256.from_cryptography_key(private_key.public_key())
    begun = await service.begin_registration(
        admitted=current.admitted,
        presented_session_secret=current.secret.get_secret_value(),
        expected_origin=_ORIGIN,
    )
    challenge, user_handle = _registration_values(begun.options)
    issued = await service.complete_registration(
        admitted=current.admitted,
        presented_session_secret=current.secret.get_secret_value(),
        webauthn_challenge_ref=begun.webauthn_challenge_ref,
        response=_registration_response(
            challenge=challenge,
            credential_id=credential_id,
            public_key=public_key,
        ),
        label=label,
    )
    async with runtime.session_factory() as session, session.begin():
        passkey_ref = await session.scalar(
            select(PasskeyCredentialRow.passkey_credential_ref).where(
                PasskeyCredentialRow.credential_id == credential_id
            )
        )
    assert passkey_ref is not None
    return _RegisteredPasskey(
        passkey_credential_ref=passkey_ref,
        credential_id=credential_id,
        user_handle=user_handle,
        private_key=private_key,
        issued=issued,
    )


async def _auth_session_count(runtime: DatabaseRuntime, account_ref: UUID) -> int:
    async with runtime.session_factory() as session, session.begin():
        value = await session.scalar(
            select(func.count())
            .select_from(AuthSessionRow)
            .where(AuthSessionRow.account_ref == account_ref)
        )
    return int(value or 0)


async def _credential_by_id(
    runtime: DatabaseRuntime,
    credential_id: bytes,
) -> PasskeyCredentialRow:
    async with runtime.session_factory() as session, session.begin():
        row = await session.scalar(
            select(PasskeyCredentialRow).where(
                PasskeyCredentialRow.credential_id == credential_id
            )
        )
    assert row is not None
    return row


def _lifecycle_limiters() -> LifecycleLimiters:
    return LifecycleLimiters(
        signup_email=KeyedRateLimiter(capacity=100, window_seconds=60, max_keys=128),
        signup_source=KeyedRateLimiter(capacity=100, window_seconds=60, max_keys=128),
        recovery_email=KeyedRateLimiter(capacity=100, window_seconds=60, max_keys=128),
        recovery_source=KeyedRateLimiter(capacity=100, window_seconds=60, max_keys=128),
        reauth=KeyedRateLimiter(capacity=100, window_seconds=60, max_keys=128),
    )


def _password_lifecycle(runtime: DatabaseRuntime) -> MultiAuthenticatorLifecycleService:
    settings = _settings()
    return MultiAuthenticatorLifecycleService(
        session_factory=runtime.session_factory,
        settings=settings,
        password_kdf=cast(Any, object()),
        breach_checker=cast(Any, object()),
        otp_codec=SignupOtpCodec(
            key_ring=settings.signup_otp_key_bytes,
            current_key_id=settings.signup_otp_current_key_id,
        ),
        email_delivery=cast(Any, object()),
        limiters=_lifecycle_limiters(),
    )


def _disable_account_under_security_lock(database: Any, account_ref: UUID) -> None:
    now = datetime.now(UTC)
    with psycopg.connect(
        **database.connection_kwargs(
            "dante_migrator",
            database.cluster.migrator_password,
        )
    ) as connection:
        connection.execute("SET ROLE dante_owner")
        connection.execute("SET search_path TO pg_catalog,dante,pg_temp")
        connection.execute("SELECT dante.acquire_account_security_lock(%s)", (account_ref,))
        connection.execute(
            """
            UPDATE dante.account
            SET status_code = 'disabled', disabled_at = %s
            WHERE account_ref = %s AND status_code = 'active'
            """,
            (now, account_ref),
        )
        connection.commit()


def _lost_commit_ack() -> DBAPIError:
    return DBAPIError(
        "COMMIT",
        None,
        RuntimeError("synthetic lost commit acknowledgement"),
        connection_invalidated=True,
    )


@pytest.mark.asyncio
async def test_real_fido2_registration_authentication_reauth_replay_and_removal(
    migrated_database: Any,
) -> None:
    async with _service(migrated_database) as (service, runtime):
        account_ref, _email_ref, sessions = await _seed_account(
            runtime,
            email="passkey-owner@example.com",
            password_present=True,
        )
        current = sessions[0]
        private_key = ec.generate_private_key(ec.SECP256R1())
        public_key = ES256.from_cryptography_key(private_key.public_key())
        credential_id = b"passkey-credential-0001"

        begun = await service.begin_registration(
            admitted=current.admitted,
            presented_session_secret=current.secret.get_secret_value(),
            expected_origin=_ORIGIN,
        )
        registration_challenge, user_handle = _registration_values(begun.options)
        registered = await service.complete_registration(
            admitted=current.admitted,
            presented_session_secret=current.secret.get_secret_value(),
            webauthn_challenge_ref=begun.webauthn_challenge_ref,
            response=_registration_response(
                challenge=registration_challenge,
                credential_id=credential_id,
                public_key=public_key,
            ),
            label="Laptop passkey",
            transports=("internal", "hybrid"),
        )

        passkeys = await _active_passkeys(runtime, account_ref)
        assert len(passkeys) == 1
        assert passkeys[0].credential_id == credential_id
        assert passkeys[0].cose_algorithm == ES256.ALGORITHM
        assert passkeys[0].backup_eligible is True
        assert passkeys[0].transports == ["internal", "hybrid"]

        registered_admitted = AdmittedSession(
            principal=registered.principal,
            expires_at=registered.expires_at,
            csrf_token=registered.csrf_token,
        )
        projected = await service.list_passkeys(admitted=registered_admitted)
        assert len(projected) == 1
        assert projected[0].passkey_credential_ref == passkeys[0].passkey_credential_ref
        assert projected[0].label == "Laptop passkey"
        assert projected[0].transports == ("internal", "hybrid")
        assert projected[0].backup_eligible is True

        await service.update_label(
            admitted=registered_admitted,
            presented_session_secret=registered.session_secret.get_secret_value(),
            passkey_credential_ref=passkeys[0].passkey_credential_ref,
            label="Travel laptop",
        )
        projected = await service.list_passkeys(admitted=registered_admitted)
        assert projected[0].label == "Travel laptop"

        second_begin = await service.begin_registration(
            admitted=registered_admitted,
            presented_session_secret=registered.session_secret.get_secret_value(),
            expected_origin=_ORIGIN,
        )
        second_challenge, _same_user_handle = _registration_values(second_begin.options)
        with pytest.raises(PasskeyAlreadyRegisteredError):
            await service.complete_registration(
                admitted=registered_admitted,
                presented_session_secret=registered.session_secret.get_secret_value(),
                webauthn_challenge_ref=second_begin.webauthn_challenge_ref,
                response=_registration_response(
                    challenge=second_challenge,
                    credential_id=credential_id,
                    public_key=public_key,
                ),
                label="Duplicate",
            )

        auth_begin = await service.begin_authentication(
            expected_origin=_ORIGIN,
            source_context="test-source",
        )
        auth_challenge = _authentication_challenge(auth_begin.options)
        assertion = _authentication_response(
            challenge=auth_challenge,
            credential_id=credential_id,
            user_handle=user_handle,
            private_key=private_key,
            counter=5,
            backed_up=True,
        )
        authenticated = await service.complete_authentication(
            webauthn_challenge_ref=auth_begin.webauthn_challenge_ref,
            response=assertion,
            source_context="test-source",
        )
        assert authenticated.principal.account_ref == account_ref

        with pytest.raises(PasskeyChallengeInvalidOrExpiredError):
            await service.complete_authentication(
                webauthn_challenge_ref=auth_begin.webauthn_challenge_ref,
                response=assertion,
                source_context="test-source",
            )

        reauth_admitted = AdmittedSession(
            principal=authenticated.principal,
            expires_at=authenticated.expires_at,
            csrf_token=authenticated.csrf_token,
        )
        reauth_begin = await service.begin_reauthentication(
            admitted=reauth_admitted,
            presented_session_secret=authenticated.session_secret.get_secret_value(),
            expected_origin=_ORIGIN,
        )
        reauth_challenge = _authentication_challenge(reauth_begin.options)
        reauthenticated = await service.complete_reauthentication(
            admitted=reauth_admitted,
            presented_session_secret=authenticated.session_secret.get_secret_value(),
            webauthn_challenge_ref=reauth_begin.webauthn_challenge_ref,
            response=_authentication_response(
                challenge=reauth_challenge,
                credential_id=credential_id,
                user_handle=user_handle,
                private_key=private_key,
                counter=6,
                backed_up=True,
            ),
        )
        assert reauthenticated.principal.auth_session_ref == authenticated.principal.auth_session_ref
        assert reauthenticated.principal.recent_auth_at >= authenticated.principal.recent_auth_at

        removed = await service.remove_passkey(
            admitted=AdmittedSession(
                principal=reauthenticated.principal,
                expires_at=reauthenticated.expires_at,
                csrf_token=reauthenticated.csrf_token,
            ),
            presented_session_secret=reauthenticated.session_secret.get_secret_value(),
            passkey_credential_ref=passkeys[0].passkey_credential_ref,
        )
        assert removed.principal.account_ref == account_ref
        assert await _active_passkeys(runtime, account_ref) == []

        revoked_begin = await service.begin_authentication(
            expected_origin=_ORIGIN,
            source_context="revoked-test",
        )
        with pytest.raises(PasskeyVerificationFailedError):
            await service.complete_authentication(
                webauthn_challenge_ref=revoked_begin.webauthn_challenge_ref,
                response=_authentication_response(
                    challenge=_authentication_challenge(revoked_begin.options),
                    credential_id=credential_id,
                    user_handle=user_handle,
                    private_key=private_key,
                    counter=7,
                    backed_up=True,
                ),
                source_context="revoked-test",
            )


@pytest.mark.asyncio
async def test_concurrent_passkey_removals_preserve_last_authenticator(
    migrated_database: Any,
) -> None:
    async with _service(migrated_database) as (service, runtime):
        account_ref, _email_ref, sessions = await _seed_account(
            runtime,
            email="passkey-only@example.com",
            password_present=False,
            session_count=2,
        )
        now = datetime.now(UTC)
        user_handle = b"h" * 32
        passkey_refs = (uuid7(), uuid7())
        async with runtime.session_factory() as session, session.begin():
            session.add(
                WebAuthnAccountRow(
                    account_ref=account_ref,
                    user_handle=user_handle,
                    created_at=now,
                )
            )
            session.add_all(
                [
                    PasskeyCredentialRow(
                        passkey_credential_ref=passkey_ref,
                        account_ref=account_ref,
                        credential_id=f"race-{index}".encode("ascii"),
                        credential_public_key=b"synthetic-public-key",
                        cose_algorithm=-7,
                        sign_count=0,
                        backup_eligible=True,
                        backup_state=False,
                        transports=[],
                        label=f"Passkey {index}",
                        status_code="active",
                        created_at=now,
                        updated_at=now,
                        last_used_at=None,
                        revoked_at=None,
                        revocation_reason_code=None,
                    )
                    for index, passkey_ref in enumerate(passkey_refs)
                ]
            )

        async def remove(index: int) -> object:
            current = sessions[index]
            try:
                return await service.remove_passkey(
                    admitted=current.admitted,
                    presented_session_secret=current.secret.get_secret_value(),
                    passkey_credential_ref=passkey_refs[index],
                )
            except AuthenticatorRemovalBlockedError as exc:
                return exc

        outcomes = await asyncio.gather(remove(0), remove(1))

        assert sum(isinstance(outcome, AuthenticatorRemovalBlockedError) for outcome in outcomes) == 1
        assert len(await _active_passkeys(runtime, account_ref)) == 1

        async with runtime.session_factory() as session, session.begin():
            challenge_count = await session.scalar(
                select(func.count()).select_from(WebAuthnChallengeRow)
            )
        assert challenge_count == 0


@pytest.mark.asyncio
async def test_passkey_removal_and_provider_unlink_share_account_wide_lock(
    migrated_database: Any,
) -> None:
    async with _service(migrated_database) as (service, runtime):
        account_ref, email_ref, sessions = await _seed_account(
            runtime,
            email="passkey-provider-race@example.com",
            password_present=False,
            session_count=2,
        )
        provider_ref = await _seed_provider(
            runtime,
            account_ref=account_ref,
            email_ref=email_ref,
            subject="passkey-provider-race",
        )
        now = datetime.now(UTC)
        passkey_ref = uuid7()
        async with runtime.session_factory() as session, session.begin():
            session.add(
                WebAuthnAccountRow(
                    account_ref=account_ref,
                    user_handle=b"p" * 32,
                    created_at=now,
                )
            )
            session.add(
                PasskeyCredentialRow(
                    passkey_credential_ref=passkey_ref,
                    account_ref=account_ref,
                    credential_id=b"passkey-provider-race",
                    credential_public_key=b"synthetic-public-key",
                    cose_algorithm=-7,
                    sign_count=0,
                    backup_eligible=True,
                    backup_state=False,
                    transports=[],
                    label="Passkey",
                    status_code="active",
                    created_at=now,
                    updated_at=now,
                    last_used_at=None,
                    revoked_at=None,
                    revocation_reason_code=None,
                )
            )

        authenticators = AuthenticatorLifecycleService(
            session_factory=runtime.session_factory,
            settings=_settings(),
            apple_reconciler=None,
        )

        async def remove_passkey() -> object:
            try:
                return await service.remove_passkey(
                    admitted=sessions[0].admitted,
                    presented_session_secret=sessions[0].secret.get_secret_value(),
                    passkey_credential_ref=passkey_ref,
                )
            except AuthenticatorRemovalBlockedError as exc:
                return exc

        async def unlink_provider() -> object:
            try:
                return await authenticators.unlink_provider(
                    admitted=sessions[1].admitted,
                    presented_session_secret=sessions[1].secret.get_secret_value(),
                    external_identity_ref=provider_ref,
                )
            except AuthenticatorRemovalBlockedError as exc:
                return exc

        outcomes = await asyncio.gather(remove_passkey(), unlink_provider())
        assert sum(isinstance(outcome, AuthenticatorRemovalBlockedError) for outcome in outcomes) == 1

        async with runtime.session_factory() as session, session.begin():
            active_passkeys = await session.scalar(
                select(func.count())
                .select_from(PasskeyCredentialRow)
                .where(
                    PasskeyCredentialRow.account_ref == account_ref,
                    PasskeyCredentialRow.status_code == "active",
                )
            )
            active_providers = await session.scalar(
                select(func.count())
                .select_from(ExternalIdentityRow)
                .where(
                    ExternalIdentityRow.account_ref == account_ref,
                    ExternalIdentityRow.status_code == "active",
                )
            )
        assert int(active_passkeys or 0) + int(active_providers or 0) == 1


@pytest.mark.asyncio
async def test_same_credential_registration_race_across_accounts_is_db_unique_and_never_rebinds(
    migrated_database: Any,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    async with _service(migrated_database) as (service, runtime):
        account_a, _email_a, sessions_a = await _seed_account(
            runtime,
            email="passkey-race-a@example.com",
            password_present=True,
        )
        account_b, _email_b, sessions_b = await _seed_account(
            runtime,
            email="passkey-race-b@example.com",
            password_present=True,
        )
        private_key = ec.generate_private_key(ec.SECP256R1())
        public_key = ES256.from_cryptography_key(private_key.public_key())
        credential_id = b"cross-account-credential-race"

        begin_a, begin_b = await asyncio.gather(
            service.begin_registration(
                admitted=sessions_a[0].admitted,
                presented_session_secret=sessions_a[0].secret.get_secret_value(),
                expected_origin=_ORIGIN,
            ),
            service.begin_registration(
                admitted=sessions_b[0].admitted,
                presented_session_secret=sessions_b[0].secret.get_secret_value(),
                expected_origin=_ORIGIN,
            ),
        )
        challenge_a, _handle_a = _registration_values(begin_a.options)
        challenge_b, _handle_b = _registration_values(begin_b.options)

        original_scalar = AsyncSession.scalar
        precheck_count = 0
        precheck_lock = asyncio.Lock()
        both_prechecked = asyncio.Event()

        async def scalar_with_registration_barrier(
            database_session: AsyncSession,
            statement: Any,
            *args: Any,
            **kwargs: Any,
        ) -> Any:
            nonlocal precheck_count
            result = await original_scalar(database_session, statement, *args, **kwargs)
            descriptions = getattr(statement, "column_descriptions", ())
            expression = descriptions[0].get("expr") if len(descriptions) == 1 else None
            if (
                result is None
                and getattr(expression, "key", None) == "passkey_credential_ref"
                and getattr(expression, "class_", None) is PasskeyCredentialRow
            ):
                async with precheck_lock:
                    if precheck_count < 2:
                        precheck_count += 1
                        if precheck_count == 2:
                            both_prechecked.set()
                if precheck_count <= 2:
                    await both_prechecked.wait()
            return result

        monkeypatch.setattr(AsyncSession, "scalar", scalar_with_registration_barrier)

        async def complete(
            current: _SessionSeed,
            begun_ref: UUID,
            challenge: bytes,
        ) -> object:
            try:
                return await service.complete_registration(
                    admitted=current.admitted,
                    presented_session_secret=current.secret.get_secret_value(),
                    webauthn_challenge_ref=begun_ref,
                    response=_registration_response(
                        challenge=challenge,
                        credential_id=credential_id,
                        public_key=public_key,
                    ),
                    label="Shared credential race",
                )
            except PasskeyAlreadyRegisteredError as exc:
                return exc

        outcomes = await asyncio.gather(
            complete(sessions_a[0], begin_a.webauthn_challenge_ref, challenge_a),
            complete(sessions_b[0], begin_b.webauthn_challenge_ref, challenge_b),
        )
        assert precheck_count == 2
        assert sum(isinstance(outcome, PasskeyAlreadyRegisteredError) for outcome in outcomes) == 1

        async with runtime.session_factory() as session, session.begin():
            rows = list(
                (
                    await session.scalars(
                        select(PasskeyCredentialRow).where(
                            PasskeyCredentialRow.credential_id == credential_id
                        )
                    )
                ).all()
            )
        assert len(rows) == 1
        assert rows[0].account_ref in {account_a, account_b}


@pytest.mark.asyncio
async def test_verified_passkey_signin_cannot_outlive_concurrent_passkey_removal(
    migrated_database: Any,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    async with _service(migrated_database) as (service, runtime):
        account_ref, _email_ref, sessions = await _seed_account(
            runtime,
            email="signin-remove-race@example.com",
            password_present=True,
        )
        registered = await _register_passkey(
            service,
            runtime,
            current=sessions[0],
            credential_id=b"signin-remove-race",
        )
        before_sessions = await _auth_session_count(runtime, account_ref)
        begun = await service.begin_authentication(
            expected_origin=_ORIGIN,
            source_context="signin-remove-race",
        )
        response = _authentication_response(
            challenge=_authentication_challenge(begun.options),
            credential_id=registered.credential_id,
            user_handle=registered.user_handle,
            private_key=registered.private_key,
            counter=10,
            backed_up=False,
        )

        original_verify = service._verify_assertion
        verified = asyncio.Event()
        release = asyncio.Event()

        async def pause_after_real_verify(**kwargs: Any) -> WebAuthnAssertionEvidence:
            evidence = await original_verify(**kwargs)
            verified.set()
            await release.wait()
            return evidence

        monkeypatch.setattr(service, "_verify_assertion", pause_after_real_verify)
        signin = asyncio.create_task(
            service.complete_authentication(
                webauthn_challenge_ref=begun.webauthn_challenge_ref,
                response=response,
                source_context="signin-remove-race",
            )
        )
        await verified.wait()

        await service.remove_passkey(
            admitted=_admitted(registered.issued),
            presented_session_secret=registered.issued.session_secret.get_secret_value(),
            passkey_credential_ref=registered.passkey_credential_ref,
        )
        release.set()

        with pytest.raises(AuthStateChangedError):
            await signin
        assert await _auth_session_count(runtime, account_ref) == before_sessions


@pytest.mark.asyncio
async def test_verified_passkey_signin_cannot_outlive_account_disable(
    migrated_database: Any,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    async with _service(migrated_database) as (service, runtime):
        account_ref, _email_ref, sessions = await _seed_account(
            runtime,
            email="signin-disable-race@example.com",
            password_present=True,
        )
        registered = await _register_passkey(
            service,
            runtime,
            current=sessions[0],
            credential_id=b"signin-disable-race",
        )
        before_sessions = await _auth_session_count(runtime, account_ref)
        begun = await service.begin_authentication(
            expected_origin=_ORIGIN,
            source_context="signin-disable-race",
        )
        response = _authentication_response(
            challenge=_authentication_challenge(begun.options),
            credential_id=registered.credential_id,
            user_handle=registered.user_handle,
            private_key=registered.private_key,
            counter=10,
            backed_up=False,
        )

        original_verify = service._verify_assertion
        verified = asyncio.Event()
        release = asyncio.Event()

        async def pause_after_real_verify(**kwargs: Any) -> WebAuthnAssertionEvidence:
            evidence = await original_verify(**kwargs)
            verified.set()
            await release.wait()
            return evidence

        monkeypatch.setattr(service, "_verify_assertion", pause_after_real_verify)
        signin = asyncio.create_task(
            service.complete_authentication(
                webauthn_challenge_ref=begun.webauthn_challenge_ref,
                response=response,
                source_context="signin-disable-race",
            )
        )
        await verified.wait()
        await asyncio.to_thread(
            _disable_account_under_security_lock,
            migrated_database,
            account_ref,
        )
        release.set()

        with pytest.raises(AccountUnavailableError):
            await signin
        assert await _auth_session_count(runtime, account_ref) == before_sessions


@pytest.mark.asyncio
async def test_passkey_reauth_rejects_bearer_rotated_after_real_assertion_verification(
    migrated_database: Any,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    async with _service(migrated_database) as (service, runtime):
        account_ref, email_ref, sessions = await _seed_account(
            runtime,
            email="reauth-bearer-race@example.com",
            password_present=True,
        )
        provider_ref = await _seed_provider(
            runtime,
            account_ref=account_ref,
            email_ref=email_ref,
            subject="reauth-bearer-race",
        )
        registered = await _register_passkey(
            service,
            runtime,
            current=sessions[0],
            credential_id=b"reauth-bearer-race",
        )
        begun = await service.begin_reauthentication(
            admitted=_admitted(registered.issued),
            presented_session_secret=registered.issued.session_secret.get_secret_value(),
            expected_origin=_ORIGIN,
        )
        response = _authentication_response(
            challenge=_authentication_challenge(begun.options),
            credential_id=registered.credential_id,
            user_handle=registered.user_handle,
            private_key=registered.private_key,
            counter=10,
            backed_up=False,
        )

        original_verify = service._verify_assertion
        verified = asyncio.Event()
        release = asyncio.Event()

        async def pause_after_real_verify(**kwargs: Any) -> WebAuthnAssertionEvidence:
            evidence = await original_verify(**kwargs)
            verified.set()
            await release.wait()
            return evidence

        monkeypatch.setattr(service, "_verify_assertion", pause_after_real_verify)
        reauth = asyncio.create_task(
            service.complete_reauthentication(
                admitted=_admitted(registered.issued),
                presented_session_secret=registered.issued.session_secret.get_secret_value(),
                webauthn_challenge_ref=begun.webauthn_challenge_ref,
                response=response,
            )
        )
        await verified.wait()

        authenticators = AuthenticatorLifecycleService(
            session_factory=runtime.session_factory,
            settings=_settings(),
            apple_reconciler=None,
        )
        await authenticators.unlink_provider(
            admitted=_admitted(registered.issued),
            presented_session_secret=registered.issued.session_secret.get_secret_value(),
            external_identity_ref=provider_ref,
        )
        release.set()

        with pytest.raises(AuthStateChangedError):
            await reauth


@pytest.mark.asyncio
async def test_passkey_and_password_removal_share_one_account_anti_lockout_authority(
    migrated_database: Any,
) -> None:
    async with _service(migrated_database) as (service, runtime):
        account_ref, _email_ref, sessions = await _seed_account(
            runtime,
            email="passkey-password-race@example.com",
            password_present=True,
            session_count=2,
        )
        registered = await _register_passkey(
            service,
            runtime,
            current=sessions[0],
            credential_id=b"passkey-password-race",
        )
        lifecycle = _password_lifecycle(runtime)
        start = asyncio.Event()

        async def remove_passkey() -> object:
            await start.wait()
            try:
                return await service.remove_passkey(
                    admitted=_admitted(registered.issued),
                    presented_session_secret=registered.issued.session_secret.get_secret_value(),
                    passkey_credential_ref=registered.passkey_credential_ref,
                )
            except AuthenticatorRemovalBlockedError as exc:
                return exc

        async def remove_password() -> object:
            await start.wait()
            try:
                return await lifecycle.remove_password(
                    admitted=sessions[1].admitted,
                    presented_session_secret=sessions[1].secret.get_secret_value(),
                )
            except AuthenticatorRemovalBlockedError as exc:
                return exc

        passkey_task = asyncio.create_task(remove_passkey())
        password_task = asyncio.create_task(remove_password())
        start.set()
        outcomes = await asyncio.gather(passkey_task, password_task)
        assert sum(isinstance(outcome, AuthenticatorRemovalBlockedError) for outcome in outcomes) == 1

        async with runtime.session_factory() as session, session.begin():
            password_count = await session.scalar(
                select(func.count())
                .select_from(PasswordCredentialRow)
                .where(PasswordCredentialRow.account_ref == account_ref)
            )
            passkey_count = await session.scalar(
                select(func.count())
                .select_from(PasskeyCredentialRow)
                .where(
                    PasskeyCredentialRow.account_ref == account_ref,
                    PasskeyCredentialRow.status_code == "active",
                )
            )
        assert int(password_count or 0) + int(passkey_count or 0) == 1


@pytest.mark.asyncio
async def test_concurrent_valid_assertions_serialize_without_counter_regression(
    migrated_database: Any,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    async with _service(migrated_database) as (service, runtime):
        account_ref, _email_ref, sessions = await _seed_account(
            runtime,
            email="concurrent-assertions@example.com",
            password_present=True,
        )
        registered = await _register_passkey(
            service,
            runtime,
            current=sessions[0],
            credential_id=b"concurrent-assertions",
        )
        begins = await asyncio.gather(
            service.begin_authentication(
                expected_origin=_ORIGIN,
                source_context="assertion-10",
            ),
            service.begin_authentication(
                expected_origin=_ORIGIN,
                source_context="assertion-11",
            ),
        )
        responses = (
            _authentication_response(
                challenge=_authentication_challenge(begins[0].options),
                credential_id=registered.credential_id,
                user_handle=registered.user_handle,
                private_key=registered.private_key,
                counter=10,
                backed_up=False,
            ),
            _authentication_response(
                challenge=_authentication_challenge(begins[1].options),
                credential_id=registered.credential_id,
                user_handle=registered.user_handle,
                private_key=registered.private_key,
                counter=11,
                backed_up=True,
            ),
        )

        original_verify = service._verify_assertion
        verified_count = 0
        verified_lock = asyncio.Lock()
        both_verified = asyncio.Event()

        async def verify_then_barrier(**kwargs: Any) -> WebAuthnAssertionEvidence:
            nonlocal verified_count
            evidence = await original_verify(**kwargs)
            async with verified_lock:
                verified_count += 1
                if verified_count == 2:
                    both_verified.set()
            await both_verified.wait()
            return evidence

        monkeypatch.setattr(service, "_verify_assertion", verify_then_barrier)
        authenticated = await asyncio.gather(
            service.complete_authentication(
                webauthn_challenge_ref=begins[0].webauthn_challenge_ref,
                response=responses[0],
                source_context="assertion-10",
            ),
            service.complete_authentication(
                webauthn_challenge_ref=begins[1].webauthn_challenge_ref,
                response=responses[1],
                source_context="assertion-11",
            ),
        )

        assert verified_count == 2
        assert authenticated[0].principal.auth_session_ref != authenticated[1].principal.auth_session_ref
        credential = await _credential_by_id(runtime, registered.credential_id)
        assert credential.sign_count >= 11
        assert credential.backup_state in {False, True}
        assert credential.last_used_at is not None
        assert credential.updated_at >= credential.last_used_at
        assert await _auth_session_count(runtime, account_ref) == 3


@pytest.mark.asyncio
async def test_ambiguous_signin_commit_reconciles_after_later_valid_assertion_advances_credential(
    migrated_database: Any,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    async with _service(migrated_database) as (service, runtime):
        account_ref, _email_ref, sessions = await _seed_account(
            runtime,
            email="ambiguous-signin@example.com",
            password_present=True,
        )
        registered = await _register_passkey(
            service,
            runtime,
            current=sessions[0],
            credential_id=b"ambiguous-signin",
        )
        first_begin = await service.begin_authentication(
            expected_origin=_ORIGIN,
            source_context="ambiguous-first",
        )
        second_begin = await service.begin_authentication(
            expected_origin=_ORIGIN,
            source_context="ambiguous-second",
        )
        first_response = _authentication_response(
            challenge=_authentication_challenge(first_begin.options),
            credential_id=registered.credential_id,
            user_handle=registered.user_handle,
            private_key=registered.private_key,
            counter=10,
            backed_up=False,
        )
        second_response = _authentication_response(
            challenge=_authentication_challenge(second_begin.options),
            credential_id=registered.credential_id,
            user_handle=registered.user_handle,
            private_key=registered.private_key,
            counter=11,
            backed_up=True,
        )

        original_commit = AsyncSession.commit
        explicit_commit_count = 0
        lost_ack_injected = False

        async def commit_with_one_lost_ack(database_session: AsyncSession) -> None:
            nonlocal explicit_commit_count, lost_ack_injected
            await original_commit(database_session)
            explicit_commit_count += 1
            if not lost_ack_injected and explicit_commit_count == 2:
                lost_ack_injected = True
                raise _lost_commit_ack()

        monkeypatch.setattr(AsyncSession, "commit", commit_with_one_lost_ack)
        original_reconcile = service._reconcile_authentication
        later_sessions: list[IssuedSession] = []

        async def reconcile_after_later_assertion(**kwargs: Any) -> None:
            later_sessions.append(
                await service.complete_authentication(
                    webauthn_challenge_ref=second_begin.webauthn_challenge_ref,
                    response=second_response,
                    source_context="ambiguous-second",
                )
            )
            await original_reconcile(**kwargs)

        monkeypatch.setattr(service, "_reconcile_authentication", reconcile_after_later_assertion)
        first = await service.complete_authentication(
            webauthn_challenge_ref=first_begin.webauthn_challenge_ref,
            response=first_response,
            source_context="ambiguous-first",
        )

        assert lost_ack_injected is True
        assert len(later_sessions) == 1
        assert first.principal.auth_session_ref != later_sessions[0].principal.auth_session_ref
        credential = await _credential_by_id(runtime, registered.credential_id)
        assert credential.sign_count >= 11
        assert credential.backup_state is True
        assert await _auth_session_count(runtime, account_ref) == 3


@pytest.mark.asyncio
async def test_ambiguous_signin_reconciliation_distinguishes_precommit_and_impossible_state(
    migrated_database: Any,
) -> None:
    async with _service(migrated_database) as (service, runtime):
        _account_ref, _email_ref, sessions = await _seed_account(
            runtime,
            email="ambiguous-precommit@example.com",
            password_present=True,
        )
        registered = await _register_passkey(
            service,
            runtime,
            current=sessions[0],
            credential_id=b"ambiguous-precommit",
        )
        begun = await service.begin_authentication(
            expected_origin=_ORIGIN,
            source_context="ambiguous-precommit",
        )
        response = _authentication_response(
            challenge=_authentication_challenge(begun.options),
            credential_id=registered.credential_id,
            user_handle=registered.user_handle,
            private_key=registered.private_key,
            counter=10,
            backed_up=False,
        )
        parsed = service._parse_authentication(response)
        snapshot = await service._claim_challenge(
            webauthn_challenge_ref=begun.webauthn_challenge_ref,
            ceremony_code="authentication",
            parsed=parsed,
        )
        credential = await service._read_credential_snapshot(
            credential_id=parsed.credential_id,
            account_ref=None,
        )
        assert credential is not None
        evidence = await service._verify_assertion(
            snapshot=snapshot,
            parsed=parsed,
            response=response,
            credential=credential,
        )
        prospective_ref = uuid7()
        prospective_verifier = session_secret_verifier(generate_session_secret())
        mutation_at = datetime.now(UTC)
        expires_at = mutation_at + timedelta(seconds=_settings().session_max_age_seconds)

        with pytest.raises(AuthServiceUnavailableError) as precommit:
            await service._reconcile_authentication(
                snapshot=snapshot,
                credential=credential,
                evidence=evidence,
                auth_session_ref=prospective_ref,
                secret_verifier=prospective_verifier,
                mutation_at=mutation_at,
                expires_at=expires_at,
            )
        assert precommit.value.retryable is True

        await service._delete_challenge(snapshot)
        with pytest.raises(AuthIntegrityError):
            await service._reconcile_authentication(
                snapshot=snapshot,
                credential=credential,
                evidence=evidence,
                auth_session_ref=prospective_ref,
                secret_verifier=prospective_verifier,
                mutation_at=mutation_at,
                expires_at=expires_at,
            )


@pytest.mark.asyncio
async def test_ambiguous_reauth_commit_reconciles_after_later_valid_assertion_advances_credential(
    migrated_database: Any,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    async with _service(migrated_database) as (service, runtime):
        _account_ref, _email_ref, sessions = await _seed_account(
            runtime,
            email="ambiguous-reauth@example.com",
            password_present=True,
        )
        registered = await _register_passkey(
            service,
            runtime,
            current=sessions[0],
            credential_id=b"ambiguous-reauth",
        )
        reauth_begin = await service.begin_reauthentication(
            admitted=_admitted(registered.issued),
            presented_session_secret=registered.issued.session_secret.get_secret_value(),
            expected_origin=_ORIGIN,
        )
        later_begin = await service.begin_authentication(
            expected_origin=_ORIGIN,
            source_context="ambiguous-reauth-later",
        )
        reauth_response = _authentication_response(
            challenge=_authentication_challenge(reauth_begin.options),
            credential_id=registered.credential_id,
            user_handle=registered.user_handle,
            private_key=registered.private_key,
            counter=10,
            backed_up=False,
        )
        later_response = _authentication_response(
            challenge=_authentication_challenge(later_begin.options),
            credential_id=registered.credential_id,
            user_handle=registered.user_handle,
            private_key=registered.private_key,
            counter=11,
            backed_up=True,
        )

        original_commit = AsyncSession.commit
        explicit_commit_count = 0
        lost_ack_injected = False

        async def commit_with_one_lost_ack(database_session: AsyncSession) -> None:
            nonlocal explicit_commit_count, lost_ack_injected
            await original_commit(database_session)
            explicit_commit_count += 1
            if not lost_ack_injected and explicit_commit_count == 2:
                lost_ack_injected = True
                raise _lost_commit_ack()

        monkeypatch.setattr(AsyncSession, "commit", commit_with_one_lost_ack)
        original_reconcile = service._reconcile_reauthentication
        later_sessions: list[IssuedSession] = []

        async def reconcile_after_later_assertion(**kwargs: Any) -> None:
            later_sessions.append(
                await service.complete_authentication(
                    webauthn_challenge_ref=later_begin.webauthn_challenge_ref,
                    response=later_response,
                    source_context="ambiguous-reauth-later",
                )
            )
            await original_reconcile(**kwargs)

        monkeypatch.setattr(service, "_reconcile_reauthentication", reconcile_after_later_assertion)
        reauthenticated = await service.complete_reauthentication(
            admitted=_admitted(registered.issued),
            presented_session_secret=registered.issued.session_secret.get_secret_value(),
            webauthn_challenge_ref=reauth_begin.webauthn_challenge_ref,
            response=reauth_response,
        )

        assert lost_ack_injected is True
        assert reauthenticated.principal.auth_session_ref == registered.issued.principal.auth_session_ref
        assert len(later_sessions) == 1
        credential = await _credential_by_id(runtime, registered.credential_id)
        assert credential.sign_count >= 11
        assert credential.backup_state is True
