import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';

import {
  createPasskeyAuthenticationEvidence,
  createPasskeyRegistrationEvidence,
  WebAuthnBrowserError,
} from './web-auth-webauthn';

function buffer(...bytes: number[]): ArrayBuffer {
  return Uint8Array.from(bytes).buffer;
}

function byteValues(value: BufferSource | undefined): number[] {
  if (value === undefined) {
    return [];
  }
  const bytes =
    value instanceof ArrayBuffer
      ? new Uint8Array(value)
      : new Uint8Array(value.buffer, value.byteOffset, value.byteLength);
  return Array.from(bytes);
}

class FakeAuthenticatorAttestationResponse {
  constructor(
    readonly attestationObject: ArrayBuffer,
    readonly clientDataJSON: ArrayBuffer,
  ) {}

  getTransports(): AuthenticatorTransport[] {
    return ['internal'];
  }
}

class FakeAuthenticatorAssertionResponse {
  constructor(
    readonly authenticatorData: ArrayBuffer,
    readonly clientDataJSON: ArrayBuffer,
    readonly signature: ArrayBuffer,
    readonly userHandle: ArrayBuffer | null,
  ) {}
}

class FakePublicKeyCredential {
  readonly id = 'credential-id';
  readonly type = 'public-key';
  readonly authenticatorAttachment = 'platform';

  constructor(
    readonly rawId: ArrayBuffer,
    readonly response:
      | FakeAuthenticatorAttestationResponse
      | FakeAuthenticatorAssertionResponse,
  ) {}

  getClientExtensionResults() {
    return { credProps: { rk: true } };
  }
}

let credentialsDescriptor: PropertyDescriptor | undefined;

function installCredentials(
  create: (options: CredentialCreationOptions) => Promise<Credential | null>,
  get: (options: CredentialRequestOptions) => Promise<Credential | null>,
): void {
  Object.defineProperty(navigator, 'credentials', {
    configurable: true,
    value: { create, get },
  });
}

beforeEach(() => {
  credentialsDescriptor = Object.getOwnPropertyDescriptor(navigator, 'credentials');
  vi.stubGlobal('PublicKeyCredential', FakePublicKeyCredential);
  vi.stubGlobal(
    'AuthenticatorAttestationResponse',
    FakeAuthenticatorAttestationResponse,
  );
  vi.stubGlobal(
    'AuthenticatorAssertionResponse',
    FakeAuthenticatorAssertionResponse,
  );
});

afterEach(() => {
  if (credentialsDescriptor === undefined) {
    Reflect.deleteProperty(navigator, 'credentials');
  } else {
    Object.defineProperty(navigator, 'credentials', credentialsDescriptor);
  }
  vi.unstubAllGlobals();
  vi.restoreAllMocks();
});

describe('WebAuthn browser serialization boundary', () => {
  it('decodes backend creation options and serializes registration evidence back to Base64URL', async () => {
    const credential = new FakePublicKeyCredential(
      buffer(10, 11),
      new FakeAuthenticatorAttestationResponse(buffer(12, 13), buffer(14, 15)),
    );
    const createMock = vi.fn((_options: CredentialCreationOptions) =>
      Promise.resolve(credential as unknown as Credential),
    );
    const getMock = vi.fn((_options: CredentialRequestOptions) =>
      Promise.resolve(null),
    );
    installCredentials(createMock, getMock);
    const signal = new AbortController().signal;

    const result = await createPasskeyRegistrationEvidence({
      ceremony: {
        webauthn_challenge_ref: '00000000-0000-4000-8000-000000000001',
        options: {
          challenge: 'AQID',
          rp: { name: 'DANTE' },
          user: {
            id: 'BAUG',
            name: 'person@example.com',
            displayName: 'Person',
          },
          pubKeyCredParams: [{ type: 'public-key', alg: -7 }],
          excludeCredentials: [
            { type: 'public-key', id: 'BwgJ', transports: ['internal'] },
          ],
        },
      } as never,
      label: 'Laptop',
      signal,
    });

    const creation = createMock.mock.calls[0]?.[0];
    expect(byteValues(creation?.publicKey?.challenge)).toEqual([1, 2, 3]);
    expect(byteValues(creation?.publicKey?.user.id)).toEqual([4, 5, 6]);
    expect(
      byteValues(creation?.publicKey?.excludeCredentials?.[0]?.id),
    ).toEqual([7, 8, 9]);
    expect(creation?.signal).toBe(signal);
    expect(result).toEqual({
      webauthn_challenge_ref: '00000000-0000-4000-8000-000000000001',
      label: 'Laptop',
      transports: ['internal'],
      response: {
        id: 'credential-id',
        rawId: 'Cgs',
        type: 'public-key',
        authenticatorAttachment: 'platform',
        clientExtensionResults: { credProps: { rk: true } },
        response: {
          attestationObject: 'DA0',
          clientDataJSON: 'Dg8',
        },
      },
    });
  });

  it('decodes request allowCredentials and preserves assertion userHandle semantics', async () => {
    const credential = new FakePublicKeyCredential(
      buffer(10, 11),
      new FakeAuthenticatorAssertionResponse(
        buffer(16, 17),
        buffer(14, 15),
        buffer(18, 19),
        buffer(20, 21),
      ),
    );
    const createMock = vi.fn((_options: CredentialCreationOptions) =>
      Promise.resolve(null),
    );
    const getMock = vi.fn((_options: CredentialRequestOptions) =>
      Promise.resolve(credential as unknown as Credential),
    );
    installCredentials(createMock, getMock);
    const signal = new AbortController().signal;

    const result = await createPasskeyAuthenticationEvidence({
      ceremony: {
        webauthn_challenge_ref: '00000000-0000-4000-8000-000000000002',
        options: {
          challenge: 'AQID',
          allowCredentials: [
            { type: 'public-key', id: 'BwgJ', transports: ['internal'] },
          ],
        },
      } as never,
      signal,
    });

    const request = getMock.mock.calls[0]?.[0];
    expect(byteValues(request?.publicKey?.challenge)).toEqual([1, 2, 3]);
    expect(byteValues(request?.publicKey?.allowCredentials?.[0]?.id)).toEqual([
      7, 8, 9,
    ]);
    expect(request?.signal).toBe(signal);
    expect(result).toEqual({
      webauthn_challenge_ref: '00000000-0000-4000-8000-000000000002',
      response: {
        id: 'credential-id',
        rawId: 'Cgs',
        type: 'public-key',
        authenticatorAttachment: 'platform',
        clientExtensionResults: { credProps: { rk: true } },
        response: {
          authenticatorData: 'EBE',
          clientDataJSON: 'Dg8',
          signature: 'EhM',
          userHandle: 'FBU',
        },
      },
    });
  });

  it('rejects malformed backend binary fields before invoking the browser credential API', async () => {
    const createMock = vi.fn((_options: CredentialCreationOptions) =>
      Promise.resolve(null),
    );
    const getMock = vi.fn((_options: CredentialRequestOptions) =>
      Promise.resolve(null),
    );
    installCredentials(createMock, getMock);

    await expect(
      createPasskeyAuthenticationEvidence({
        ceremony: {
          webauthn_challenge_ref: '00000000-0000-4000-8000-000000000003',
          options: { challenge: 'not base64url!' },
        } as never,
      }),
    ).rejects.toBeInstanceOf(WebAuthnBrowserError);
    expect(getMock).not.toHaveBeenCalled();
  });
});
