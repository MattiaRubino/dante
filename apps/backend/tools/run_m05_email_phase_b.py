from __future__ import annotations

import subprocess
from pathlib import Path

EXPECTED_BRANCH = "feature/access-auth"
EXPECTED_HASHES = {
    "apps/backend/src/dante/auth/provider_flow.py": "3b0350a50cad9de7fadfdc1ddddeb417c7c1c327",
    "apps/backend/src/dante/auth/apple_flow.py": "7bf335d7463b124111db4cc03f3e04104e573373",
    "apps/backend/src/dante/auth/provider_flow_runtime.py": "73b10c740a2fdb183181a38ddf3d673866f7a47b",
}


def run(*args: str) -> str:
    return subprocess.check_output(args, text=True).strip()


def replace_exact(text: str, old: str, new: str, *, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"{label}: expected exactly one anchor, found {count}")
    return text.replace(old, new, 1)


def validate_repo(root: Path) -> None:
    branch = run("git", "-C", str(root), "branch", "--show-current")
    if branch != EXPECTED_BRANCH:
        raise RuntimeError(f"expected branch {EXPECTED_BRANCH}, found {branch!r}")
    for relative, expected in EXPECTED_HASHES.items():
        actual = run("git", "-C", str(root), "hash-object", relative)
        if actual != expected:
            raise RuntimeError(f"unexpected blob for {relative}: {actual} != {expected}")


def patch_google(text: str) -> str:
    text = replace_exact(
        text,
        "from contextlib import suppress\n",
        "from collections.abc import Callable\nfrom contextlib import suppress\n",
        label="google callable import",
    )
    text = replace_exact(
        text,
        "from dante.auth.email import EmailNormalizationError, NormalizedEmail, normalize_email\n",
        "from dante.auth.email import EmailNormalizationError, NormalizedEmail, normalize_email\n"
        "from dante.auth.email_contracts import EmailIntentConflictError\n"
        "from dante.auth.email_outbox import DurableEmailOutbox\n",
        label="google durable imports",
    )
    text = replace_exact(
        text,
        '''        otp_codec: ProviderEnrollmentOtpCodec,\n        email_delivery: EmailDeliveryPort,\n        limiters: ProviderFlowLimiters,\n    ) -> None:\n''',
        '''        otp_codec: ProviderEnrollmentOtpCodec,\n        email_delivery: EmailDeliveryPort,\n        limiters: ProviderFlowLimiters,\n        email_outbox: DurableEmailOutbox | None = None,\n        email_wake: Callable[[], None] | None = None,\n    ) -> None:\n''',
        label="google constructor signature",
    )
    text = replace_exact(
        text,
        '''        self._otp_codec = otp_codec\n        self._email_delivery = email_delivery\n        self._limiters = limiters\n''',
        '''        self._otp_codec = otp_codec\n        self._email_delivery = email_delivery\n        self._email_outbox = email_outbox\n        self._email_wake = email_wake\n        self._limiters = limiters\n''',
        label="google constructor fields",
    )

    text = replace_exact(
        text,
        '''        expires_at: datetime | None = None\n        verification_expires_at: datetime | None = None\n\n        database_session = self._session_factory()\n''',
        '''        expires_at: datetime | None = None\n        verification_expires_at: datetime | None = None\n        email_command: ProviderEnrollmentVerificationEmail | None = None\n        staged = False\n\n        database_session = self._session_factory()\n''',
        label="google set-email staged state",
    )
    text = replace_exact(
        text,
        '''            challenge.verification_expires_at = verification_expires_at\n            challenge.failed_verification_attempts = 0\n            challenge.updated_at = now\n            await database_session.commit()\n''',
        '''            challenge.verification_expires_at = verification_expires_at\n            challenge.failed_verification_attempts = 0\n            challenge.updated_at = now\n            email_command = self._provider_email_command(\n                email_address=normalized.address,\n                code=otp.code,\n                expires_at=verification_expires_at,\n                now=now,\n            )\n            staged = await self._stage_provider_email(\n                database_session,\n                command=email_command,\n                idempotency_key=f"{external_signup_ref}:{now.isoformat()}",\n                expires_at=verification_expires_at,\n                supersession_key=f"provider-enrollment:{external_signup_ref}",\n            )\n            await database_session.commit()\n''',
        label="google set-email atomic intent",
    )
    text = replace_exact(
        text,
        '''        if expires_at is None or verification_expires_at is None:\n            raise AuthIntegrityError("provider enrollment email update lost challenge timestamps")\n        await self._enqueue_provider_otp(\n            email_address=normalized.address,\n            code=otp.code,\n            expires_at=verification_expires_at,\n            now=now,\n        )\n''',
        '''        if expires_at is None or verification_expires_at is None or email_command is None:\n            raise AuthIntegrityError("provider enrollment email update lost challenge timestamps")\n        await self._after_provider_email_commit(email_command, staged=staged)\n''',
        label="google set-email post commit",
    )

    text = replace_exact(
        text,
        '''        email_address: str | None = None\n        expires_at: datetime | None = None\n        verification_expires_at: datetime | None = None\n        database_session = self._session_factory()\n''',
        '''        email_address: str | None = None\n        expires_at: datetime | None = None\n        verification_expires_at: datetime | None = None\n        email_command: ProviderEnrollmentVerificationEmail | None = None\n        staged = False\n        database_session = self._session_factory()\n''',
        label="google resend staged state",
    )
    text = replace_exact(
        text,
        '''            locked.verification_expires_at = verification_expires_at\n            locked.failed_verification_attempts = 0\n            locked.updated_at = now\n            await database_session.commit()\n''',
        '''            locked.verification_expires_at = verification_expires_at\n            locked.failed_verification_attempts = 0\n            locked.updated_at = now\n            email_command = self._provider_email_command(\n                email_address=email_address,\n                code=otp.code,\n                expires_at=verification_expires_at,\n                now=now,\n            )\n            staged = await self._stage_provider_email(\n                database_session,\n                command=email_command,\n                idempotency_key=f"{external_signup_ref}:{now.isoformat()}",\n                expires_at=verification_expires_at,\n                supersession_key=f"provider-enrollment:{external_signup_ref}",\n            )\n            await database_session.commit()\n''',
        label="google resend atomic intent",
    )
    text = replace_exact(
        text,
        '''        if email_address is None or expires_at is None or verification_expires_at is None:\n            raise AuthIntegrityError("provider enrollment resend lost challenge state")\n        await self._enqueue_provider_otp(\n            email_address=email_address,\n            code=otp.code,\n            expires_at=verification_expires_at,\n            now=now,\n        )\n''',
        '''        if (\n            email_address is None\n            or expires_at is None\n            or verification_expires_at is None\n            or email_command is None\n        ):\n            raise AuthIntegrityError("provider enrollment resend lost challenge state")\n        await self._after_provider_email_commit(email_command, staged=staged)\n''',
        label="google resend post commit",
    )

    text = replace_exact(
        text,
        '''        await self._persist_provider_enrollment(row)\n        if otp is not None and evidence.email is not None and verification_expires_at is not None:\n            await self._enqueue_provider_otp(\n                email_address=evidence.email.address,\n                code=otp.code,\n                expires_at=verification_expires_at,\n                now=now,\n            )\n''',
        '''        email_command = (\n            self._provider_email_command(\n                email_address=evidence.email.address,\n                code=otp.code,\n                expires_at=verification_expires_at,\n                now=now,\n            )\n            if otp is not None\n            and evidence.email is not None\n            and verification_expires_at is not None\n            else None\n        )\n        staged = await self._persist_provider_enrollment(row, email_command=email_command)\n        if email_command is not None:\n            await self._after_provider_email_commit(email_command, staged=staged)\n''',
        label="google initial enrollment atomic intent",
    )

    text = replace_exact(
        text,
        '''    async def _persist_provider_enrollment(self, row: ExternalSignupChallengeRow) -> None:\n        ambiguous_commit = False\n        database_session = self._session_factory()\n''',
        '''    async def _persist_provider_enrollment(\n        self,\n        row: ExternalSignupChallengeRow,\n        *,\n        email_command: ProviderEnrollmentVerificationEmail | None,\n    ) -> bool:\n        ambiguous_commit = False\n        staged = False\n        database_session = self._session_factory()\n''',
        label="google persistence signature",
    )
    text = replace_exact(
        text,
        '''            )\n            database_session.add(row)\n            try:\n''',
        '''            )\n            database_session.add(row)\n            if email_command is not None:\n                if row.verification_expires_at is None:\n                    raise AuthIntegrityError("provider enrollment email lost verification expiry")\n                staged = await self._stage_provider_email(\n                    database_session,\n                    command=email_command,\n                    idempotency_key=(\n                        f"{row.external_signup_ref}:{row.verification_issued_at.isoformat()}"\n                    ),\n                    expires_at=row.verification_expires_at,\n                    supersession_key=f"provider-enrollment:{row.external_signup_ref}",\n                )\n            try:\n''',
        label="google persistence atomic stage",
    )
    text = replace_exact(
        text,
        '''        if not ambiguous_commit:\n            return\n        persisted = await self._read_provider_enrollment(row.external_signup_ref)\n''',
        '''        if not ambiguous_commit:\n            return staged\n        persisted = await self._read_provider_enrollment(row.external_signup_ref)\n''',
        label="google persistence normal return",
    )
    text = replace_exact(
        text,
        '''        ):\n            raise AuthServiceUnavailableError(retryable=False)\n\n    async def _persist_link_challenge''',
        '''        ):\n            raise AuthServiceUnavailableError(retryable=False)\n        return staged\n\n    async def _persist_link_challenge''',
        label="google persistence ambiguous return",
    )

    text = replace_exact(
        text,
        '''    async def _enqueue_provider_otp(\n        self,\n        *,\n        email_address: str,\n''',
        '''    async def _stage_provider_email(\n        self,\n        database_session: AsyncSession,\n        *,\n        command: ProviderEnrollmentVerificationEmail,\n        idempotency_key: str,\n        expires_at: datetime,\n        supersession_key: str,\n    ) -> bool:\n        if self._email_outbox is None:\n            return False\n        try:\n            await self._email_outbox.stage(\n                database_session,\n                command=command,\n                operation_scope="auth.provider_enrollment_verification",\n                idempotency_key=idempotency_key,\n                expires_at=expires_at,\n                supersession_key=supersession_key,\n            )\n        except EmailIntentConflictError as exc:\n            raise AuthIntegrityError("provider email intent idempotency conflict") from exc\n        return True\n\n    async def _after_provider_email_commit(\n        self,\n        command: ProviderEnrollmentVerificationEmail,\n        *,\n        staged: bool,\n    ) -> None:\n        if staged:\n            if self._email_wake is not None:\n                self._email_wake()\n            return\n        try:\n            await self._email_delivery.enqueue(command)\n        except EmailDispatchCapacityError as exc:\n            raise EmailDeliveryUnavailableError() from exc\n\n    @staticmethod\n    def _provider_email_command(\n        *,\n        email_address: str,\n        code: SecretStr,\n        expires_at: datetime,\n        now: datetime,\n    ) -> ProviderEnrollmentVerificationEmail:\n        return ProviderEnrollmentVerificationEmail(\n            to_address=email_address,\n            code=code,\n            expires_minutes=max(1, math.ceil((expires_at - now).total_seconds() / 60)),\n        )\n\n    async def _enqueue_provider_otp(\n        self,\n        *,\n        email_address: str,\n''',
        label="google durable email helpers",
    )
    return text


def patch_apple(text: str) -> str:
    text = replace_exact(
        text,
        "from contextlib import suppress\n",
        "from collections.abc import Callable\nfrom contextlib import suppress\n",
        label="apple callable import",
    )
    text = replace_exact(
        text,
        "from dante.auth.email import EmailNormalizationError, NormalizedEmail, normalize_email\n",
        "from dante.auth.email import EmailNormalizationError, NormalizedEmail, normalize_email\n"
        "from dante.auth.email_contracts import EmailIntentConflictError\n"
        "from dante.auth.email_outbox import DurableEmailOutbox\n",
        label="apple durable imports",
    )
    text = replace_exact(
        text,
        '''        otp_codec: ProviderEnrollmentOtpCodec,\n        email_delivery: EmailDeliveryPort,\n        limiters: ProviderFlowLimiters,\n    ) -> None:\n''',
        '''        otp_codec: ProviderEnrollmentOtpCodec,\n        email_delivery: EmailDeliveryPort,\n        limiters: ProviderFlowLimiters,\n        email_outbox: DurableEmailOutbox | None = None,\n        email_wake: Callable[[], None] | None = None,\n    ) -> None:\n''',
        label="apple constructor signature",
    )
    text = replace_exact(
        text,
        '''        self._otp_codec = otp_codec\n        self._email_delivery = email_delivery\n        self._limiters = limiters\n''',
        '''        self._otp_codec = otp_codec\n        self._email_delivery = email_delivery\n        self._email_outbox = email_outbox\n        self._email_wake = email_wake\n        self._limiters = limiters\n''',
        label="apple constructor fields",
    )

    text = replace_exact(
        text,
        '''        email_address: str | None = None\n        verification_expires_at: datetime | None = None\n        expires_at: datetime | None = None\n        database_session = self._session_factory()\n''',
        '''        email_address: str | None = None\n        verification_expires_at: datetime | None = None\n        expires_at: datetime | None = None\n        email_command: ProviderEnrollmentVerificationEmail | None = None\n        staged = False\n        database_session = self._session_factory()\n''',
        label="apple set-email staged state",
    )
    text = replace_exact(
        text,
        '''            challenge.verification_expires_at = verification_expires_at\n            challenge.failed_verification_attempts = 0\n            challenge.updated_at = now\n            await database_session.commit()\n''',
        '''            challenge.verification_expires_at = verification_expires_at\n            challenge.failed_verification_attempts = 0\n            challenge.updated_at = now\n            email_command = self._provider_email_command(\n                email_address=email_address,\n                code=otp.code,\n                expires_at=verification_expires_at,\n                now=now,\n            )\n            staged = await self._stage_provider_email(\n                database_session,\n                command=email_command,\n                idempotency_key=f"{external_signup_ref}:{now.isoformat()}",\n                expires_at=verification_expires_at,\n                supersession_key=f"provider-enrollment:{external_signup_ref}",\n            )\n            await database_session.commit()\n''',
        label="apple set-email atomic intent",
    )
    text = replace_exact(
        text,
        '''        if email_address is None or expires_at is None or verification_expires_at is None:\n            raise AuthIntegrityError("Apple enrollment email update lost challenge state")\n        await self._enqueue_otp(\n            email_address=email_address,\n            code=otp.code,\n            expires_at=verification_expires_at,\n            now=now,\n        )\n''',
        '''        if (\n            email_address is None\n            or expires_at is None\n            or verification_expires_at is None\n            or email_command is None\n        ):\n            raise AuthIntegrityError("Apple enrollment email update lost challenge state")\n        await self._after_provider_email_commit(email_command, staged=staged)\n''',
        label="apple set-email post commit",
    )

    text = replace_exact(
        text,
        '''        email_address: str | None = None\n        verification_expires_at: datetime | None = None\n        expires_at: datetime | None = None\n        database_session = self._session_factory()\n''',
        '''        email_address: str | None = None\n        verification_expires_at: datetime | None = None\n        expires_at: datetime | None = None\n        email_command: ProviderEnrollmentVerificationEmail | None = None\n        staged = False\n        database_session = self._session_factory()\n''',
        label="apple resend staged state",
    )
    text = replace_exact(
        text,
        '''            challenge.verification_expires_at = verification_expires_at\n            challenge.failed_verification_attempts = 0\n            challenge.updated_at = now\n            await database_session.commit()\n''',
        '''            challenge.verification_expires_at = verification_expires_at\n            challenge.failed_verification_attempts = 0\n            challenge.updated_at = now\n            email_command = self._provider_email_command(\n                email_address=email_address,\n                code=otp.code,\n                expires_at=verification_expires_at,\n                now=now,\n            )\n            staged = await self._stage_provider_email(\n                database_session,\n                command=email_command,\n                idempotency_key=f"{external_signup_ref}:{now.isoformat()}",\n                expires_at=verification_expires_at,\n                supersession_key=f"provider-enrollment:{external_signup_ref}",\n            )\n            await database_session.commit()\n''',
        label="apple resend atomic intent",
    )
    text = replace_exact(
        text,
        '''        if email_address is None or expires_at is None or verification_expires_at is None:\n            raise AuthIntegrityError("Apple enrollment resend lost challenge state")\n        await self._enqueue_otp(\n            email_address=email_address,\n            code=otp.code,\n            expires_at=verification_expires_at,\n            now=now,\n        )\n''',
        '''        if (\n            email_address is None\n            or expires_at is None\n            or verification_expires_at is None\n            or email_command is None\n        ):\n            raise AuthIntegrityError("Apple enrollment resend lost challenge state")\n        await self._after_provider_email_commit(email_command, staged=staged)\n''',
        label="apple resend post commit",
    )

    text = replace_exact(
        text,
        '''        await self._persist_enrollment(row)\n        if otp is not None and email is not None and verification_expires_at is not None:\n            await self._enqueue_otp(\n                email_address=email.address,\n                code=otp.code,\n                expires_at=verification_expires_at,\n                now=now,\n            )\n''',
        '''        email_command = (\n            self._provider_email_command(\n                email_address=email.address,\n                code=otp.code,\n                expires_at=verification_expires_at,\n                now=now,\n            )\n            if otp is not None and email is not None and verification_expires_at is not None\n            else None\n        )\n        staged = await self._persist_enrollment(row, email_command=email_command)\n        if email_command is not None:\n            await self._after_provider_email_commit(email_command, staged=staged)\n''',
        label="apple initial enrollment atomic intent",
    )

    text = replace_exact(
        text,
        '''    async def _persist_enrollment(self, row: ExternalSignupChallengeRow) -> None:\n        ambiguous_commit = False\n        database_session = self._session_factory()\n''',
        '''    async def _persist_enrollment(\n        self,\n        row: ExternalSignupChallengeRow,\n        *,\n        email_command: ProviderEnrollmentVerificationEmail | None,\n    ) -> bool:\n        ambiguous_commit = False\n        staged = False\n        database_session = self._session_factory()\n''',
        label="apple persistence signature",
    )
    text = replace_exact(
        text,
        '''            )\n            database_session.add(row)\n            ambiguous_commit = await self._commit(database_session)\n''',
        '''            )\n            database_session.add(row)\n            if email_command is not None:\n                if row.verification_expires_at is None:\n                    raise AuthIntegrityError("Apple enrollment email lost verification expiry")\n                staged = await self._stage_provider_email(\n                    database_session,\n                    command=email_command,\n                    idempotency_key=(\n                        f"{row.external_signup_ref}:{row.verification_issued_at.isoformat()}"\n                    ),\n                    expires_at=row.verification_expires_at,\n                    supersession_key=f"provider-enrollment:{row.external_signup_ref}",\n                )\n            ambiguous_commit = await self._commit(database_session)\n''',
        label="apple persistence atomic stage",
    )
    text = replace_exact(
        text,
        '''        if ambiguous_commit:\n            persisted = await self._read_enrollment(row.external_signup_ref)\n            if not self._same_enrollment(persisted, row):\n                raise ProviderReconciliationPendingError()\n\n    async def _persist_link''',
        '''        if ambiguous_commit:\n            persisted = await self._read_enrollment(row.external_signup_ref)\n            if not self._same_enrollment(persisted, row):\n                raise ProviderReconciliationPendingError()\n        return staged\n\n    async def _persist_link''',
        label="apple persistence return",
    )

    text = replace_exact(
        text,
        '''    async def _enqueue_otp(\n        self,\n        *,\n        email_address: str,\n''',
        '''    async def _stage_provider_email(\n        self,\n        database_session: AsyncSession,\n        *,\n        command: ProviderEnrollmentVerificationEmail,\n        idempotency_key: str,\n        expires_at: datetime,\n        supersession_key: str,\n    ) -> bool:\n        if self._email_outbox is None:\n            return False\n        try:\n            await self._email_outbox.stage(\n                database_session,\n                command=command,\n                operation_scope="auth.provider_enrollment_verification",\n                idempotency_key=idempotency_key,\n                expires_at=expires_at,\n                supersession_key=supersession_key,\n            )\n        except EmailIntentConflictError as exc:\n            raise AuthIntegrityError("Apple email intent idempotency conflict") from exc\n        return True\n\n    async def _after_provider_email_commit(\n        self,\n        command: ProviderEnrollmentVerificationEmail,\n        *,\n        staged: bool,\n    ) -> None:\n        if staged:\n            if self._email_wake is not None:\n                self._email_wake()\n            return\n        try:\n            await self._email_delivery.enqueue(command)\n        except EmailDispatchCapacityError as exc:\n            raise EmailDeliveryUnavailableError() from exc\n\n    @staticmethod\n    def _provider_email_command(\n        *,\n        email_address: str,\n        code: SecretStr,\n        expires_at: datetime,\n        now: datetime,\n    ) -> ProviderEnrollmentVerificationEmail:\n        return ProviderEnrollmentVerificationEmail(\n            to_address=email_address,\n            code=code,\n            expires_minutes=max(1, math.ceil((expires_at - now).total_seconds() / 60)),\n        )\n\n    async def _enqueue_otp(\n        self,\n        *,\n        email_address: str,\n''',
        label="apple durable email helpers",
    )
    return text


def patch_runtime(text: str) -> str:
    injection = '''            email_outbox=(\n                lifecycle_runtime.email_platform.outbox\n                if lifecycle_runtime.email_platform is not None\n                else None\n            ),\n            email_wake=(\n                lifecycle_runtime.email_platform.wake\n                if lifecycle_runtime.email_platform is not None\n                else None\n            ),\n'''
    text = replace_exact(
        text,
        '''            otp_codec=otp_codec,\n            email_delivery=lifecycle_runtime.email_dispatcher,\n            limiters=limiters,\n        )\n        if settings.provider.google.enabled\n''',
        '''            otp_codec=otp_codec,\n            email_delivery=lifecycle_runtime.email_dispatcher,\n            limiters=limiters,\n''' + injection + '''        )\n        if settings.provider.google.enabled\n''',
        label="provider runtime google durable injection",
    )
    text = replace_exact(
        text,
        '''            grant_cipher=auth_runtime.apple_grant_cipher,\n            otp_codec=otp_codec,\n            email_delivery=lifecycle_runtime.email_dispatcher,\n            limiters=limiters,\n        )\n''',
        '''            grant_cipher=auth_runtime.apple_grant_cipher,\n            otp_codec=otp_codec,\n            email_delivery=lifecycle_runtime.email_dispatcher,\n            limiters=limiters,\n''' + injection + '''        )\n''',
        label="provider runtime apple durable injection",
    )
    return text


def main() -> None:
    root = Path(__file__).resolve().parents[3]
    validate_repo(root)
    targets = {
        relative: (root / relative).read_text()
        for relative in EXPECTED_HASHES
    }
    patched = {
        "apps/backend/src/dante/auth/provider_flow.py": patch_google(
            targets["apps/backend/src/dante/auth/provider_flow.py"]
        ),
        "apps/backend/src/dante/auth/apple_flow.py": patch_apple(
            targets["apps/backend/src/dante/auth/apple_flow.py"]
        ),
        "apps/backend/src/dante/auth/provider_flow_runtime.py": patch_runtime(
            targets["apps/backend/src/dante/auth/provider_flow_runtime.py"]
        ),
    }
    for relative, content in patched.items():
        (root / relative).write_text(content)
    print("M05 Email Platform Phase B materialized successfully.")
    print("Google + Apple enrollment email intents now share their PostgreSQL transaction.")
    print("No commit was created.")


if __name__ == "__main__":
    main()
