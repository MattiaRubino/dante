const GOOGLE_IDENTITY_SCRIPT_ID = 'dante-google-identity-services';
const GOOGLE_IDENTITY_SCRIPT_SRC = 'https://accounts.google.com/gsi/client';
const GOOGLE_PROMPT_TIMEOUT_MS = 60_000;
const APPLE_AUTHORIZATION_HOST = 'appleid.apple.com';

type GoogleCredentialResponse = Readonly<{
  credential?: string;
}>;

type GooglePromptMoment = Readonly<{
  isDismissedMoment?: () => boolean;
  isNotDisplayed?: () => boolean;
  isSkippedMoment?: () => boolean;
  getDismissedReason?: () => string;
  getNotDisplayedReason?: () => string;
  getSkippedReason?: () => string;
}>;

type GoogleIdentityConfiguration = Readonly<{
  client_id: string;
  callback: (response: GoogleCredentialResponse) => void;
  nonce: string;
  auto_select: false;
  cancel_on_tap_outside: true;
}>;

type GoogleAccountsId = Readonly<{
  initialize: (configuration: GoogleIdentityConfiguration) => void;
  prompt: (callback?: (notification: GooglePromptMoment) => void) => void;
  cancel?: () => void;
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

function abortedError(): DOMException {
  return new DOMException('The provider request was aborted.', 'AbortError');
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

function promptFailureReason(notification: GooglePromptMoment): string | null {
  if (notification.isNotDisplayed?.()) {
    return notification.getNotDisplayedReason?.() ?? 'not_displayed';
  }
  if (notification.isSkippedMoment?.()) {
    return notification.getSkippedReason?.() ?? 'skipped';
  }
  if (notification.isDismissedMoment?.()) {
    return notification.getDismissedReason?.() ?? 'dismissed';
  }
  return null;
}

export async function requestGoogleCredential({
  clientId,
  nonce,
  signal,
}: Readonly<{
  clientId: string;
  nonce: string;
  signal?: AbortSignal;
}>): Promise<string> {
  if (signal?.aborted) {
    throw abortedError();
  }
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
  if (signal?.aborted) {
    throw abortedError();
  }

  return new Promise<string>((resolve, reject) => {
    let settled = false;
    const finish = (callback: () => void) => {
      if (settled) {
        return;
      }
      settled = true;
      window.clearTimeout(timeoutId);
      signal?.removeEventListener('abort', abort);
      callback();
    };
    const abort = () => {
      google.cancel?.();
      finish(() => reject(abortedError()));
    };
    const timeoutId = window.setTimeout(() => {
      google.cancel?.();
      finish(() =>
        reject(
          new ProviderBrowserUnavailableError(
            'Google sign-in did not complete before the browser prompt expired.',
          ),
        ),
      );
    }, GOOGLE_PROMPT_TIMEOUT_MS);

    signal?.addEventListener('abort', abort, { once: true });

    google.initialize({
      client_id: clientId,
      nonce,
      auto_select: false,
      cancel_on_tap_outside: true,
      callback: (response) => {
        const credential = response.credential;
        if (typeof credential !== 'string' || credential.length === 0) {
          finish(() =>
            reject(
              new ProviderBrowserUnavailableError(
                'Google sign-in returned no credential evidence.',
              ),
            ),
          );
          return;
        }
        finish(() => resolve(credential));
      },
    });

    google.prompt((notification) => {
      const reason = promptFailureReason(notification);
      if (reason === null) {
        return;
      }
      finish(() =>
        reject(
          new ProviderBrowserUnavailableError(
            `Google sign-in browser prompt ended before authentication (${reason}).`,
          ),
        ),
      );
    });
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
