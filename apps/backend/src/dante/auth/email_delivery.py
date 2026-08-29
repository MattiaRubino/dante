"""Bounded process-owned email delivery boundary for M4 Auth lifecycle messages."""

from __future__ import annotations

import asyncio
import logging
import smtplib
import ssl
from dataclasses import dataclass
from email.message import EmailMessage
from typing import Protocol, TypeAlias
from uuid import UUID

from pydantic import SecretStr

from dante.platform.config.auth import AuthSettings, SmtpSecurity

_LOGGER = logging.getLogger(__name__)


class EmailDispatchCapacityError(RuntimeError):
    """The bounded process-owned delivery queue cannot admit more work."""


@dataclass(frozen=True, slots=True)
class SignupVerificationEmail:
    """Out-of-band six-digit signup verification message."""

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
    """Equivalent bounded queue work for deliberately neutral recovery paths."""

    reason: str = "neutral_recovery"


EmailCommand: TypeAlias = (
    SignupVerificationEmail
    | PasswordRecoveryEmail
    | PasswordResetNotificationEmail
    | NoopEmail
)


class EmailDeliveryPort(Protocol):
    """Application-facing delivery boundary; enqueue never performs network I/O."""

    async def enqueue(self, command: EmailCommand) -> None:
        """Admit one bounded delivery command or fail immediately on capacity pressure."""
        ...


class _Stop:
    pass


_STOP = _Stop()


class SmtpEmailDispatcher:
    """Fixed-worker bounded SMTP dispatcher with no blind transport retry."""

    def __init__(self, *, settings: AuthSettings) -> None:
        self._settings = settings
        self._queue: asyncio.Queue[EmailCommand | _Stop] = asyncio.Queue(
            maxsize=settings.email_queue_capacity
        )
        self._workers: list[asyncio.Task[None]] = []
        self._started = False
        self._closed = False

    async def start(self) -> None:
        """Start the fixed worker set exactly once."""
        if self._started:
            return
        if self._closed:
            raise RuntimeError("email dispatcher is already closed")
        self._started = True
        self._workers = [
            asyncio.create_task(self._worker(), name=f"dante-auth-email-{index}")
            for index in range(self._settings.email_worker_count)
        ]

    async def enqueue(self, command: EmailCommand) -> None:
        """Admit work without waiting on SMTP or an unbounded queue."""
        if not self._started or self._closed:
            raise EmailDispatchCapacityError("email dispatcher is unavailable")
        try:
            self._queue.put_nowait(command)
        except asyncio.QueueFull as exc:
            raise EmailDispatchCapacityError("email dispatcher capacity is exhausted") from exc

    async def aclose(self) -> None:
        """Drain admitted work, stop workers in-order and release task references."""
        if self._closed:
            return
        self._closed = True
        if not self._started:
            return

        for _worker in self._workers:
            await self._queue.put(_STOP)
        await asyncio.gather(*self._workers, return_exceptions=False)
        self._workers.clear()

    async def _worker(self) -> None:
        while True:
            command = await self._queue.get()
            try:
                if command is _STOP:
                    return
                if isinstance(command, NoopEmail):
                    continue
                try:
                    await asyncio.to_thread(self._send_sync, command)
                except Exception:
                    # Do not retry after an ambiguous SMTP outcome. User-driven resend is
                    # the recovery path and logs intentionally omit recipient/proof material.
                    _LOGGER.exception(
                        "auth.email_delivery_failed kind=%s",
                        type(command).__name__,
                    )
            finally:
                self._queue.task_done()

    def _send_sync(
        self,
        command: SignupVerificationEmail | PasswordRecoveryEmail | PasswordResetNotificationEmail,
    ) -> None:
        message = self._message(command)
        timeout = self._settings.smtp_timeout_seconds
        security = self._settings.smtp_security
        context = ssl.create_default_context()

        if security is SmtpSecurity.TLS:
            client: smtplib.SMTP = smtplib.SMTP_SSL(
                self._settings.smtp_host,
                self._settings.smtp_port,
                timeout=timeout,
                context=context,
            )
        else:
            client = smtplib.SMTP(
                self._settings.smtp_host,
                self._settings.smtp_port,
                timeout=timeout,
            )

        with client:
            client.ehlo()
            if security is SmtpSecurity.STARTTLS:
                client.starttls(context=context)
                client.ehlo()
            if self._settings.smtp_username is not None:
                assert self._settings.smtp_password is not None
                client.login(
                    self._settings.smtp_username,
                    self._settings.smtp_password.get_secret_value(),
                )
            client.send_message(message)

    def _message(
        self,
        command: SignupVerificationEmail | PasswordRecoveryEmail | PasswordResetNotificationEmail,
    ) -> EmailMessage:
        message = EmailMessage()
        message["From"] = self._settings.smtp_from_address
        message["To"] = command.to_address
        message["Auto-Submitted"] = "auto-generated"

        if isinstance(command, SignupVerificationEmail):
            message["Subject"] = "Verify your DANTE email"
            message.set_content(
                "Your DANTE verification code is "
                f"{command.code.get_secret_value()}.\n\n"
                f"It expires in {command.expires_minutes} minutes. "
                "If you did not request this, you can ignore this email.\n"
            )
            return message

        if isinstance(command, PasswordRecoveryEmail):
            recovery_url = (
                f"{self._settings.canonical_web_origin}/?recovery="
                f"{command.password_recovery_ref}#"
                f"{command.secret.get_secret_value()}"
            )
            message["Subject"] = "Reset your DANTE password"
            message.set_content(
                "A password reset was requested for your DANTE account.\n\n"
                f"Open this link to continue:\n{recovery_url}\n\n"
                "This link expires shortly and can be used only once. "
                "If you did not request this, you can ignore this email.\n"
            )
            return message

        message["Subject"] = "Your DANTE password was changed"
        message.set_content(
            "Your DANTE password was changed through account recovery. "
            "All existing sessions were signed out. If you did not perform this change, "
            "secure your email account and contact DANTE support through the official channel.\n"
        )
        return message
