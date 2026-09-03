"""Repository-owned Auth/security email intent derivation and rendering."""

from __future__ import annotations

from html import escape

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

_SUPPORTED_TEMPLATE_REVISIONS = frozenset({"1", "2"})


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
    """Render reviewed repository-owned Auth/security copy from one authenticated payload."""
    if claim.template_revision not in _SUPPORTED_TEMPLATE_REVISIONS:
        raise EmailPayloadError("email intent references an unsupported template revision")

    payload = cipher.unprotect(claim=claim)
    html_body: str | None = None

    if claim.purpose_code == "signup_verification":
        code = _require_str(payload, "code")
        expires_minutes = _require_int(payload, "expires_minutes")
        subject = "Verify your DANTE email"
        text_body = (
            f"Your DANTE verification code is {code}.\n\n"
            f"It expires in {expires_minutes} minutes. "
            "If you did not request this, you can ignore this email.\n"
        )
        if claim.template_revision == "2":
            html_body = _html_document(
                heading="Verify your DANTE email",
                content=(
                    "<p>Your DANTE verification code is:</p>"
                    f'<p style="font-size:28px;font-weight:700;letter-spacing:4px;">'
                    f"{escape(code)}</p>"
                    f"<p>It expires in {expires_minutes} minutes.</p>"
                    "<p>If you did not request this, you can ignore this email.</p>"
                ),
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
        if claim.template_revision == "2":
            html_body = _html_document(
                heading="Verify your email for DANTE",
                content=(
                    "<p>Use this code to finish setting up your DANTE account:</p>"
                    f'<p style="font-size:28px;font-weight:700;letter-spacing:4px;">'
                    f"{escape(code)}</p>"
                    f"<p>It expires in {expires_minutes} minutes.</p>"
                    "<p>If you did not start this sign-in, you can ignore this email.</p>"
                ),
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
        if claim.template_revision == "2":
            safe_url = escape(recovery_url, quote=True)
            html_body = _html_document(
                heading="Reset your DANTE password",
                content=(
                    "<p>A password reset was requested for your DANTE account.</p>"
                    f'<p><a href="{safe_url}" style="display:inline-block;padding:12px 18px;'
                    'background:#111827;color:#ffffff;text-decoration:none;border-radius:8px;">'
                    "Reset password</a></p>"
                    "<p>This link expires shortly and can be used only once.</p>"
                    "<p>If you did not request this, you can ignore this email.</p>"
                ),
            )
    elif claim.purpose_code == "password_reset_notification":
        subject = "Your DANTE password was changed"
        text_body = (
            "Your DANTE password was changed through account recovery. "
            "All existing sessions were signed out. If you did not perform this change, "
            "secure your email account and contact DANTE support through the official channel.\n"
        )
        if claim.template_revision == "2":
            html_body = _html_document(
                heading="Your DANTE password was changed",
                content=(
                    "<p>Your DANTE password was changed through account recovery. "
                    "All existing sessions were signed out.</p>"
                    "<p>If you did not perform this change, secure your email account and "
                    "contact DANTE support through the official channel.</p>"
                ),
            )
    else:
        raise EmailPayloadError("email intent references an unsupported purpose")

    return ProviderMessage(
        email_intent_ref=claim.email_intent_ref,
        from_address=from_address,
        to_address=claim.recipient_address,
        subject=subject,
        text_body=text_body,
        html_body=html_body,
    )


def _html_document(*, heading: str, content: str) -> str:
    safe_heading = escape(heading)
    return (
        "<!doctype html>"
        '<html lang="en"><body style="margin:0;padding:0;background:#f6f7f9;">'
        '<table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0" '
        'style="background:#f6f7f9;padding:24px 12px;">'
        '<tr><td align="center">'
        '<table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0" '
        'style="max-width:560px;background:#ffffff;border:1px solid #e5e7eb;border-radius:12px;">'
        '<tr><td style="padding:28px;font-family:Arial,sans-serif;color:#111827;line-height:1.5;">'
        f'<h1 style="margin:0 0 20px;font-size:22px;line-height:1.3;">{safe_heading}</h1>'
        f"{content}"
        '<p style="margin-top:28px;color:#6b7280;font-size:12px;">'
        "This is an automated security message from DANTE.</p>"
        "</td></tr></table></td></tr></table></body></html>"
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
