from __future__ import annotations

import re
import subprocess
from pathlib import Path

EXPECTED_HEAD = "81a56c9a9c390b36198cf3b444f1652db2ee9124"
EXPECTED_BRANCH = "feature/access-auth"
EXPECTED_HASHES = {
    "apps/backend/src/dante/platform/config/auth.py": "58ea175f110fb9a3c2b5f0fdd94a72f3da63f079",
    "apps/backend/src/dante/auth/lifecycle.py": "2220a99235f494b490aace220808358dbb6d508b",
    "apps/backend/src/dante/auth/authenticator_lifecycle.py": "cabcbe07943d0cd91c806a81ea30c89121ae253c",
    "apps/backend/src/dante/auth/lifecycle_runtime.py": "d155353663c65058aa81c4ec24ce0b67f4791e8a",
    "apps/backend/src/dante/bootstrap/lifespan.py": "451560b9a587ef05e0625ed76cf3a55731fb2624",
    "apps/backend/pyproject.toml": "76e9e78596b20d0b6350fa2084afd4b0e1ad0b0e",
}


def run(*args: str) -> str:
    return subprocess.check_output(args, text=True).strip()


def replace_exact(text: str, old: str, new: str, *, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"{label}: expected exactly one anchor, found {count}")
    return text.replace(old, new, 1)


def replace_regex(text: str, pattern: str, repl: str, *, label: str) -> str:
    result, count = re.subn(pattern, repl, text, count=1, flags=re.MULTILINE | re.DOTALL)
    if count != 1:
        raise RuntimeError(f"{label}: expected exactly one regex anchor, found {count}")
    return result


def validate_repo(root: Path) -> None:
    branch = run("git", "-C", str(root), "branch", "--show-current")
    if branch != EXPECTED_BRANCH:
        raise RuntimeError(f"expected branch {EXPECTED_BRANCH}, found {branch!r}")
    head = run("git", "-C", str(root), "rev-parse", "HEAD")
    if head != EXPECTED_HEAD:
        raise RuntimeError(f"expected HEAD {EXPECTED_HEAD}, found {head}")
    status = run("git", "-C", str(root), "status", "--porcelain")
    if status:
        raise RuntimeError("worktree must be clean before materialization")
    for relative, expected in EXPECTED_HASHES.items():
        actual = run("git", "-C", str(root), "hash-object", relative)
        if actual != expected:
            raise RuntimeError(f"unexpected blob for {relative}: {actual} != {expected}")


def patch_auth_settings(path: Path) -> None:
    text = path.read_text()
    text = replace_exact(
        text,
        '''class SmtpSecurity(StrEnum):\n    """Supported SMTP transport-security modes."""\n\n    PLAIN = "plain"\n    STARTTLS = "starttls"\n    TLS = "tls"\n''',
        '''class SmtpSecurity(StrEnum):\n    """Supported SMTP transport-security modes."""\n\n    PLAIN = "plain"\n    STARTTLS = "starttls"\n    TLS = "tls"\n\n\nclass EmailTransport(StrEnum):\n    """Last-mile email transport behind the durable PostgreSQL outbox."""\n\n    SMTP = "smtp"\n    SES = "ses"\n''',
        label="auth-settings transport enum",
    )
    text = replace_exact(
        text,
        '''    smtp_timeout_seconds: PositiveFloat = 5.0\n    email_queue_capacity: PositiveInt = 256\n    email_worker_count: PositiveInt = 2\n    email_shutdown_drain_seconds: PositiveFloat = 10.0\n''',
        '''    smtp_timeout_seconds: PositiveFloat = 5.0\n    email_queue_capacity: PositiveInt = 256\n    email_worker_count: PositiveInt = 2\n    email_shutdown_drain_seconds: PositiveFloat = 10.0\n\n    email_platform_enabled: bool = False\n    email_transport: EmailTransport = EmailTransport.SMTP\n    email_from_address: str | None = None\n    email_payload_current_key_id: str | None = None\n    email_payload_keys: dict[str, SecretStr] = Field(default_factory=dict)\n    email_attempt_limit: PositiveInt = 3\n    email_claim_batch_size: PositiveInt = 16\n    email_claim_lease_seconds: PositiveFloat = 30.0\n    email_poll_interval_seconds: PositiveFloat = 0.5\n    email_retry_base_seconds: PositiveFloat = 1.0\n    email_retry_max_seconds: PositiveFloat = 30.0\n    email_provider_connect_timeout_seconds: PositiveFloat = 2.0\n    email_provider_read_timeout_seconds: PositiveFloat = 5.0\n    ses_region: str | None = None\n    ses_configuration_set: str | None = None\n''',
        label="auth-settings email fields",
    )
    text = replace_exact(
        text,
        '''    @field_validator("smtp_from_address")\n    @classmethod\n    def validate_smtp_from_address(cls, value: str) -> str:\n        """Keep the configured envelope/header sender injection-safe."""\n        return _smtp_mailbox(value)\n''',
        '''    @field_validator("smtp_from_address")\n    @classmethod\n    def validate_smtp_from_address(cls, value: str) -> str:\n        """Keep the configured envelope/header sender injection-safe."""\n        return _smtp_mailbox(value)\n\n    @field_validator("email_from_address")\n    @classmethod\n    def validate_email_from_address(cls, value: str | None) -> str | None:\n        """Validate the provider-neutral From mailbox when explicitly configured."""\n        return None if value is None else _smtp_mailbox(value)\n\n    @field_validator("email_payload_current_key_id", "ses_region", "ses_configuration_set")\n    @classmethod\n    def validate_optional_email_identity(cls, value: str | None) -> str | None:\n        if value is None:\n            return None\n        return _trimmed_identity(value, name="email platform identity")\n''',
        label="auth-settings email validators",
    )
    text = replace_exact(
        text,
        '''        apple_grant_bytes = self.provider.apple.grant_encryption_key_bytes\n\n        if len(set(pepper_bytes.values())) != len(pepper_bytes):\n''',
        '''        apple_grant_bytes = self.provider.apple.grant_encryption_key_bytes\n        email_payload_bytes = (\n            self._decode_ring(self.email_payload_keys, name="email_payload_keys")\n            if self.email_payload_keys\n            else {}\n        )\n\n        if self.email_platform_enabled:\n            if not email_payload_bytes:\n                raise ValueError("email_payload_keys must be configured when Email Platform is enabled")\n            if self.email_payload_current_key_id not in email_payload_bytes:\n                raise ValueError(\n                    "email_payload_current_key_id is absent from email_payload_keys"\n                )\n            if self.email_transport is EmailTransport.SES and self.ses_region is None:\n                raise ValueError("SES email transport requires ses_region")\n\n        if len(set(pepper_bytes.values())) != len(pepper_bytes):\n''',
        label="auth-settings email ring validation",
    )
    text = replace_exact(
        text,
        '''            {csrf_bytes},\n            set(apple_grant_bytes.values()),\n        ]\n''',
        '''            {csrf_bytes},\n            set(apple_grant_bytes.values()),\n            set(email_payload_bytes.values()),\n        ]\n''',
        label="auth-settings purpose separation",
    )
    text = replace_exact(
        text,
        '''    @property\n    def csrf_key_bytes(self) -> bytes:\n        """Return the validated decoded CSRF derivation key."""\n        return _decode_canonical_secret(self.csrf_key.get_secret_value(), name="csrf_key")\n''',
        '''    @property\n    def email_payload_key_bytes(self) -> dict[str, bytes]:\n        """Return the validated dedicated Email Platform AEAD/HMAC key ring."""\n        return self._decode_ring(self.email_payload_keys, name="email_payload_keys")\n\n    @property\n    def email_sender_address(self) -> str:\n        """Return the provider-neutral visible From mailbox."""\n        return self.email_from_address or self.smtp_from_address\n\n    @property\n    def csrf_key_bytes(self) -> bytes:\n        """Return the validated decoded CSRF derivation key."""\n        return _decode_canonical_secret(self.csrf_key.get_secret_value(), name="csrf_key")\n''',
        label="auth-settings email properties",
    )
    path.write_text(text)


def patch_lifecycle(path: Path) -> None:
    text = path.read_text()
    text = replace_exact(
        text,
        "from collections import OrderedDict\n",
        "from collections import OrderedDict\nfrom collections.abc import Callable\n",
        label="lifecycle callable import",
    )
    text = replace_exact(
        text,
        "from dante.auth.email import EmailNormalizationError, NormalizedEmail, normalize_email\n",
        "from dante.auth.email import EmailNormalizationError, NormalizedEmail, normalize_email\nfrom dante.auth.email_contracts import EmailIntentConflictError\nfrom dante.auth.email_outbox import DurableEmailOutbox\n",
        label="lifecycle durable imports",
    )
    old_ctor = '''        otp_codec: SignupOtpCodec,\n        email_delivery: EmailDeliveryPort,\n        limiters: LifecycleLimiters,\n    ) -> None:\n'''
    new_ctor = '''        otp_codec: SignupOtpCodec,\n        email_delivery: EmailDeliveryPort,\n        limiters: LifecycleLimiters,\n        email_outbox: DurableEmailOutbox | None = None,\n        email_wake: Callable[[], None] | None = None,\n    ) -> None:\n'''
    text = replace_exact(text, old_ctor, new_ctor, label="lifecycle constructor signature")
    text = replace_exact(
        text,
        '''        self._otp_codec = otp_codec\n        self._email_delivery = email_delivery\n        self._limiters = limiters\n''',
        '''        self._otp_codec = otp_codec\n        self._email_delivery = email_delivery\n        self._email_outbox = email_outbox\n        self._email_wake = email_wake\n        self._limiters = limiters\n''',
        label="lifecycle constructor fields",
    )
    text = replace_exact(
        text,
        '''        await self._insert_signup_challenge(row)\n        await self._enqueue(\n            SignupVerificationEmail(\n                to_address=normalized_email.address,\n                code=otp.code,\n                expires_minutes=max(1, math.ceil(self._settings.signup_otp_lifetime_seconds / 60)),\n            )\n        )\n''',
        '''        email_command = SignupVerificationEmail(\n            to_address=normalized_email.address,\n            code=otp.code,\n            expires_minutes=max(1, math.ceil(self._settings.signup_otp_lifetime_seconds / 60)),\n        )\n        staged = await self._insert_signup_challenge(row, email_command=email_command)\n        await self._after_email_commit(email_command, staged=staged)\n''',
        label="lifecycle signup atomic stage",
    )
    text = replace_exact(
        text,
        '''        verification_expires_at = min(\n            snapshot.signup_expires_at,\n            now + timedelta(seconds=self._settings.signup_otp_lifetime_seconds),\n        )\n        try:\n''',
        '''        verification_expires_at = min(\n            snapshot.signup_expires_at,\n            now + timedelta(seconds=self._settings.signup_otp_lifetime_seconds),\n        )\n        email_command = SignupVerificationEmail(\n            to_address=snapshot.email_address,\n            code=otp.code,\n            expires_minutes=max(1, math.ceil(self._settings.signup_otp_lifetime_seconds / 60)),\n        )\n        staged = False\n        try:\n''',
        label="lifecycle resend command",
    )
    text = replace_exact(
        text,
        '''                locked.verification_expires_at = verification_expires_at\n                locked.failed_verification_attempts = 0\n        except VerificationInvalidOrExpiredError, SignupResendCooldownError:\n''',
        '''                locked.verification_expires_at = verification_expires_at\n                locked.failed_verification_attempts = 0\n                staged = await self._stage_email_intent(\n                    database_session,\n                    command=email_command,\n                    operation_scope="auth.signup_verification",\n                    idempotency_key=f"{signup_ref}:{now.isoformat()}",\n                    expires_at=verification_expires_at,\n                    supersession_key=f"signup:{signup_ref}",\n                )\n        except VerificationInvalidOrExpiredError, SignupResendCooldownError:\n''',
        label="lifecycle resend tx stage",
    )
    text = replace_exact(
        text,
        '''        await self._enqueue(\n            SignupVerificationEmail(\n                to_address=snapshot.email_address,\n                code=otp.code,\n                expires_minutes=max(1, math.ceil(self._settings.signup_otp_lifetime_seconds / 60)),\n            )\n        )\n''',
        '''        await self._after_email_commit(email_command, staged=staged)\n''',
        label="lifecycle resend post commit",
    )
    text = replace_exact(
        text,
        '''        recovery_ref = uuid7()\n        proof = issue_recovery_proof()\n        committed = await self._persist_recovery_challenge(\n            snapshot=snapshot,\n            password_recovery_ref=recovery_ref,\n            secret_verifier=proof.verifier,\n        )\n''',
        '''        recovery_ref = uuid7()\n        proof = issue_recovery_proof()\n        email_command = PasswordRecoveryEmail(\n            to_address=snapshot.email_address,\n            password_recovery_ref=recovery_ref,\n            secret=proof.secret,\n        )\n        committed, staged = await self._persist_recovery_challenge(\n            snapshot=snapshot,\n            password_recovery_ref=recovery_ref,\n            secret_verifier=proof.verifier,\n            email_command=email_command,\n        )\n''',
        label="lifecycle recovery command",
    )
    text = replace_exact(
        text,
        '''        await self._enqueue(\n            PasswordRecoveryEmail(\n                to_address=snapshot.email_address,\n                password_recovery_ref=recovery_ref,\n                secret=proof.secret,\n            )\n        )\n''',
        '''        await self._after_email_commit(email_command, staged=staged)\n''',
        label="lifecycle recovery post commit",
    )
    text = replace_exact(
        text,
        '''        ambiguous_commit = False\n        mutation_at: datetime | None = None\n        database_session = self._session_factory()\n''',
        '''        ambiguous_commit = False\n        mutation_at: datetime | None = None\n        notification = PasswordResetNotificationEmail(to_address=snapshot.email_address)\n        notification_staged = False\n        database_session = self._session_factory()\n''',
        label="lifecycle reset notification setup",
    )
    text = replace_exact(
        text,
        '''            await database_session.execute(\n                update(AuthSessionRow)\n                .where(\n                    AuthSessionRow.account_ref == snapshot.account_ref,\n                    AuthSessionRow.revoked_at.is_(None),\n                )\n                .values(\n                    revoked_at=mutation_at,\n                    revocation_reason_code="password_reset",\n                )\n            )\n            try:\n''',
        '''            await database_session.execute(\n                update(AuthSessionRow)\n                .where(\n                    AuthSessionRow.account_ref == snapshot.account_ref,\n                    AuthSessionRow.revoked_at.is_(None),\n                )\n                .values(\n                    revoked_at=mutation_at,\n                    revocation_reason_code="password_reset",\n                )\n            )\n            notification_staged = await self._stage_email_intent(\n                database_session,\n                command=notification,\n                operation_scope="auth.password_reset_notification",\n                idempotency_key=str(password_recovery_ref),\n                expires_at=mutation_at + timedelta(days=1),\n            )\n            try:\n''',
        label="lifecycle reset atomic notification",
    )
    text = replace_exact(
        text,
        '''        try:\n            await self._email_delivery.enqueue(\n                PasswordResetNotificationEmail(to_address=snapshot.email_address)\n            )\n        except EmailDispatchCapacityError:\n            _LOGGER.warning("auth.password_reset_notification_queue_unavailable")\n''',
        '''        await self._after_email_commit(notification, staged=notification_staged)\n''',
        label="lifecycle reset post commit",
    )
    text = replace_exact(
        text,
        '''    async def _insert_signup_challenge(self, row: PasswordSignupChallengeRow) -> None:\n        await self._cleanup_expired_challenges(datetime.now(UTC))\n        ambiguous_commit = False\n''',
        '''    async def _stage_email_intent(\n        self,\n        database_session: AsyncSession,\n        *,\n        command: EmailCommand,\n        operation_scope: str,\n        idempotency_key: str,\n        expires_at: datetime,\n        supersession_key: str | None = None,\n    ) -> bool:\n        if self._email_outbox is None or isinstance(command, NoopEmail):\n            return False\n        try:\n            await self._email_outbox.stage(\n                database_session,\n                command=command,\n                operation_scope=operation_scope,\n                idempotency_key=idempotency_key,\n                expires_at=expires_at,\n                supersession_key=supersession_key,\n            )\n        except EmailIntentConflictError as exc:\n            raise AuthIntegrityError("email intent idempotency conflict") from exc\n        return True\n\n    async def _after_email_commit(self, command: EmailCommand, *, staged: bool) -> None:\n        if staged:\n            if self._email_wake is not None:\n                self._email_wake()\n            return\n        if self._email_outbox is not None and isinstance(command, NoopEmail):\n            return\n        await self._enqueue(command)\n\n    async def _insert_signup_challenge(\n        self,\n        row: PasswordSignupChallengeRow,\n        *,\n        email_command: SignupVerificationEmail,\n    ) -> bool:\n        await self._cleanup_expired_challenges(datetime.now(UTC))\n        ambiguous_commit = False\n        staged = False\n''',
        label="lifecycle durable helper insertion",
    )
    text = replace_exact(
        text,
        '''            await database_session.begin()\n            database_session.add(row)\n            try:\n''',
        '''            await database_session.begin()\n            database_session.add(row)\n            staged = await self._stage_email_intent(\n                database_session,\n                command=email_command,\n                operation_scope="auth.signup_verification",\n                idempotency_key=f"{row.signup_ref}:{row.verification_issued_at.isoformat()}",\n                expires_at=row.verification_expires_at,\n                supersession_key=f"signup:{row.signup_ref}",\n            )\n            try:\n''',
        label="lifecycle signup insert stage",
    )
    text = replace_exact(
        text,
        '''        if not ambiguous_commit:\n            return\n\n        persisted = await self._read_signup_challenge(row.signup_ref)\n''',
        '''        if not ambiguous_commit:\n            return staged\n\n        persisted = await self._read_signup_challenge(row.signup_ref)\n''',
        label="lifecycle signup insert return",
    )
    text = replace_exact(
        text,
        '''        ):\n            raise AuthIntegrityError("ambiguous signup challenge reconciliation mismatched state")\n\n    async def _persist_recovery_challenge(\n''',
        '''        ):\n            raise AuthIntegrityError("ambiguous signup challenge reconciliation mismatched state")\n        return staged\n\n    async def _persist_recovery_challenge(\n''',
        label="lifecycle signup reconcile return",
    )
    text = replace_exact(
        text,
        '''        password_recovery_ref: UUID,\n        secret_verifier: bytes,\n    ) -> bool:\n''',
        '''        password_recovery_ref: UUID,\n        secret_verifier: bytes,\n        email_command: PasswordRecoveryEmail,\n    ) -> tuple[bool, bool]:\n''',
        label="lifecycle recovery helper signature",
    )
    text = replace_exact(
        text,
        '''        ambiguous_commit = False\n        issued_at: datetime | None = None\n        expires_at: datetime | None = None\n        database_session = self._session_factory()\n''',
        '''        ambiguous_commit = False\n        issued_at: datetime | None = None\n        expires_at: datetime | None = None\n        staged = False\n        database_session = self._session_factory()\n''',
        label="lifecycle recovery staged flag",
    )
    text = replace_exact(
        text,
        '''            if current is None:\n                await database_session.rollback()\n                return False\n''',
        '''            if current is None:\n                await database_session.rollback()\n                return False, False\n''',
        label="lifecycle recovery false return",
    )
    text = replace_exact(
        text,
        '''            database_session.add(\n                PasswordRecoveryChallengeRow(\n                    password_recovery_ref=password_recovery_ref,\n                    account_ref=snapshot.account_ref,\n                    email_identity_ref=snapshot.email_identity_ref,\n                    secret_verifier=secret_verifier,\n                    issued_at=issued_at,\n                    expires_at=expires_at,\n                )\n            )\n            try:\n''',
        '''            database_session.add(\n                PasswordRecoveryChallengeRow(\n                    password_recovery_ref=password_recovery_ref,\n                    account_ref=snapshot.account_ref,\n                    email_identity_ref=snapshot.email_identity_ref,\n                    secret_verifier=secret_verifier,\n                    issued_at=issued_at,\n                    expires_at=expires_at,\n                )\n            )\n            staged = await self._stage_email_intent(\n                database_session,\n                command=email_command,\n                operation_scope="auth.password_recovery",\n                idempotency_key=str(password_recovery_ref),\n                expires_at=expires_at,\n                supersession_key=f"password-recovery:{snapshot.account_ref}",\n            )\n            try:\n''',
        label="lifecycle recovery atomic stage",
    )
    text = replace_exact(
        text,
        '''        if not ambiguous_commit:\n            return True\n\n        try:\n''',
        '''        if not ambiguous_commit:\n            return True, staged\n\n        try:\n''',
        label="lifecycle recovery normal return",
    )
    text = replace_exact(
        text,
        '''        return True\n\n    async def _resolve_signup_collision''',
        '''        return True, staged\n\n    async def _resolve_signup_collision''',
        label="lifecycle recovery ambiguous return",
    )
    path.write_text(text)


def patch_multi_lifecycle(path: Path) -> None:
    text = path.read_text()
    text = replace_exact(
        text,
        "from dante.auth.email_delivery import (\n",
        "from dante.auth.email_outbox import DurableEmailOutbox\nfrom dante.auth.email_delivery import (\n",
        label="multi durable import",
    )
    text = replace_exact(
        text,
        '''        otp_codec: SignupOtpCodec,\n        email_delivery: EmailDeliveryPort,\n        limiters: LifecycleLimiters,\n    ) -> None:\n''',
        '''        otp_codec: SignupOtpCodec,\n        email_delivery: EmailDeliveryPort,\n        limiters: LifecycleLimiters,\n        email_outbox: DurableEmailOutbox | None = None,\n        email_wake: Callable[[], None] | None = None,\n    ) -> None:\n''',
        label="multi constructor signature",
    )
    text = replace_exact(
        text,
        '''            otp_codec=otp_codec,\n            email_delivery=email_delivery,\n            limiters=limiters,\n        )\n''',
        '''            otp_codec=otp_codec,\n            email_delivery=email_delivery,\n            limiters=limiters,\n            email_outbox=email_outbox,\n            email_wake=email_wake,\n        )\n''',
        label="multi super durable args",
    )
    text = replace_exact(
        text,
        '''        recovery_ref = uuid7()\n        proof = issue_recovery_proof()\n        committed = await self._persist_passwordless_recovery_challenge(\n            channel=channel,\n            password_recovery_ref=recovery_ref,\n            secret_verifier=proof.verifier,\n        )\n''',
        '''        recovery_ref = uuid7()\n        proof = issue_recovery_proof()\n        email_command = PasswordRecoveryEmail(\n            to_address=channel.email_address,\n            password_recovery_ref=recovery_ref,\n            secret=proof.secret,\n        )\n        committed, staged = await self._persist_passwordless_recovery_challenge(\n            channel=channel,\n            password_recovery_ref=recovery_ref,\n            secret_verifier=proof.verifier,\n            email_command=email_command,\n        )\n''',
        label="multi recovery command",
    )
    text = replace_exact(
        text,
        '''        await self._enqueue(\n            PasswordRecoveryEmail(\n                to_address=channel.email_address,\n                password_recovery_ref=recovery_ref,\n                secret=proof.secret,\n            )\n        )\n''',
        '''        await self._after_email_commit(email_command, staged=staged)\n''',
        label="multi recovery post commit",
    )
    text = replace_exact(
        text,
        '''        mutation_at: datetime | None = None\n        ambiguous_commit = False\n        database_session = self._session_factory()\n''',
        '''        mutation_at: datetime | None = None\n        ambiguous_commit = False\n        notification = PasswordResetNotificationEmail(to_address=snapshot.email_address)\n        notification_staged = False\n        database_session = self._session_factory()\n''',
        label="multi reset notification setup",
    )
    text = replace_exact(
        text,
        '''            await database_session.execute(\n                update(AuthSessionRow)\n                .where(\n                    AuthSessionRow.account_ref == snapshot.account_ref,\n                    AuthSessionRow.revoked_at.is_(None),\n                )\n                .values(\n                    revoked_at=mutation_at,\n                    revocation_reason_code="password_reset",\n                )\n            )\n            try:\n''',
        '''            await database_session.execute(\n                update(AuthSessionRow)\n                .where(\n                    AuthSessionRow.account_ref == snapshot.account_ref,\n                    AuthSessionRow.revoked_at.is_(None),\n                )\n                .values(\n                    revoked_at=mutation_at,\n                    revocation_reason_code="password_reset",\n                )\n            )\n            notification_staged = await self._stage_email_intent(\n                database_session,\n                command=notification,\n                operation_scope="auth.password_reset_notification",\n                idempotency_key=str(password_recovery_ref),\n                expires_at=mutation_at + timedelta(days=1),\n            )\n            try:\n''',
        label="multi reset atomic notification",
    )
    text = replace_exact(
        text,
        '''        try:\n            await self._email_delivery.enqueue(\n                PasswordResetNotificationEmail(to_address=snapshot.email_address)\n            )\n        except EmailDispatchCapacityError:\n            _LOGGER.warning("auth.password_reset_notification_queue_unavailable")\n''',
        '''        await self._after_email_commit(notification, staged=notification_staged)\n''',
        label="multi reset post commit",
    )
    text = replace_exact(
        text,
        '''        password_recovery_ref: UUID,\n        secret_verifier: bytes,\n    ) -> bool:\n''',
        '''        password_recovery_ref: UUID,\n        secret_verifier: bytes,\n        email_command: PasswordRecoveryEmail,\n    ) -> tuple[bool, bool]:\n''',
        label="multi recovery helper signature",
    )
    text = replace_exact(
        text,
        '''        expires_at: datetime | None = None\n        ambiguous_commit = False\n        database_session = self._session_factory()\n''',
        '''        expires_at: datetime | None = None\n        ambiguous_commit = False\n        staged = False\n        database_session = self._session_factory()\n''',
        label="multi recovery staged flag",
    )
    text = replace_exact(
        text,
        '''            if current is None or current.address != channel.email_address:\n                await database_session.rollback()\n                return False\n''',
        '''            if current is None or current.address != channel.email_address:\n                await database_session.rollback()\n                return False, False\n''',
        label="multi recovery false return",
    )
    text = replace_exact(
        text,
        '''            database_session.add(\n                PasswordRecoveryChallengeRow(\n                    password_recovery_ref=password_recovery_ref,\n                    account_ref=channel.account_ref,\n                    email_identity_ref=channel.email_identity_ref,\n                    secret_verifier=secret_verifier,\n                    issued_at=issued_at,\n                    expires_at=expires_at,\n                )\n            )\n            try:\n''',
        '''            database_session.add(\n                PasswordRecoveryChallengeRow(\n                    password_recovery_ref=password_recovery_ref,\n                    account_ref=channel.account_ref,\n                    email_identity_ref=channel.email_identity_ref,\n                    secret_verifier=secret_verifier,\n                    issued_at=issued_at,\n                    expires_at=expires_at,\n                )\n            )\n            staged = await self._stage_email_intent(\n                database_session,\n                command=email_command,\n                operation_scope="auth.password_recovery",\n                idempotency_key=str(password_recovery_ref),\n                expires_at=expires_at,\n                supersession_key=f"password-recovery:{channel.account_ref}",\n            )\n            try:\n''',
        label="multi recovery atomic stage",
    )
    text = replace_exact(
        text,
        '''        if not ambiguous_commit:\n            return True\n        try:\n''',
        '''        if not ambiguous_commit:\n            return True, staged\n        try:\n''',
        label="multi recovery normal return",
    )
    text = replace_exact(
        text,
        '''        ):\n            return True\n        if persisted is None:\n''',
        '''        ):\n            return True, staged\n        if persisted is None:\n''',
        label="multi recovery ambiguous return",
    )
    path.write_text(text)


def patch_lifecycle_runtime(path: Path) -> None:
    text = path.read_text()
    text = replace_exact(
        text,
        "from dante.auth.email_delivery import SmtpEmailDispatcher\n",
        "from dante.auth.email_delivery import SmtpEmailDispatcher\nfrom dante.auth.email_runtime import EmailPlatformRuntime\n",
        label="runtime durable import",
    )
    text = replace_exact(
        text,
        '''    service: MultiAuthenticatorLifecycleService\n    email_dispatcher: SmtpEmailDispatcher\n\n    async def aclose(self) -> None:\n        """Drain admitted email work before shared M3 Auth resources are disposed."""\n        await self.email_dispatcher.aclose()\n''',
        '''    service: MultiAuthenticatorLifecycleService\n    email_dispatcher: SmtpEmailDispatcher\n    email_platform: EmailPlatformRuntime | None\n\n    async def aclose(self) -> None:\n        """Drain only the legacy dispatcher; durable workers are owned by bootstrap."""\n        await self.email_dispatcher.aclose()\n''',
        label="runtime dataclass fields",
    )
    text = replace_exact(
        text,
        '''    database_runtime: DatabaseRuntime,\n    auth_runtime: AuthRuntime,\n) -> AuthLifecycleRuntime:\n''',
        '''    database_runtime: DatabaseRuntime,\n    auth_runtime: AuthRuntime,\n    email_platform: EmailPlatformRuntime | None = None,\n) -> AuthLifecycleRuntime:\n''',
        label="runtime factory signature",
    )
    text = replace_exact(
        text,
        '''            otp_codec=otp_codec,\n            email_delivery=email_dispatcher,\n            limiters=limiters,\n        )\n        return AuthLifecycleRuntime(\n            service=service,\n            email_dispatcher=email_dispatcher,\n        )\n''',
        '''            otp_codec=otp_codec,\n            email_delivery=email_dispatcher,\n            limiters=limiters,\n            email_outbox=(email_platform.outbox if email_platform is not None else None),\n            email_wake=(email_platform.wake if email_platform is not None else None),\n        )\n        return AuthLifecycleRuntime(\n            service=service,\n            email_dispatcher=email_dispatcher,\n            email_platform=email_platform,\n        )\n''',
        label="runtime service durable injection",
    )
    path.write_text(text)


def patch_lifespan(path: Path) -> None:
    text = path.read_text()
    text = replace_exact(
        text,
        "from dante.auth.lifecycle_runtime import create_auth_lifecycle_runtime\n",
        "from dante.auth.email_runtime import create_email_platform_runtime\nfrom dante.auth.lifecycle_runtime import create_auth_lifecycle_runtime\n",
        label="lifespan email runtime import",
    )
    text = replace_exact(
        text,
        '''        auth_lifecycle_runtime = await create_auth_lifecycle_runtime(\n            settings=settings.auth,\n            database_runtime=database_runtime,\n            auth_runtime=auth_runtime,\n        )\n''',
        '''        email_platform_runtime = (\n            await create_email_platform_runtime(\n                settings=settings.auth,\n                database_runtime=database_runtime,\n            )\n            if settings.auth.email_platform_enabled\n            else None\n        )\n        if email_platform_runtime is not None:\n            stack.push_async_callback(email_platform_runtime.aclose)\n            app.state.email_platform_runtime = email_platform_runtime\n\n        auth_lifecycle_runtime = await create_auth_lifecycle_runtime(\n            settings=settings.auth,\n            database_runtime=database_runtime,\n            auth_runtime=auth_runtime,\n            email_platform=email_platform_runtime,\n        )\n''',
        label="lifespan runtime creation",
    )
    path.write_text(text)


def patch_pyproject(path: Path) -> None:
    text = path.read_text()
    text = replace_exact(
        text,
        '''    "cryptography==50.0.1",\n''',
        '''    "cryptography==50.0.1",\n    "boto3>=1.40,<2",\n    "botocore>=1.40,<2",\n''',
        label="pyproject aws dependencies",
    )
    path.write_text(text)


def main() -> None:
    script = Path(__file__).resolve()
    root = script.parents[3]
    validate_repo(root)

    patch_auth_settings(root / "apps/backend/src/dante/platform/config/auth.py")
    patch_lifecycle(root / "apps/backend/src/dante/auth/lifecycle.py")
    patch_multi_lifecycle(root / "apps/backend/src/dante/auth/authenticator_lifecycle.py")
    patch_lifecycle_runtime(root / "apps/backend/src/dante/auth/lifecycle_runtime.py")
    patch_lifespan(root / "apps/backend/src/dante/bootstrap/lifespan.py")
    patch_pyproject(root / "apps/backend/pyproject.toml")

    print("M05 Email Platform Phase A materialized successfully.")
    print("No commit was created. Review git diff before any commit.")


if __name__ == "__main__":
    main()
