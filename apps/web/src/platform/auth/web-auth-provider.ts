const GOOGLE_IDENTITY_SCRIPT_ID = 'dante-google-identity-services';
const GOOGLE_IDENTITY_SCRIPT_SRC = 'https://accounts.google.com/gsi/client';
const APPLE_AUTHORIZATION_HOST = 'appleid.apple.com';

type GoogleCredentialResponse = Readonly<{
  credential?: string;
}>;

type GoogleIdentityConfiguration = Readonly<{
  client_id: string;
  callback: (response: GoogleCredentialResponse) => void;
  nonce: string;
  auto_select: false;
  cancel_on_tap_outside: true;
  use_fedcm_for_button: true;
  button_auto_select: false;
}>;

type GoogleButtonConfiguration = Readonly<{
  type: 'standard';
  theme: 'outline';
  size: 'large';
  text: 'continue_with';
  shape: 'rectangular';
  logo_alignment: 'left';
  width?: number;
}>;

type GoogleAccountsId = Readonly<{
  initialize: (configuration: GoogleIdentityConfiguration) => void;
  renderButton: (
    parent: HTMLElement,
    configuration: GoogleButtonConfiguration,
  ) => void;
}>;

type GoogleIdentityGlobal = Readonly<{
  accounts: Readonly<{
    id: GoogleAccountsId;
  }>;
}>;

type GoogleWindow = Window &
  typeof globalThis & {
    google?: GoogleIdentityGlobal;
  };

let googleScriptPromise: Promise<GoogleAccountsId> | null = null;

export class ProviderBrowserUnavailableError extends Error {
  constructor(message: string) {
    super(message);
    this.name = 'ProviderBrowserUnavailableError';
  }
}

function googleAccountsId(): GoogleAccountsId | null {
  if (typeof window === 'undefined') {
    return null;
  }
  return (window as GoogleWindow).google?.accounts.id ?? null;
}

function removeFailedScript(script: HTMLScriptElement): void {
  if (script.parentNode !== null) {
    script.parentNode.removeChild(script);
  }
}

export function loadGoogleIdentityServices(): Promise<GoogleAccountsId> {
  const existing = googleAccountsId();
  if (existing !== null) {
    return Promise.resolve(existing);
  }
  if (typeof document === 'undefined') {
    return Promise.reject(
      new ProviderBrowserUnavailableError(
        'Google Identity Services requires a browser document.',
      ),
    );
  }
  if (googleScriptPromise !== null) {
    return googleScriptPromise;
  }

  googleScriptPromise = new Promise<GoogleAccountsId>((resolve, reject) => {
    const current = document.getElementById(GOOGLE_IDENTITY_SCRIPT_ID);
    const script =
      current instanceof HTMLScriptElement
        ? current
        : Object.assign(document.createElement('script'), {
            id: GOOGLE_IDENTITY_SCRIPT_ID,
            src: GOOGLE_IDENTITY_SCRIPT_SRC,
            async: true,
            defer: true,
          });

    const cleanup = () => {
      script.removeEventListener('load', loaded);
      script.removeEventListener('error', failed);
    };
    const loaded = () => {
      cleanup();
      const api = googleAccountsId();
      if (api === null) {
        googleScriptPromise = null;
        reject(
          new ProviderBrowserUnavailableError(
            'Google Identity Services loaded without exposing its browser API.',
          ),
        );
        return;
      }
      resolve(api);
    };
    const failed = () => {
      cleanup();
      googleScriptPromise = null;
      removeFailedScript(script);
      reject(
        new ProviderBrowserUnavailableError(
          'Google Identity Services could not be loaded.',
        ),
      );
    };

    script.addEventListener('load', loaded, { once: true });
    script.addEventListener('error', failed, { once: true });
    if (current === null) {
      document.head.appendChild(script);
    }
  });

  return googleScriptPromise;
}

export function googleClientIdFromBuild(): string {
  const value = import.meta.env.VITE_DANTE_GOOGLE_CLIENT_ID;
  return typeof value === 'string' ? value.trim() : '';
}

export async function renderGoogleIdentityButton({
  container,
  clientId,
  nonce,
  onCredential,
  onError,
}: Readonly<{
  container: HTMLElement;
  clientId: string;
  nonce: string;
  onCredential: (credential: string) => void;
  onError: (error: ProviderBrowserUnavailableError) => void;
}>): Promise<void> {
  if (clientId.trim().length === 0) {
    throw new ProviderBrowserUnavailableError(
      'Google sign-in is not configured for this build.',
    );
  }
  if (nonce.length === 0) {
    throw new ProviderBrowserUnavailableError(
      'Google sign-in did not receive a DANTE nonce.',
    );
  }

  const google = await loadGoogleIdentityServices();
  container.replaceChildren();
  google.initialize({
    client_id: clientId,
    nonce,
    auto_select: false,
    cancel_on_tap_outside: true,
    use_fedcm_for_button: true,
    button_auto_select: false,
    callback: (response) => {
      const credential = response.credential;
      if (typeof credential !== 'string' || credential.length === 0) {
        onError(
          new ProviderBrowserUnavailableError(
            'Google sign-in returned no credential evidence.',
          ),
        );
        return;
      }
      onCredential(credential);
    },
  });
  const width = Math.floor(container.getBoundingClientRect().width);
  google.renderButton(container, {
    type: 'standard',
    theme: 'outline',
    size: 'large',
    text: 'continue_with',
    shape: 'rectangular',
    logo_alignment: 'left',
    ...(width > 0 ? { width } : {}),
  });
}

export function redirectToAppleAuthorization(
  authorizationUrl: string,
  location: Pick<Location, 'assign'> = window.location,
): void {
  const parsed = new URL(authorizationUrl);
  if (
    parsed.protocol !== 'https:' ||
    parsed.hostname.toLowerCase() !== APPLE_AUTHORIZATION_HOST
  ) {
    throw new ProviderBrowserUnavailableError(
      'Apple authorization returned an unexpected redirect authority.',
    );
  }
  location.assign(parsed.toString());
}
