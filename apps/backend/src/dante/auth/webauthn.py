"""fido2-backed WebAuthn RP/origin policy and protocol adapter."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from typing import Any, cast

from fido2 import cbor
from fido2.cose import CoseKey
from fido2.server import Fido2Server
from fido2.webauthn import (
    Aaguid,
    AttestationConveyancePreference,
    AttestedCredentialData,
    AuthenticationResponse,
    PublicKeyCredentialDescriptor,
    PublicKeyCredentialType,
    PublicKeyCredentialUserEntity,
    RegistrationResponse,
    ResidentKeyRequirement,
    UserVerificationRequirement,
)

from dante.platform.config.auth_provider import WebAuthnSettings

_MAX_CREDENTIAL_ID_BYTES = 1023
_MAX_COSE_PUBLIC_KEY_BYTES = 8192


@dataclass(frozen=True, slots=True)
class ParsedWebAuthnResponse:
    """Safe routing evidence parsed before any durable ceremony claim."""

    credential_id: bytes
    challenge: bytes
    origin: str
    user_handle: bytes | None


@dataclass(frozen=True, slots=True)
class WebAuthnRegistrationEvidence:
    """Verified registration evidence suitable for canonical credential persistence."""

    credential_id: bytes
    public_key_cose: bytes
    cose_algorithm: int
    sign_count: int
    backup_eligible: bool
    backup_state: bool
    challenge: bytes
    origin: str


@dataclass(frozen=True, slots=True)
class WebAuthnAssertionEvidence:
    """Verified assertion evidence suitable for session and credential-state mutation."""

    credential_id: bytes
    user_handle: bytes | None
    sign_count: int
    backup_eligible: bool
    backup_state: bool
    challenge: bytes
    origin: str


@dataclass(frozen=True, slots=True)
class WebAuthnPolicy:
    """Frozen relying-party policy plus exact fido2 ceremony verification."""

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

        from fido2.webauthn import PublicKeyCredentialRpEntity

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

    def registration_options(
        self,
        *,
        user_handle: bytes,
        display_name: str,
        challenge: bytes,
        existing_credential_ids: Sequence[bytes],
    ) -> dict[str, Any]:
        """Build resident, UV-required registration options with duplicate exclusion."""
        credentials = [self._descriptor(credential_id) for credential_id in existing_credential_ids]
        options, _state = self.server.register_begin(
            PublicKeyCredentialUserEntity(
                id=user_handle,
                name=display_name,
                display_name=display_name,
            ),
            credentials=credentials,
            resident_key_requirement=self.resident_key,
            user_verification=self.user_verification,
            challenge=challenge,
        )
        return dict(options)

    def authentication_options(
        self,
        *,
        challenge: bytes,
        credential_ids: Sequence[bytes] | None,
    ) -> dict[str, Any]:
        """Build UV-required discoverable or Account-bound assertion options."""
        credentials = (
            None
            if credential_ids is None
            else [self._descriptor(credential_id) for credential_id in credential_ids]
        )
        options, _state = self.server.authenticate_begin(
            credentials=credentials,
            user_verification=self.user_verification,
            challenge=challenge,
        )
        return dict(options)

    @staticmethod
    def parse_registration(response: Mapping[str, Any]) -> ParsedWebAuthnResponse:
        """Parse bounded routing evidence without deciding ceremony validity."""
        registration = RegistrationResponse.from_dict(response)
        return ParsedWebAuthnResponse(
            credential_id=registration.raw_id,
            challenge=registration.response.client_data.challenge,
            origin=registration.response.client_data.origin,
            user_handle=None,
        )

    @staticmethod
    def parse_authentication(response: Mapping[str, Any]) -> ParsedWebAuthnResponse:
        """Parse assertion routing evidence without signature/authenticator trust."""
        authentication = AuthenticationResponse.from_dict(response)
        return ParsedWebAuthnResponse(
            credential_id=authentication.raw_id,
            challenge=authentication.response.client_data.challenge,
            origin=authentication.response.client_data.origin,
            user_handle=authentication.response.user_handle,
        )

    def verify_registration(
        self,
        *,
        response: Mapping[str, Any],
        expected_challenge: bytes,
    ) -> WebAuthnRegistrationEvidence:
        """Run the real fido2 RP/origin/challenge/UP/UV registration verifier."""
        registration = RegistrationResponse.from_dict(response)
        auth_data = self.server.register_complete(
            self._state(expected_challenge),
            registration,
        )
        credential = auth_data.credential_data
        if credential is None:
            raise ValueError("registration response omitted credential data")
        if not 1 <= len(credential.credential_id) <= _MAX_CREDENTIAL_ID_BYTES:
            raise ValueError("registered credential id exceeds the persistence contract")
        public_key_cose = cbor.encode(credential.public_key)
        if not 1 <= len(public_key_cose) <= _MAX_COSE_PUBLIC_KEY_BYTES:
            raise ValueError("registered COSE public key exceeds the persistence contract")
        algorithm = credential.public_key.ALGORITHM
        if algorithm is None:
            raise ValueError("registered COSE key has no algorithm")
        return WebAuthnRegistrationEvidence(
            credential_id=credential.credential_id,
            public_key_cose=public_key_cose,
            cose_algorithm=int(algorithm),
            sign_count=auth_data.counter,
            backup_eligible=auth_data.is_backup_eligible(),
            backup_state=auth_data.is_backed_up(),
            challenge=registration.response.client_data.challenge,
            origin=registration.response.client_data.origin,
        )

    def verify_authentication(
        self,
        *,
        response: Mapping[str, Any],
        expected_challenge: bytes,
        credential_id: bytes,
        public_key_cose: bytes,
        cose_algorithm: int,
    ) -> WebAuthnAssertionEvidence:
        """Verify an assertion through the persisted canonical COSE public key."""
        authentication = AuthenticationResponse.from_dict(response)
        credential = self._credential(
            credential_id=credential_id,
            public_key_cose=public_key_cose,
            cose_algorithm=cose_algorithm,
        )
        matched = self.server.authenticate_complete(
            self._state(expected_challenge),
            [credential],
            authentication,
        )
        if matched.credential_id != credential_id:
            raise ValueError("verified credential id mismatched canonical credential")
        auth_data = authentication.response.authenticator_data
        return WebAuthnAssertionEvidence(
            credential_id=authentication.raw_id,
            user_handle=authentication.response.user_handle,
            sign_count=auth_data.counter,
            backup_eligible=auth_data.is_backup_eligible(),
            backup_state=auth_data.is_backed_up(),
            challenge=authentication.response.client_data.challenge,
            origin=authentication.response.client_data.origin,
        )

    def _state(self, challenge: bytes) -> dict[str, Any]:
        """Reconstruct the only fido2 state fields accepted by the frozen M5 policy."""
        from fido2.utils import websafe_encode

        return {
            "challenge": websafe_encode(challenge),
            "user_verification": self.user_verification,
        }

    @staticmethod
    def _descriptor(credential_id: bytes) -> PublicKeyCredentialDescriptor:
        return PublicKeyCredentialDescriptor(
            type=PublicKeyCredentialType.PUBLIC_KEY,
            id=credential_id,
        )

    @staticmethod
    def _credential(
        *,
        credential_id: bytes,
        public_key_cose: bytes,
        cose_algorithm: int,
    ) -> AttestedCredentialData:
        decoded = cbor.decode(public_key_cose)
        if not isinstance(decoded, Mapping):
            raise ValueError("stored COSE public key is not a map")
        key = CoseKey.parse(cast(Mapping[int, Any], decoded))
        if cose_algorithm != key.ALGORITHM:
            raise ValueError("stored COSE algorithm does not match persisted metadata")
        return AttestedCredentialData.create(Aaguid.NONE, credential_id, key)
