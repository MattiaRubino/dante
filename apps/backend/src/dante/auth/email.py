"""Canonical DANTE email normalization and comparison policy."""

from dataclasses import dataclass
from unicodedata import normalize

from email_validator import EmailNotValidError, validate_email


class EmailNormalizationError(ValueError):
    """Submitted email cannot enter the canonical comparison pipeline."""


@dataclass(frozen=True, slots=True)
class NormalizedEmail:
    """Delivery/display representation plus deterministic DANTE comparison key."""

    address: str
    comparison_key: str


def normalize_email(value: str) -> NormalizedEmail:
    """Validate and normalize one login email without DNS/deliverability I/O."""
    try:
        validated = validate_email(
            value,
            allow_smtputf8=True,
            check_deliverability=False,
        )
    except EmailNotValidError as exc:
        raise EmailNormalizationError("invalid email address") from exc

    ascii_domain = validated.ascii_domain
    if ascii_domain is None:
        raise EmailNormalizationError("email domain has no canonical IDNA form")

    local_part = normalize("NFC", validated.local_part)
    return NormalizedEmail(
        address=validated.normalized,
        comparison_key=f"{local_part.casefold()}@{ascii_domain.lower()}",
    )
