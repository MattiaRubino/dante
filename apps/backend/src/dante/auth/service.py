"""Access/Auth application service and process-scoped runtime resources."""

from __future__ import annotations

import asyncio
import logging
import math
import time
from collections import OrderedDict
from contextlib import AsyncExitStack, suppress
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from hashlib import sha256
from typing import cast
from uuid import UUID, uuid7

import httpx2
from pydantic import SecretStr
from sqlalchemy import func, select, update
from sqlalchemy.exc import DBAPIError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from dante.auth.apple_crypto import AppleGrantCipher
from dante.auth.contracts import (
    AccountUnavailableError,
    AdmittedSession,
    AuthInputError,
    AuthIntegrityError,
    AuthServiceUnavailableError,
    InvalidCredentialsError,
    IssuedSession,
    PasswordCompromisedError,
    Principal,
    SigninRateLimitedError,
)
from dante.auth.email import EmailNormalizationError, NormalizedEmail, normalize_email
from dante.auth.passwords import (
    BreachCheckUnavailableError,
    HibpPasswordChecker,
    PasswordInputError,
    PasswordKdf,
    normalize_password_for_authentication,
)
from dante.auth.provider_runtime import ProviderRuntime
from dante.auth.sessions import (
    decode_session_secret,
    derive_csrf_token,
    generate_session_secret,
    session_secret_verifier,
    session_secret_verifier_from_raw,
)
from dante.auth.webauthn import WebAuthnPolicy
from dante.platform.config.auth import AuthSettings
from dante.platform.database.mappings.auth import (
    AccountRow,
    AuthSessionRow,
    EmailIdentityRow,
    PasswordCredentialRow,
)
from dante.platform.database.runtime import DatabaseRuntime
from dante.platform.observability.logging import log_event
from dante.platform.observability.metrics import AuthTelemetry, DependencyOutcome, SigninOutcome

_LOGGER = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True)
class _CredentialSnapshot:
    account_ref: UUID
    account_status_code: str
    email_identity_ref: UUID
    email_verified: bool
    password_credential_ref: UUID
    verifier: str
    pepper_key_id: str
    credential_updated_at: datetime


@dataclass(slots=True)
class _TokenBucket:
    tokens: float
    updated_at: float


class SigninAttemptLimiter:
    """Bounded-memory per-process ingress guard ahead of expensive KDF work."""

    def __init__(self, *, capacity: int, window_seconds: float, max_keys: int) -> None:
        self._capacity = float(capacity)
        self._refill_rate = float(capacity) / window_seconds
        self._max_keys = max_keys
        self._buckets: OrderedDict[bytes, _TokenBucket] = OrderedDict()
        self._lock = asyncio.Lock()

    async def consume(self, comparison_key: str) -> None:
        """Consume one token or raise with a bounded Retry-After hint."""
        key = sha256(comparison_key.encode("utf-8")).digest()
        now = time.monotonic()

        async with self._lock:
            bucket = self._buckets.pop(key, None)
            if bucket is None:
                if len(self._buckets) >= self._max_keys:
                    self._buckets.popitem(last=False)
                bucket = _TokenBucket(tokens=self._capacity, updated_at=now)

            elapsed = max(0.0, now - bucket.updated_at)
            bucket.tokens = min(
                self._capacity,
                bucket.tokens + elapsed * self._refill_rate,
            )
            bucket.updated_at = now

            if bucket.tokens < 1.0:
                self._buckets[key] = bucket
                wait_seconds = (1.0 - bucket.tokens) / self._refill_rate
                raise SigninRateLimitedError(max(1, math.ceil(wait_seconds)))

            bucket.tokens -= 1.0
            self._buckets[key] = bucket


class AuthService:
    """Application-level Auth operations over canonical PostgreSQL state."""

    def __init__(
        self,
        *,
        session_factory: async_sessionmaker[AsyncSession],
        settings: AuthSettings,
        password_kdf: PasswordKdf,
        breach_checker: HibpPasswordChecker,
        signin_limiter: SigninAttemptLimiter,
        telemetry: AuthTelemetry | None = None,
    ) -> None:
        self._session_factory = session_factory
        self._settings = settings
        self._password_kdf = password_kdf
        self._breach_checker = breach_checker
        self._signin_limiter = signin_limiter
        self._telemetry = telemetry
        self._csrf_key = settings.csrf_key_bytes

    @property
    def session_cookie_max_age_seconds(self) -> int:
        """Return the browser cookie's overall lifetime; idle expiry stays server-side."""
        return self._settings.session_max_age_seconds

    async def sign_in(
        self,
        *,
        email: str,
        password: str,
        request_id: str,
    ) -> IssuedSession:
        """Record one identity-free outcome around the canonical signin operation."""
        started = time.perf_counter()
        outcome: SigninOutcome = "unexpected"
        try:
            issued = await self._sign_in(
                email=email,
                password=password,
                request_id=request_id,
            )
            outcome = "success"
            return issued
        except AuthInputError:
            outcome = "invalid_input"
            raise
        except InvalidCredentialsError:
            outcome = "invalid_credentials"
            raise
        except AccountUnavailableError:
            outcome = "account_unavailable"
            raise
        except PasswordCompromisedError:
            outcome = "password_compromised"
            raise
        except SigninRateLimitedError:
            outcome = "rate_limited"
            raise
        except AuthServiceUnavailableError:
            outcome = "service_unavailable"
            raise
        finally:
            if self._telemetry is not None:
                with suppress(Exception):
                    self._telemetry.record_signin(
                        outcome,
                        duration=time.perf_counter() - started,
                    )

    async def _sign_in(
        self,
        *,
        email: str,
        password: str,
        request_id: str,
    ) -> IssuedSession:
        """Authenticate password evidence then atomically create one AuthSession."""
        normalized_email = self._normalize_email_for_signin(email)
        normalized_password = self._normalize_password_for_signin(password)
        await self._signin_limiter.consume(normalized_email.comparison_key)

        snapshot = await self._read_credential_snapshot(normalized_email.comparison_key)
        if snapshot is None:
            await self._password_kdf.verify_dummy(normalized_password)
            raise InvalidCredentialsError()

        verification = await self._password_kdf.verify(
            normalized_password=normalized_password,
            verifier=snapshot.verifier,
            pepper_key_id=snapshot.pepper_key_id,
        )
        if not verification.valid:
            raise InvalidCredentialsError()
        if not snapshot.email_verified:
            raise InvalidCredentialsError()
        if snapshot.account_status_code != "active":
            raise AccountUnavailableError()

        dependency_started = time.perf_counter()
        dependency_outcome: DependencyOutcome = "success"
        try:
            breached = await self._breach_checker.is_breached(normalized_password)
        except BreachCheckUnavailableError as exc:
            dependency_outcome = "error"
            log_event(
                _LOGGER,
                logging.WARNING,
                "auth.hibp_unavailable",
                fields={"dependency": "hibp", "outcome": "error", "retryable": True},
                exception=exc,
            )
            breached = False
        finally:
            if self._telemetry is not None:
                with suppress(Exception):
                    self._telemetry.record_dependency(
                        "hibp",
                        outcome=dependency_outcome,
                        duration=time.perf_counter() - dependency_started,
                    )

        if breached:
            raise PasswordCompromisedError()

        replacement_verifier: tuple[str, str] | None = None
        if verification.needs_rehash:
            replacement_verifier = await self._password_kdf.hash_normalized_password(
                normalized_password
            )

        return await self._finalize_signin(
            snapshot=snapshot,
            expected_comparison_key=normalized_email.comparison_key,
            replacement_verifier=replacement_verifier,
        )

    async def admit_session(self, cookie_value: str | None) -> AdmittedSession | None:
        """Resolve one bearer secret against current Account/AuthSession state."""
        if cookie_value is None:
            return None

        raw_secret = decode_session_secret(cookie_value)
        if raw_secret is None:
            return None

        verifier = session_secret_verifier_from_raw(raw_secret)
        now = datetime.now(UTC)

        try:
            async with (
                self._session_factory() as database_session,
                database_session.begin(),
            ):
                statement = (
                    select(AuthSessionRow, AccountRow)
                    .join(
                        AccountRow,
                        AccountRow.account_ref == AuthSessionRow.account_ref,
                    )
                    .where(AuthSessionRow.secret_verifier == verifier)
                )
                row = (await database_session.execute(statement)).one_or_none()
        except SQLAlchemyError as exc:
            raise AuthServiceUnavailableError(retryable=True) from exc

        if row is None:
            return None

        auth_session, account = row
        idle_deadline = auth_session.last_user_activity_at + timedelta(
            seconds=self._settings.session_idle_timeout_seconds
        )
        if (
            auth_session.revoked_at is not None
            or auth_session.expires_at <= now
            or idle_deadline <= now
            or account.status_code != "active"
        ):
            return None

        principal = Principal(
            account_ref=account.account_ref,
            auth_session_ref=auth_session.auth_session_ref,
            authenticated_at=auth_session.authenticated_at,
            recent_auth_at=auth_session.recent_auth_at,
        )
        return AdmittedSession(
            principal=principal,
            expires_at=auth_session.expires_at,
            csrf_token=derive_csrf_token(
                csrf_key=self._csrf_key,
                auth_session_ref=auth_session.auth_session_ref,
                secret_verifier=auth_session.secret_verifier,
            ),
        )

    async def log_out(self, auth_session_ref: UUID) -> None:
        """Idempotently terminally revoke only the current AuthSession."""
        statement = (
            update(AuthSessionRow)
            .where(
                AuthSessionRow.auth_session_ref == auth_session_ref,
                AuthSessionRow.revoked_at.is_(None),
            )
            .values(
                revoked_at=datetime.now(UTC),
                revocation_reason_code="logout",
            )
        )

        try:
            async with (
                self._session_factory() as database_session,
                database_session.begin(),
            ):
                await database_session.execute(statement)
        except SQLAlchemyError as exc:
            raise AuthServiceUnavailableError(retryable=True) from exc

    def _normalize_email_for_signin(self, value: str) -> NormalizedEmail:
        try:
            return normalize_email(value)
        except EmailNormalizationError as exc:
            raise AuthInputError(
                pointer="/email",
                code="invalid_format",
                detail="Enter a valid email address.",
            ) from exc

    @staticmethod
    def _normalize_password_for_signin(value: str) -> str:
        try:
            return normalize_password_for_authentication(value)
        except PasswordInputError as exc:
            raise AuthInputError(
                pointer="/password",
                code=exc.code,
                detail=exc.detail,
                parameters=exc.parameters,
            ) from exc

    async def _read_credential_snapshot(
        self,
        comparison_key: str,
    ) -> _CredentialSnapshot | None:
        statement = (
            select(EmailIdentityRow, AccountRow, PasswordCredentialRow)
            .join(
                AccountRow,
                AccountRow.account_ref == EmailIdentityRow.account_ref,
            )
            .outerjoin(
                PasswordCredentialRow,
                PasswordCredentialRow.account_ref == AccountRow.account_ref,
            )
            .where(EmailIdentityRow.comparison_key == comparison_key)
        )

        try:
            async with (
                self._session_factory() as database_session,
                database_session.begin(),
            ):
                row = (await database_session.execute(statement)).one_or_none()
        except SQLAlchemyError as exc:
            raise AuthServiceUnavailableError(retryable=True) from exc

        if row is None:
            return None

        email_identity = row[0]
        account = row[1]
        credential = cast(PasswordCredentialRow | None, row[2])
        if credential is None:
            return None

        return _CredentialSnapshot(
            account_ref=account.account_ref,
            account_status_code=account.status_code,
            email_identity_ref=email_identity.email_identity_ref,
            email_verified=email_identity.verified_at is not None,
            password_credential_ref=credential.password_credential_ref,
            verifier=credential.verifier,
            pepper_key_id=credential.pepper_key_id,
            credential_updated_at=credential.updated_at,
        )

    async def _finalize_signin(
        self,
        *,
        snapshot: _CredentialSnapshot,
        expected_comparison_key: str,
        replacement_verifier: tuple[str, str] | None,
    ) -> IssuedSession:
        auth_session_ref = uuid7()
        session_secret = generate_session_secret()
        secret_verifier = session_secret_verifier(session_secret)
        now = datetime.now(UTC)
        expires_at = now + timedelta(seconds=self._settings.session_max_age_seconds)
        ambiguous_commit = False

        database_session = self._session_factory()
        try:
            await database_session.begin()
            await database_session.execute(
                select(func.dante.acquire_account_security_lock(snapshot.account_ref))
            )

            account = await database_session.scalar(
                select(AccountRow).where(AccountRow.account_ref == snapshot.account_ref)
            )
            if account is None or account.status_code != "active":
                await database_session.rollback()
                raise AccountUnavailableError()

            email_identity = await database_session.scalar(
                select(EmailIdentityRow).where(
                    EmailIdentityRow.email_identity_ref == snapshot.email_identity_ref,
                    EmailIdentityRow.account_ref == snapshot.account_ref,
                    EmailIdentityRow.comparison_key == expected_comparison_key,
                )
            )
            credential = await database_session.scalar(
                select(PasswordCredentialRow).where(
                    PasswordCredentialRow.account_ref == snapshot.account_ref
                )
            )

            if (
                email_identity is None
                or email_identity.verified_at is None
                or credential is None
                or credential.password_credential_ref != snapshot.password_credential_ref
                or credential.verifier != snapshot.verifier
                or credential.pepper_key_id != snapshot.pepper_key_id
                or credential.updated_at != snapshot.credential_updated_at
            ):
                await database_session.rollback()
                raise InvalidCredentialsError()

            if replacement_verifier is not None:
                credential.verifier = replacement_verifier[0]
                credential.pepper_key_id = replacement_verifier[1]
                credential.updated_at = now

            database_session.add(
                AuthSessionRow(
                    auth_session_ref=auth_session_ref,
                    account_ref=snapshot.account_ref,
                    secret_verifier=secret_verifier,
                    created_at=now,
                    authenticated_at=now,
                    recent_auth_at=now,
                    last_user_activity_at=now,
                    expires_at=expires_at,
                    revoked_at=None,
                    revocation_reason_code=None,
                )
            )

            try:
                await database_session.commit()
            except DBAPIError as exc:
                if not exc.connection_invalidated:
                    raise
                ambiguous_commit = True
        except AccountUnavailableError, InvalidCredentialsError:
            raise
        except SQLAlchemyError as exc:
            await self._safe_rollback(database_session)
            raise AuthServiceUnavailableError(retryable=True) from exc
        finally:
            await database_session.close()

        if ambiguous_commit:
            return await self._reconcile_ambiguous_session(
                auth_session_ref=auth_session_ref,
                account_ref=snapshot.account_ref,
                secret_verifier=secret_verifier,
                created_at=now,
                authenticated_at=now,
                recent_auth_at=now,
                last_user_activity_at=now,
                expires_at=expires_at,
                session_secret=session_secret,
            )

        principal = Principal(
            account_ref=snapshot.account_ref,
            auth_session_ref=auth_session_ref,
            authenticated_at=now,
            recent_auth_at=now,
        )
        return IssuedSession(
            principal=principal,
            expires_at=expires_at,
            session_secret=session_secret,
            csrf_token=derive_csrf_token(
                csrf_key=self._csrf_key,
                auth_session_ref=auth_session_ref,
                secret_verifier=secret_verifier,
            ),
        )

    async def _reconcile_ambiguous_session(
        self,
        *,
        auth_session_ref: UUID,
        account_ref: UUID,
        secret_verifier: bytes,
        created_at: datetime,
        authenticated_at: datetime,
        recent_auth_at: datetime,
        last_user_activity_at: datetime,
        expires_at: datetime,
        session_secret: SecretStr,
    ) -> IssuedSession:
        try:
            async with (
                self._session_factory() as database_session,
                database_session.begin(),
            ):
                persisted = await database_session.scalar(
                    select(AuthSessionRow).where(
                        AuthSessionRow.auth_session_ref == auth_session_ref
                    )
                )
        except SQLAlchemyError as exc:
            raise AuthServiceUnavailableError(retryable=False) from exc

        if persisted is None:
            raise AuthServiceUnavailableError(retryable=True)
        if (
            persisted.account_ref != account_ref
            or persisted.secret_verifier != secret_verifier
            or persisted.created_at != created_at
            or persisted.authenticated_at != authenticated_at
            or persisted.recent_auth_at != recent_auth_at
            or persisted.last_user_activity_at != last_user_activity_at
            or persisted.expires_at != expires_at
            or persisted.revoked_at is not None
            or persisted.revocation_reason_code is not None
        ):
            raise AuthIntegrityError(
                "ambiguous AuthSession reconciliation mismatched canonical state"
            )

        return IssuedSession(
            principal=Principal(
                account_ref=account_ref,
                auth_session_ref=auth_session_ref,
                authenticated_at=persisted.authenticated_at,
                recent_auth_at=persisted.recent_auth_at,
            ),
            expires_at=persisted.expires_at,
            session_secret=session_secret,
            csrf_token=derive_csrf_token(
                csrf_key=self._csrf_key,
                auth_session_ref=auth_session_ref,
                secret_verifier=secret_verifier,
            ),
        )

    @staticmethod
    async def _safe_rollback(database_session: AsyncSession) -> None:
        if not database_session.in_transaction():
            return
        with suppress(SQLAlchemyError):
            await database_session.rollback()


@dataclass(slots=True)
class AuthRuntime:
    """Process-scoped Auth service plus owned crypto/network resources."""

    service: AuthService
    password_kdf: PasswordKdf
    http_client: httpx2.AsyncClient
    provider_runtime: ProviderRuntime
    apple_grant_cipher: AppleGrantCipher | None
    webauthn_policy: WebAuthnPolicy | None
    _resources: AsyncExitStack

    async def aclose(self) -> None:
        """Release all Auth-owned resources in reverse construction order."""
        await self._resources.aclose()


async def create_auth_runtime(
    *,
    settings: AuthSettings,
    database_runtime: DatabaseRuntime,
    release_sha: str,
    telemetry: AuthTelemetry | None = None,
) -> AuthRuntime:
    """Construct and warm the process-scoped Auth runtime with rollback-safe ownership."""
    resources = AsyncExitStack()
    try:
        password_kdf = PasswordKdf(
            pepper_ring=settings.password_pepper_bytes,
            current_pepper_key_id=settings.password_current_pepper_key_id,
            max_concurrency=settings.kdf_max_concurrency,
            max_queue_depth=settings.kdf_max_queue_depth,
            queue_timeout_seconds=settings.kdf_queue_timeout_seconds,
            telemetry=telemetry,
        )
        resources.push_async_callback(password_kdf.aclose)
        await password_kdf.start()

        http_client = httpx2.AsyncClient(
            base_url=settings.hibp_base_url,
            timeout=httpx2.Timeout(settings.hibp_timeout_seconds),
            limits=httpx2.Limits(
                max_connections=settings.hibp_max_connections,
                max_keepalive_connections=settings.hibp_max_connections,
            ),
            follow_redirects=False,
            trust_env=False,
            headers={
                "Accept": "text/plain",
                "User-Agent": f"DANTE/{release_sha}",
            },
        )
        resources.push_async_callback(http_client.aclose)

        provider_runtime = ProviderRuntime(
            settings=settings.provider,
            release_sha=release_sha,
        )
        resources.push_async_callback(provider_runtime.aclose)

        apple = settings.provider.apple
        apple_grant_cipher = (
            AppleGrantCipher(
                key_ring=apple.grant_encryption_key_bytes,
                current_key_id=apple.grant_encryption_current_key_id,
            )
            if apple.grant_encryption_current_key_id is not None
            else None
        )
        webauthn_policy = (
            WebAuthnPolicy.from_settings(settings.provider.webauthn)
            if settings.provider.webauthn.enabled
            else None
        )

        breach_checker = HibpPasswordChecker(
            client=http_client,
            max_response_bytes=settings.hibp_max_response_bytes,
        )
        signin_limiter = SigninAttemptLimiter(
            capacity=settings.signin_rate_capacity,
            window_seconds=settings.signin_rate_window_seconds,
            max_keys=settings.signin_rate_max_keys,
        )
        service = AuthService(
            session_factory=database_runtime.session_factory,
            settings=settings,
            password_kdf=password_kdf,
            breach_checker=breach_checker,
            signin_limiter=signin_limiter,
            telemetry=telemetry,
        )
        return AuthRuntime(
            service=service,
            password_kdf=password_kdf,
            http_client=http_client,
            provider_runtime=provider_runtime,
            apple_grant_cipher=apple_grant_cipher,
            webauthn_policy=webauthn_policy,
            _resources=resources,
        )
    except BaseException:
        await resources.aclose()
        raise
