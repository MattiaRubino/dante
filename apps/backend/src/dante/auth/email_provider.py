"""Last-mile providers for the DANTE durable email worker."""

from __future__ import annotations

import asyncio
import smtplib
import ssl
from email.message import EmailMessage
from typing import Any, cast, override

import boto3  # type: ignore[import-untyped]
from botocore.config import Config  # type: ignore[import-untyped]
from botocore.exceptions import (  # type: ignore[import-untyped]
    BotoCoreError,
    ClientError,
    ConnectionClosedError,
    ConnectTimeoutError,
    EndpointConnectionError,
    ReadTimeoutError,
)

from dante.auth.email_contracts import (
    EmailProviderPort,
    ProviderMessage,
    ProviderOutcome,
    ProviderSendResult,
)
from dante.platform.config.auth import AuthSettings, SmtpSecurity

_AMBIGUOUS_BOTO_ERRORS = (
    ConnectTimeoutError,
    ConnectionClosedError,
    EndpointConnectionError,
    ReadTimeoutError,
)
_SES_RETRYABLE_CODES = frozenset(
    {
        "LimitExceededException",
        "TooManyRequestsException",
        "Throttling",
        "ThrottlingException",
        "ServiceUnavailable",
        "ServiceUnavailableException",
        "InternalFailure",
        "InternalServerError",
    }
)
_SES_DEFINITIVE_CODES = frozenset(
    {
        "AccountSuspendedException",
        "BadRequestException",
        "MailFromDomainNotVerifiedException",
        "MessageRejected",
        "NotFoundException",
        "SendingPausedException",
    }
)
_SMTP_DEFINITIVE_ERRORS = (
    smtplib.SMTPAuthenticationError,
    smtplib.SMTPRecipientsRefused,
    smtplib.SMTPSenderRefused,
)


class SesEmailProvider(EmailProviderPort):
    """Amazon SES API v2 adapter with exactly one deliberate SDK wire attempt."""

    provider_code = "ses"

    def __init__(self, *, settings: AuthSettings) -> None:
        if settings.ses_region is None:
            raise ValueError("SES email transport requires an AWS region")
        self._configuration_set = settings.ses_configuration_set
        self._client: Any = boto3.client(
            "sesv2",
            region_name=settings.ses_region,
            config=Config(
                connect_timeout=settings.email_provider_connect_timeout_seconds,
                read_timeout=settings.email_provider_read_timeout_seconds,
                tcp_keepalive=True,
                retries={"mode": "standard", "total_max_attempts": 1},
            ),
        )

    @override
    async def send(self, message: ProviderMessage) -> ProviderSendResult:
        """Execute one SES send; any uncertain transport result remains ambiguous."""
        try:
            response = await asyncio.to_thread(self._send_sync, message)
        except _AMBIGUOUS_BOTO_ERRORS as exc:
            return ProviderSendResult(
                outcome=ProviderOutcome.AMBIGUOUS,
                safe_error_code=type(exc).__name__,
            )
        except ClientError as exc:
            error = exc.response.get("Error", {})
            code = str(error.get("Code", "ClientError"))
            if code in _SES_RETRYABLE_CODES:
                return ProviderSendResult(
                    outcome=ProviderOutcome.RETRYABLE_FAILURE,
                    safe_error_code=code,
                )
            if code in _SES_DEFINITIVE_CODES:
                return ProviderSendResult(
                    outcome=ProviderOutcome.DEFINITIVE_FAILURE,
                    safe_error_code=code,
                )
            # Unknown SES responses are not proof that the request was rejected before acceptance.
            return ProviderSendResult(
                outcome=ProviderOutcome.AMBIGUOUS,
                safe_error_code=code,
            )
        except BotoCoreError as exc:
            return ProviderSendResult(
                outcome=ProviderOutcome.AMBIGUOUS,
                safe_error_code=type(exc).__name__,
            )

        message_id = response.get("MessageId")
        if not isinstance(message_id, str) or not message_id.strip():
            return ProviderSendResult(
                outcome=ProviderOutcome.AMBIGUOUS,
                safe_error_code="missing_provider_message_id",
            )
        return ProviderSendResult(
            outcome=ProviderOutcome.ACCEPTED,
            provider_message_id=message_id,
        )

    def _send_sync(self, message: ProviderMessage) -> dict[str, Any]:
        body: dict[str, Any] = {
            "Text": {"Data": message.text_body, "Charset": "UTF-8"},
        }
        if message.html_body is not None:
            body["Html"] = {"Data": message.html_body, "Charset": "UTF-8"}
        request: dict[str, Any] = {
            "FromEmailAddress": message.from_address,
            "Destination": {"ToAddresses": [message.to_address]},
            "Content": {
                "Simple": {
                    "Subject": {"Data": message.subject, "Charset": "UTF-8"},
                    "Body": body,
                }
            },
            "EmailTags": [
                {"Name": "dante_intent", "Value": str(message.email_intent_ref)},
                {"Name": "dante_stream", "Value": message.stream_code},
            ],
        }
        if self._configuration_set is not None:
            request["ConfigurationSetName"] = self._configuration_set
        return cast(dict[str, Any], self._client.send_email(**request))


class SmtpEmailProvider(EmailProviderPort):
    """Direct SMTP last-mile adapter for LOCAL/CI behind the durable outbox."""

    provider_code = "smtp"

    def __init__(self, *, settings: AuthSettings) -> None:
        self._settings = settings

    @override
    async def send(self, message: ProviderMessage) -> ProviderSendResult:
        """Perform one SMTP transaction with no process queue and no transport retry."""
        try:
            await asyncio.to_thread(self._send_sync, message)
        except _SMTP_DEFINITIVE_ERRORS as exc:
            return ProviderSendResult(
                outcome=ProviderOutcome.DEFINITIVE_FAILURE,
                safe_error_code=type(exc).__name__,
            )
        except (OSError, smtplib.SMTPException) as exc:
            # After the transport starts, disconnect/timeout/general SMTP failure may occur
            # after remote acceptance. Preserve uncertainty rather than blind-retrying.
            return ProviderSendResult(
                outcome=ProviderOutcome.AMBIGUOUS,
                safe_error_code=type(exc).__name__,
            )
        return ProviderSendResult(outcome=ProviderOutcome.ACCEPTED)

    def _send_sync(self, message: ProviderMessage) -> None:
        email = EmailMessage()
        email["From"] = message.from_address
        email["To"] = message.to_address
        email["Subject"] = message.subject
        email["Auto-Submitted"] = "auto-generated"
        email.set_content(message.text_body)
        if message.html_body is not None:
            email.add_alternative(message.html_body, subtype="html")

        security = self._settings.smtp_security
        context = ssl.create_default_context()
        if security is SmtpSecurity.TLS:
            client: smtplib.SMTP = smtplib.SMTP_SSL(
                self._settings.smtp_host,
                self._settings.smtp_port,
                timeout=self._settings.email_provider_read_timeout_seconds,
                context=context,
            )
        else:
            client = smtplib.SMTP(
                self._settings.smtp_host,
                self._settings.smtp_port,
                timeout=self._settings.email_provider_read_timeout_seconds,
            )
        with client:
            client.ehlo()
            if security is SmtpSecurity.STARTTLS:
                client.starttls(context=context)
                client.ehlo()
            if self._settings.smtp_username is not None:
                password = self._settings.smtp_password
                if password is None:
                    raise RuntimeError("SMTP password missing for configured username")
                client.login(self._settings.smtp_username, password.get_secret_value())
            client.send_message(email)
