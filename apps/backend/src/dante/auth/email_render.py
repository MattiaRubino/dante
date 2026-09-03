"""Repository-owned Auth/security email intent derivation and rendering."""

from __future__ import annotations

from dante.auth.email import normalize_email
from dante.auth.email_contracts import (
    ClaimedEmailIntent,
    EmailIntentSpec,
    EmailPayloadError,
    ProviderMessage,
)
from dante.auth.email_crypto import EmailPayloadCipher
from dante.auth.email_delivery import (
    DeliverableEmail,
    PasswordRecoveryEmail,
    PasswordResetNotificationEmail,
    ProviderEnrollmentVerificationEmail,
    SignupVerificationEmail,
)


def email_intent_spec(command: DeliverableEmail) -> EmailIntentSpec:
    """Freeze one typed Auth email command into provider-neutral durable semantics."""
    normalized = normalize_email(command.to_address)
    if isinstance(command, SignupVerificationEmail):
        return EmailIntentSpec(
            purpose_code="signup_verification",
            template_code="auth.signup_verification",
            payload={
                "code": command.code.get_secret_value(),
                "expires_minutes": command.expires_minutes,
            },
            recipient_address=normalized.address,
            recipient_comparison_key=normalized.comparison_key,
        )
    if isinstance(command, ProviderEnrollmentVerificationEmail):
        return EmailIntentSpec(
            purpose_code="provider_enrollment_verification",
            template_code="auth.provider_enrollment_verification",
            payload={
                "code": command.code.get_secret_value(),
                "expires_minutes": command.expires_minutes,
            },
            recipient_address=normalized.address,
            recipient_comparison_key=normalized.comparison_key,
        )
    if isinstance(command, PasswordRecoveryEmail):
        return EmailIntentSpec(
            purpose_code="password_recovery",
            template_code="auth.password_recovery",
            payload={
                "password_recovery_ref": str(command.password_recovery_ref),
                "secret": command.secret.get_secret_value(),
            },
            recipient_address=normalized.address,
            recipient_comparison_key=normalized.comparison_key,
        )
    if isinstance(command, PasswordResetNotificationEmail):
        return EmailIntentSpec(
            purpose_code="password_reset_notification",
            template_code="auth.password_reset_notification",
            payload={},
            recipient_address=normalized.address,
            recipient_comparison_key=normalized.comparison_key,
        )
    raise AssertionError("unreachable deliverable email type")


def render_claim(
    *,
    claim: ClaimedEmailIntent,
    cipher: EmailPayloadCipher,
    from_address: str,
    canonical_web_origin: str,
) -> ProviderMessage:
    """Render reviewed text-only Auth/security copy from one authenticated payload."""
    payload = cipher.unprotect(claim=claim)

    if claim.purpose_code == "signup_verification":
        code = _require_str(payload, "code")
        expires_minutes = _require_int(payload, "expires_minutes")
        subject = "Verify your DANTE email"
        text_body = (
            f"Your DANTE verification code is {code}.\n\n"
            f"It expires in {expires_minutes} minutes. "
            "If you did not request this, you can ignore this email.\n"
        )
    elif claim.purpose_code == "provider_enrollment_verification":
        code = _require_str(payload, "code")
        expires_minutes = _require_int(payload, "expires_minutes")
        subject = "Verify your email for DANTE"
        text_body = (
            f"Use this code to finish setting up your DANTE account: {code}.\n\n"
            f"It expires in {expires_minutes} minutes. "
            "If you did not start this sign-in, you can ignore this email.\n"
        )
    elif claim.purpose_code == "password_recovery":
        recovery_ref = _require_str(payload, "password_recovery_ref")
        secret = _require_str(payload, "secret")
        recovery_url = f"{canonical_web_origin}/?recovery={recovery_ref}#{secret}"
        subject = "Reset your DANTE password"
        text_body = (
            "A password reset was requested for your DANTE account.\n\n"
            f"Open this link to continue:\n{recovery_url}\n\n"
            "This link expires shortly and can be used only once. "
            "If you did not request this, you can ignore this email.\n"
        )
    elif claim.purpose_code == "password_reset_notification":
        subject = "Your DANTE password was changed"
        text_body = (
            "Your DANTE password was changed through account recovery. "
            "All existing sessions were signed out. If you did not perform this change, "
            "secure your email account and contact DANTE support through the official channel.\n"
        )
    else:
        raise EmailPayloadError("email intent references an unsupported purpose")

    return ProviderMessage(
        email_intent_ref=claim.email_intent_ref,
        from_address=from_address,
        to_address=claim.recipient_address,
        subject=subject,
        text_body=text_body,
        html_body=None,
    )


def _require_str(payload: dict[str, str | int], name: str) -> str:
    value = payload.get(name)
    if not isinstance(value, str) or not value:
        raise EmailPayloadError(f"email payload is missing {name}")
    return value


def _require_int(payload: dict[str, str | int], name: str) -> int:
    value = payload.get(name)
    if not isinstance(value, int) or isinstance(value, bool):
        raise EmailPayloadError(f"email payload is missing {name}")
    return value
