import { afterEach, describe, expect, it, vi } from 'vitest';

import {
  appleAuthenticationEnabledFromBuild,
  googleAuthenticationEnabledFromBuild,
  googleClientIdFromBuild,
  passkeyAuthenticationEnabledFromBuild,
  ProviderBrowserUnavailableError,
  redirectToAppleAuthorization,
  renderGoogleIdentityButton,
} from './web-auth-provider';

afterEach(() => {
  Reflect.deleteProperty(window, 'google');
  document.getElementById('dante-google-identity-services')?.remove();
  vi.unstubAllEnvs();
  vi.restoreAllMocks();
});

describe('Web Auth provider browser boundary', () => {
  it('derives presentation availability only from public build configuration', () => {
    vi.stubEnv('VITE_DANTE_GOOGLE_CLIENT_ID', ' google-client-id ');
    vi.stubEnv('VITE_DANTE_APPLE_ENABLED', 'true');
    vi.stubEnv('VITE_DANTE_PASSKEY_ENABLED', '1');

    expect(googleClientIdFromBuild()).toBe('google-client-id');
    expect(googleAuthenticationEnabledFromBuild()).toBe(true);
    expect(appleAuthenticationEnabledFromBuild()).toBe(true);
    expect(passkeyAuthenticationEnabledFromBuild()).toBe(true);

    vi.stubEnv('VITE_DANTE_GOOGLE_CLIENT_ID', '   ');
    vi.stubEnv('VITE_DANTE_APPLE_ENABLED', 'false');
    vi.stubEnv('VITE_DANTE_PASSKEY_ENABLED', 'off');

    expect(googleAuthenticationEnabledFromBuild()).toBe(false);
    expect(appleAuthenticationEnabledFromBuild()).toBe(false);
    expect(passkeyAuthenticationEnabledFromBuild()).toBe(false);
  });

  it('only redirects Apple authorization to the canonical HTTPS authority', () => {
    const assign = vi.fn();

    redirectToAppleAuthorization(
      'https://appleid.apple.com/auth/authorize?client_id=dante',
      { assign },
    );

    expect(assign).toHaveBeenCalledWith(
      'https://appleid.apple.com/auth/authorize?client_id=dante',
    );

    expect(() =>
      redirectToAppleAuthorization('http://appleid.apple.com/auth/authorize', {
        assign,
      }),
    ).toThrow(ProviderBrowserUnavailableError);
    expect(() =>
      redirectToAppleAuthorization(
        'https://appleid.apple.com.evil.example/auth/authorize',
        { assign },
      ),
    ).toThrow(ProviderBrowserUnavailableError);
    expect(assign).toHaveBeenCalledTimes(1);
  });

  it('initializes the official Google button with DANTE nonce and no auto-select', async () => {
    const initialize = vi.fn();
    const renderButton = vi.fn();
    const onCredential = vi.fn();
    const onError = vi.fn();

    Object.defineProperty(window, 'google', {
      configurable: true,
      value: {
        accounts: {
          id: { initialize, renderButton },
        },
      },
    });

    const container = document.createElement('div');
    await renderGoogleIdentityButton({
      container,
      clientId: 'google-client-id',
      nonce: 'dante-nonce',
      onCredential,
      onError,
    });

    expect(initialize).toHaveBeenCalledWith(
      expect.objectContaining({
        client_id: 'google-client-id',
        nonce: 'dante-nonce',
        auto_select: false,
        button_auto_select: false,
        cancel_on_tap_outside: true,
        use_fedcm_for_button: true,
      }),
    );
    expect(renderButton).toHaveBeenCalledWith(
      container,
      expect.objectContaining({
        type: 'standard',
        text: 'continue_with',
      }),
    );

    const configuration = initialize.mock.calls[0]?.[0] as {
      callback: (response: { credential?: string }) => void;
    };
    configuration.callback({ credential: 'provider-credential' });
    expect(onCredential).toHaveBeenCalledWith('provider-credential');

    configuration.callback({});
    expect(onError).toHaveBeenCalledWith(
      expect.any(ProviderBrowserUnavailableError),
    );
  });

  it('rejects Google rendering when build configuration or DANTE nonce is missing', async () => {
    const container = document.createElement('div');
    const onCredential = vi.fn();
    const onError = vi.fn();

    await expect(
      renderGoogleIdentityButton({
        container,
        clientId: '   ',
        nonce: 'nonce',
        onCredential,
        onError,
      }),
    ).rejects.toThrow('not configured');

    await expect(
      renderGoogleIdentityButton({
        container,
        clientId: 'client-id',
        nonce: '',
        onCredential,
        onError,
      }),
    ).rejects.toThrow('did not receive a DANTE nonce');
  });
});
