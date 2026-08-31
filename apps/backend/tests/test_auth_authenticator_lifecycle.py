"""Pure policy tests for M5-E/G Account-wide authenticator lifecycle."""

import pytest

from dante.auth.authenticator_lifecycle import (
    AuthenticatorState,
    require_viable_authenticator_state,
)
from dante.auth.contracts import AuthenticatorRemovalBlockedError


@pytest.mark.parametrize(
    "state",
    [
        AuthenticatorState(
            password_present=True,
            active_provider_count=0,
            active_passkey_count=0,
            recovery_eligible_email_count=0,
        ),
        AuthenticatorState(
            password_present=False,
            active_provider_count=1,
            active_passkey_count=0,
            recovery_eligible_email_count=1,
        ),
        AuthenticatorState(
            password_present=False,
            active_provider_count=0,
            active_passkey_count=2,
            recovery_eligible_email_count=1,
        ),
        AuthenticatorState(
            password_present=True,
            active_provider_count=1,
            active_passkey_count=1,
            recovery_eligible_email_count=0,
        ),
    ],
)
def test_viable_authenticator_state_accepts_supported_direct_access(
    state: AuthenticatorState,
) -> None:
    require_viable_authenticator_state(state)


@pytest.mark.parametrize(
    "state",
    [
        AuthenticatorState(
            password_present=False,
            active_provider_count=0,
            active_passkey_count=0,
            recovery_eligible_email_count=1,
        ),
        AuthenticatorState(
            password_present=False,
            active_provider_count=1,
            active_passkey_count=0,
            recovery_eligible_email_count=0,
        ),
        AuthenticatorState(
            password_present=False,
            active_provider_count=0,
            active_passkey_count=1,
            recovery_eligible_email_count=0,
        ),
    ],
)
def test_viable_authenticator_state_blocks_lockout_or_passwordless_without_recovery(
    state: AuthenticatorState,
) -> None:
    with pytest.raises(AuthenticatorRemovalBlockedError):
        require_viable_authenticator_state(state)


def test_direct_authenticator_count_counts_password_provider_and_passkey() -> None:
    state = AuthenticatorState(
        password_present=True,
        active_provider_count=2,
        active_passkey_count=3,
        recovery_eligible_email_count=1,
    )

    assert state.direct_authenticator_count == 6
