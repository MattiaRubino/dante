"""fido2-backed WebAuthn RP/origin policy foundation."""

from __future__ import annotations

from dataclasses import dataclass

from fido2.server import Fido2Server
from fido2.webauthn import (
    AttestationConveyancePreference,
    PublicKeyCredentialRpEntity,
    ResidentKeyRequirement,
    UserVerificationRequirement,
)

from dante.platform.config.auth_provider import WebAuthnSettings


@dataclass(frozen=True, slots=True)
class WebAuthnPolicy:
    """Frozen relying-party policy; full ceremonies are intentionally deferred to M5-F."""

    server: Fido2Server
    rp_id: str
    rp_name: str
    expected_origins: frozenset[str]
    resident_key: ResidentKeyRequirement = ResidentKeyRequirement.REQUIRED
    user_verification: UserVerificationRequirement = UserVerificationRequirement.REQUIRED
    attestation: AttestationConveyancePreference = AttestationConveyancePreference.NONE

    @classmethod
    def from_settings(cls, settings: WebAuthnSettings) -> WebAuthnPolicy:
        origins = frozenset(settings.expected_origins)

        def verify_origin(origin: str) -> bool:
            return origin in origins

        rp = PublicKeyCredentialRpEntity(id=settings.rp_id, name=settings.rp_name)
        server = Fido2Server(
            rp,
            attestation=AttestationConveyancePreference.NONE,
            verify_origin=verify_origin,
        )
        return cls(
            server=server,
            rp_id=settings.rp_id,
            rp_name=settings.rp_name,
            expected_origins=origins,
        )

    def origin_allowed(self, origin: str) -> bool:
        """Accept only exact configured canonical origins; never suffix/substring match."""
        return origin in self.expected_origins
