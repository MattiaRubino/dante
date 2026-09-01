import type {
  PasskeyAuthenticationCompleteRequest,
  PasskeyCeremony,
  PasskeyReauthenticationCompleteRequest,
  PasskeyRegistrationCompleteRequest,
} from '@dante/api-client';

export class WebAuthnBrowserError extends Error {
  constructor(message: string, options?: ErrorOptions) {
    super(message, options);
    this.name = 'WebAuthnBrowserError';
  }
}

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === 'object' && value !== null && !Array.isArray(value);
}

function requiredRecord(
  source: Record<string, unknown>,
  key: string,
): Record<string, unknown> {
  const value = source[key];
  if (!isRecord(value)) {
    throw new WebAuthnBrowserError(`WebAuthn option ${key} is malformed.`);
  }
  return value;
}

function requiredString(source: Record<string, unknown>, key: string): string {
  const value = source[key];
  if (typeof value !== 'string' || value.length === 0) {
    throw new WebAuthnBrowserError(`WebAuthn option ${key} is malformed.`);
  }
  return value;
}

function base64UrlToBytes(value: string): Uint8Array<ArrayBuffer> {
  if (!/^[A-Za-z0-9_-]+$/.test(value)) {
    throw new WebAuthnBrowserError('WebAuthn binary field is not Base64URL.');
  }
  const padding = '='.repeat((4 - (value.length % 4)) % 4);
  const base64 = value.replace(/-/g, '+').replace(/_/g, '/') + padding;
  let binary: string;
  try {
    binary = atob(base64);
  } catch (error) {
    throw new WebAuthnBrowserError(
      'WebAuthn binary field could not be decoded.',
      { cause: error },
    );
  }
  const bytes = new Uint8Array(binary.length);
  for (let index = 0; index < binary.length; index += 1) {
    bytes[index] = binary.charCodeAt(index);
  }
  return bytes;
}

function bytesToBase64Url(value: ArrayBuffer | ArrayBufferView): string {
  const bytes =
    value instanceof ArrayBuffer
      ? new Uint8Array(value)
      : new Uint8Array(value.buffer, value.byteOffset, value.byteLength);
  let binary = '';
  for (const byte of bytes) {
    binary += String.fromCharCode(byte);
  }
  return btoa(binary)
    .replace(/\+/g, '-')
    .replace(/\//g, '_')
    .replace(/=+$/g, '');
}

function decodeCredentialDescriptors(value: unknown): PublicKeyCredentialDescriptor[] | undefined {
  if (value === undefined) {
    return undefined;
  }
  if (!Array.isArray(value)) {
    throw new WebAuthnBrowserError('WebAuthn credential descriptors are malformed.');
  }
  return value.map((entry) => {
    if (!isRecord(entry)) {
      throw new WebAuthnBrowserError('WebAuthn credential descriptor is malformed.');
    }
    const type = requiredString(entry, 'type');
    if (type !== 'public-key') {
      throw new WebAuthnBrowserError('WebAuthn credential descriptor type is unsupported.');
    }
    const transportsValue = entry.transports;
    const transports =
      transportsValue === undefined
        ? undefined
        : Array.isArray(transportsValue) &&
            transportsValue.every((item) => typeof item === 'string')
          ? (transportsValue as AuthenticatorTransport[])
          : (() => {
              throw new WebAuthnBrowserError(
                'WebAuthn credential transports are malformed.',
              );
            })();
    return {
      type: 'public-key',
      id: base64UrlToBytes(requiredString(entry, 'id')),
      ...(transports === undefined ? {} : { transports }),
    };
  });
}

function creationOptionsFromJson(
  options: Record<string, unknown>,
): PublicKeyCredentialCreationOptions {
  const user = requiredRecord(options, 'user');
  const excludeCredentials = decodeCredentialDescriptors(
    options.excludeCredentials,
  );
  return {
    ...(options as unknown as PublicKeyCredentialCreationOptions),
    challenge: base64UrlToBytes(requiredString(options, 'challenge')),
    user: {
      ...(user as unknown as PublicKeyCredentialUserEntity),
      id: base64UrlToBytes(requiredString(user, 'id')),
    },
    ...(excludeCredentials === undefined ? {} : { excludeCredentials }),
  };
}

function requestOptionsFromJson(
  options: Record<string, unknown>,
): PublicKeyCredentialRequestOptions {
  const allowCredentials = decodeCredentialDescriptors(options.allowCredentials);
  return {
    ...(options as unknown as PublicKeyCredentialRequestOptions),
    challenge: base64UrlToBytes(requiredString(options, 'challenge')),
    ...(allowCredentials === undefined ? {} : { allowCredentials }),
  };
}

function publicKeyCredential(value: Credential | null): PublicKeyCredential {
  if (!(value instanceof PublicKeyCredential)) {
    throw new WebAuthnBrowserError(
      'The browser did not return a public-key credential.',
    );
  }
  return value;
}

function authenticatorAttachment(
  credential: PublicKeyCredential,
): string | null | undefined {
  return credential.authenticatorAttachment ?? undefined;
}

function registrationResponse(
  credential: PublicKeyCredential,
): PasskeyRegistrationCompleteRequest['response'] {
  if (!(credential.response instanceof AuthenticatorAttestationResponse)) {
    throw new WebAuthnBrowserError(
      'The browser returned an unexpected registration response.',
    );
  }
  return {
    id: credential.id,
    rawId: bytesToBase64Url(credential.rawId),
    type: 'public-key',
    authenticatorAttachment: authenticatorAttachment(credential),
    clientExtensionResults: credential.getClientExtensionResults(),
    response: {
      attestationObject: bytesToBase64Url(
        credential.response.attestationObject,
      ),
      clientDataJSON: bytesToBase64Url(credential.response.clientDataJSON),
    },
  };
}

function assertionResponse(
  credential: PublicKeyCredential,
): PasskeyAuthenticationCompleteRequest['response'] {
  if (!(credential.response instanceof AuthenticatorAssertionResponse)) {
    throw new WebAuthnBrowserError(
      'The browser returned an unexpected assertion response.',
    );
  }
  return {
    id: credential.id,
    rawId: bytesToBase64Url(credential.rawId),
    type: 'public-key',
    authenticatorAttachment: authenticatorAttachment(credential),
    clientExtensionResults: credential.getClientExtensionResults(),
    response: {
      authenticatorData: bytesToBase64Url(credential.response.authenticatorData),
      clientDataJSON: bytesToBase64Url(credential.response.clientDataJSON),
      signature: bytesToBase64Url(credential.response.signature),
      userHandle:
        credential.response.userHandle === null
          ? null
          : bytesToBase64Url(credential.response.userHandle),
    },
  };
}

function ensureWebAuthnAvailable(): void {
  if (
    typeof window === 'undefined' ||
    typeof PublicKeyCredential === 'undefined' ||
    navigator.credentials === undefined
  ) {
    throw new WebAuthnBrowserError('Passkeys are not supported by this browser.');
  }
}

export function isWebAuthnAvailable(): boolean {
  return (
    typeof window !== 'undefined' &&
    typeof PublicKeyCredential !== 'undefined' &&
    navigator.credentials !== undefined
  );
}

export async function createPasskeyRegistrationEvidence({
  ceremony,
  label,
  signal,
}: Readonly<{
  ceremony: PasskeyCeremony;
  label: string;
  signal?: AbortSignal;
}>): Promise<PasskeyRegistrationCompleteRequest> {
  ensureWebAuthnAvailable();
  const credential = publicKeyCredential(
    await navigator.credentials.create({
      publicKey: creationOptionsFromJson(ceremony.options),
      ...(signal === undefined ? {} : { signal }),
    }),
  );
  const response = registrationResponse(credential);
  const attestation = credential.response as AuthenticatorAttestationResponse;
  const transports =
    typeof attestation.getTransports === 'function'
      ? attestation.getTransports()
      : [];
  return {
    webauthn_challenge_ref: ceremony.webauthn_challenge_ref,
    label,
    transports,
    response,
  };
}

export async function createPasskeyAuthenticationEvidence({
  ceremony,
  signal,
}: Readonly<{
  ceremony: PasskeyCeremony;
  signal?: AbortSignal;
}>): Promise<PasskeyAuthenticationCompleteRequest> {
  ensureWebAuthnAvailable();
  const credential = publicKeyCredential(
    await navigator.credentials.get({
      publicKey: requestOptionsFromJson(ceremony.options),
      ...(signal === undefined ? {} : { signal }),
    }),
  );
  return {
    webauthn_challenge_ref: ceremony.webauthn_challenge_ref,
    response: assertionResponse(credential),
  };
}

export async function createPasskeyReauthenticationEvidence({
  ceremony,
  signal,
}: Readonly<{
  ceremony: PasskeyCeremony;
  signal?: AbortSignal;
}>): Promise<PasskeyReauthenticationCompleteRequest> {
  return createPasskeyAuthenticationEvidence({ ceremony, signal });
}
