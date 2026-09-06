"""Unit proof for DANTE email normalization/comparison semantics."""

from unicodedata import normalize

import pytest

from dante.auth.email import EmailNormalizationError, normalize_email


def test_email_normalization_preserves_local_part_and_uses_idna_comparison() -> None:
    normalized_email = normalize_email("Usér@Exämple.COM")

    assert normalized_email.address.startswith("Usér@")
    assert normalized_email.comparison_key == "usér@xn--exmple-cua.com"


def test_email_comparison_uses_nfc_then_unicode_casefold() -> None:
    composed = normalize_email("TÉST@example.com")
    decomposed = normalize_email(f"T{normalize('NFD', 'É')}ST@example.com")

    assert composed.comparison_key == decomposed.comparison_key


def test_email_policy_does_not_apply_provider_specific_dot_or_plus_rewriting() -> None:
    first = normalize_email("first.last+tag@gmail.com")
    second = normalize_email("firstlast@gmail.com")

    assert first.comparison_key != second.comparison_key


@pytest.mark.parametrize(
    "value",
    ["", "not-an-email", "a@localhost", "Display <a@example.com>"],
)
def test_invalid_login_email_is_rejected_without_deliverability_lookup(value: str) -> None:
    with pytest.raises(EmailNormalizationError):
        normalize_email(value)
