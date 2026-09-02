import type { ReactNode } from 'react';
import {
  act,
  cleanup,
  fireEvent,
  render,
  screen,
} from '@testing-library/react';
import {
  afterEach,
  beforeAll,
  beforeEach,
  describe,
  expect,
  it,
  vi,
} from 'vitest';

vi.mock('@tanstack/react-router', () => ({
  Link: ({
    children,
    to,
    className,
  }: {
    children: ReactNode;
    to: string;
    className?: string;
  }) => (
    <a href={to} className={className}>
      {children}
    </a>
  ),
}));

vi.mock('../application/auth-methods', () => ({
  useAuthenticationMethodsQuery: vi.fn(),
  useEstablishPasswordMutation: vi.fn(),
  useRemovePasswordMutation: vi.fn(),
}));

vi.mock('../application/auth-passkey', () => ({
  usePasskeyReauthenticationMutation: vi.fn(),
  usePasskeyRegistrationMutation: vi.fn(),
  useRemovePasskeyMutation: vi.fn(),
  useUpdatePasskeyMutation: vi.fn(),
}));

vi.mock('../application/auth-provider', () => ({
  useAppleAuthenticationMutation: vi.fn(),
  useCompleteGoogleAuthenticationMutation: vi.fn(),
  usePrepareGoogleAuthenticationMutation: vi.fn(),
  useUnlinkProviderMutation: vi.fn(),
}));

vi.mock('../application/auth-session', () => ({
  isAuthenticatedAccessSession: vi.fn(
    (session: { authenticated?: boolean } | undefined) =>
      session?.authenticated === true,
  ),
  useAuthSessionQuery: vi.fn(),
}));

vi.mock('../application/auth-lifecycle', () => ({
  useReauthenticateMutation: vi.fn(),
}));

import { i18n } from '../../../bootstrap/i18n';
import { WebAuthRemoteError } from '../../../platform/auth/web-auth-remote';
import {
  useAuthenticationMethodsQuery,
  useEstablishPasswordMutation,
  useRemovePasswordMutation,
} from '../application/auth-methods';
import {
  usePasskeyReauthenticationMutation,
  usePasskeyRegistrationMutation,
  useRemovePasskeyMutation,
  useUpdatePasskeyMutation,
} from '../application/auth-passkey';
import {
  useAppleAuthenticationMutation,
  useCompleteGoogleAuthenticationMutation,
  usePrepareGoogleAuthenticationMutation,
  useUnlinkProviderMutation,
} from '../application/auth-provider';
import { useAuthSessionQuery } from '../application/auth-session';
import { useReauthenticateMutation } from '../application/auth-lifecycle';
import { AccessSecurityPage } from './access-security-page';

type MutationMock = Readonly<{
  mutate: ReturnType<typeof vi.fn>;
  isPending: boolean;
}>;

function mutationMock(): MutationMock {
  return { mutate: vi.fn(), isPending: false };
}

const authenticatedSession = {
  authenticated: true as const,
  account_ref: '00000000-0000-4000-8000-000000000001',
  auth_session_ref: '00000000-0000-4000-8000-000000000002',
  recent_auth_at: '2026-09-02T07:30:00Z',
  expires_at: '2026-10-02T07:30:00Z',
  csrf_token: 'current-session-csrf',
};

let methodsRefetch: ReturnType<typeof vi.fn>;
let establishPasswordMutation: MutationMock;
let removePasswordMutation: MutationMock;
let prepareGoogleMutation: MutationMock;
let completeGoogleMutation: MutationMock;
let appleMutation: MutationMock;
let unlinkProviderMutation: MutationMock;
let registerPasskeyMutation: MutationMock;
let updatePasskeyMutation: MutationMock;
let removePasskeyMutation: MutationMock;
let passwordReauthMutation: MutationMock;
let passkeyReauthMutation: MutationMock;

function setMethods(methods: unknown): void {
  methodsRefetch = vi.fn().mockResolvedValue({ data: methods });
  vi.mocked(useAuthenticationMethodsQuery).mockReturnValue({
    data: methods,
    isPending: false,
    isError: false,
    error: null,
    refetch: methodsRefetch,
  } as never);
}

beforeAll(async () => {
  await i18n.changeLanguage('it');
});

beforeEach(() => {
  vi.clearAllMocks();
  vi.stubEnv('VITE_DANTE_GOOGLE_CLIENT_ID', 'google-client-id');
  vi.stubEnv('VITE_DANTE_APPLE_ENABLED', 'true');
  vi.stubEnv('VITE_DANTE_PASSKEY_ENABLED', 'true');

  establishPasswordMutation = mutationMock();
  removePasswordMutation = mutationMock();
  prepareGoogleMutation = mutationMock();
  completeGoogleMutation = mutationMock();
  appleMutation = mutationMock();
  unlinkProviderMutation = mutationMock();
  registerPasskeyMutation = mutationMock();
  updatePasskeyMutation = mutationMock();
  removePasskeyMutation = mutationMock();
  passwordReauthMutation = mutationMock();
  passkeyReauthMutation = mutationMock();

  vi.mocked(useAuthSessionQuery).mockReturnValue({
    data: authenticatedSession,
    isPending: false,
  } as never);
  setMethods({ password_established: false, providers: [], passkeys: [] });

  vi.mocked(useEstablishPasswordMutation).mockReturnValue(
    establishPasswordMutation as never,
  );
  vi.mocked(useRemovePasswordMutation).mockReturnValue(
    removePasswordMutation as never,
  );
  vi.mocked(usePrepareGoogleAuthenticationMutation).mockReturnValue(
    prepareGoogleMutation as never,
  );
  vi.mocked(useCompleteGoogleAuthenticationMutation).mockReturnValue(
    completeGoogleMutation as never,
  );
  vi.mocked(useAppleAuthenticationMutation).mockReturnValue(
    appleMutation as never,
  );
  vi.mocked(useUnlinkProviderMutation).mockReturnValue(
    unlinkProviderMutation as never,
  );
  vi.mocked(usePasskeyRegistrationMutation).mockReturnValue(
    registerPasskeyMutation as never,
  );
  vi.mocked(useUpdatePasskeyMutation).mockReturnValue(
    updatePasskeyMutation as never,
  );
  vi.mocked(useRemovePasskeyMutation).mockReturnValue(
    removePasskeyMutation as never,
  );
  vi.mocked(useReauthenticateMutation).mockReturnValue(
    passwordReauthMutation as never,
  );
  vi.mocked(usePasskeyReauthenticationMutation).mockReturnValue(
    passkeyReauthMutation as never,
  );
});

afterEach(() => {
  cleanup();
  vi.unstubAllEnvs();
});

describe('AccessSecurityPage', () => {
  it('keeps account security behind an authenticated DANTE session', () => {
    vi.mocked(useAuthSessionQuery).mockReturnValue({
      data: { authenticated: false },
      isPending: false,
    } as never);

    render(<AccessSecurityPage />);

    expect(
      screen.getByRole('heading', {
        name: 'Accedi per gestire la sicurezza dell’account.',
      }),
    ).toBeTruthy();
    expect(
      screen.getByRole('link', { name: 'Accedi' }).getAttribute('href'),
    ).toBe('/');
    expect(useAuthenticationMethodsQuery).toHaveBeenCalledWith(false);
  });

  it('binds password enrollment, provider linking, passkey management, and passkey reauthentication to current CSRF authority', () => {
    setMethods({
      password_established: false,
      providers: [],
      passkeys: [
        {
          passkey_credential_ref: '00000000-0000-4000-8000-000000000003',
          label: 'Laptop',
          transports: ['internal'],
        },
      ],
    });

    render(<AccessSecurityPage />);

    expect(screen.queryByPlaceholderText('Password')).toBeNull();

    fireEvent.change(screen.getByPlaceholderText('Nuova password'), {
      target: { value: 'correct horse battery staple' },
    });
    fireEvent.click(screen.getByRole('button', { name: 'Aggiungi password' }));
    expect(establishPasswordMutation.mutate).toHaveBeenCalledWith(
      {
        newPassword: 'correct horse battery staple',
        csrfToken: 'current-session-csrf',
      },
      expect.any(Object),
    );

    fireEvent.click(screen.getByRole('button', { name: 'Collega Google' }));
    expect(prepareGoogleMutation.mutate).toHaveBeenCalledWith(
      {
        purpose: 'link',
        returnTarget: 'security',
        csrfToken: 'current-session-csrf',
      },
      expect.any(Object),
    );

    fireEvent.click(screen.getByRole('button', { name: 'Collega Apple' }));
    expect(appleMutation.mutate).toHaveBeenCalledWith(
      {
        purpose: 'link',
        returnTarget: 'security',
        csrfToken: 'current-session-csrf',
      },
      expect.any(Object),
    );

    const passkeyLabel =
      screen.getByLabelText<HTMLInputElement>('Nome passkey');
    expect(passkeyLabel.placeholder).toBe('Es. Portatile personale');
    fireEvent.change(passkeyLabel, { target: { value: ' Work laptop ' } });
    fireEvent.click(screen.getByRole('button', { name: 'Aggiungi passkey' }));
    expect(registerPasskeyMutation.mutate).toHaveBeenCalledWith(
      { label: 'Work laptop', csrfToken: 'current-session-csrf' },
      expect.any(Object),
    );

    fireEvent.click(
      screen.getByRole('button', { name: 'Conferma con passkey' }),
    );
    expect(passkeyReauthMutation.mutate).toHaveBeenCalledWith(
      { csrfToken: 'current-session-csrf' },
      expect.any(Object),
    );

    fireEvent.click(screen.getByRole('button', { name: 'Rinomina' }));
    const editingLabel = screen.getByDisplayValue<HTMLInputElement>('Laptop');
    fireEvent.change(editingLabel, { target: { value: 'Office key' } });
    fireEvent.click(screen.getByRole('button', { name: 'Salva' }));
    expect(updatePasskeyMutation.mutate).toHaveBeenCalledWith(
      {
        passkeyCredentialRef: '00000000-0000-4000-8000-000000000003',
        label: 'Office key',
        csrfToken: 'current-session-csrf',
      },
      expect.any(Object),
    );

    fireEvent.click(screen.getByRole('button', { name: 'Rimuovi' }));
    expect(removePasskeyMutation.mutate).toHaveBeenCalledWith(
      {
        passkeyCredentialRef: '00000000-0000-4000-8000-000000000003',
        csrfToken: 'current-session-csrf',
      },
      expect.any(Object),
    );
  });

  it('offers password reauthentication only when the account actually has a password', () => {
    setMethods({ password_established: true, providers: [], passkeys: [] });

    render(<AccessSecurityPage />);

    fireEvent.change(screen.getByPlaceholderText('Password'), {
      target: { value: 'current password' },
    });
    fireEvent.click(
      screen.getByRole('button', { name: 'Conferma con password' }),
    );
    expect(passwordReauthMutation.mutate).toHaveBeenCalledWith(
      { password: 'current password', csrfToken: 'current-session-csrf' },
      expect.any(Object),
    );
  });

  it('uses linked Google and Apple as real reauthentication methods for provider-only accounts', () => {
    setMethods({
      password_established: false,
      providers: [
        {
          provider_code: 'google',
          provider_email_address: 'person@example.com',
          external_identity_ref: '00000000-0000-4000-8000-000000000004',
        },
        {
          provider_code: 'apple',
          provider_email_address: 'person@privaterelay.appleid.com',
          external_identity_ref: '00000000-0000-4000-8000-000000000005',
        },
      ],
      passkeys: [],
    });

    render(<AccessSecurityPage />);

    expect(screen.queryByPlaceholderText('Password')).toBeNull();
    expect(screen.queryByRole('button', { name: 'Collega Google' })).toBeNull();
    expect(screen.queryByRole('button', { name: 'Collega Apple' })).toBeNull();

    fireEvent.click(
      screen.getByRole('button', { name: 'Continua con Google' }),
    );
    expect(prepareGoogleMutation.mutate).toHaveBeenCalledWith(
      {
        purpose: 'reauthenticate',
        returnTarget: 'security',
        csrfToken: 'current-session-csrf',
      },
      expect.any(Object),
    );

    fireEvent.click(screen.getByRole('button', { name: 'Continua con Apple' }));
    expect(appleMutation.mutate).toHaveBeenCalledWith(
      {
        purpose: 'reauthenticate',
        returnTarget: 'security',
        csrfToken: 'current-session-csrf',
      },
      expect.any(Object),
    );
  });

  it('surfaces localized anti-lockout reauthentication requirements while wiring removal to session authority', () => {
    setMethods({
      password_established: true,
      providers: [
        {
          provider_code: 'google',
          provider_email_address: 'person@example.com',
          external_identity_ref: '00000000-0000-4000-8000-000000000004',
        },
      ],
      passkeys: [],
    });

    render(<AccessSecurityPage />);

    fireEvent.click(screen.getByRole('button', { name: 'Rimuovi password' }));
    expect(removePasswordMutation.mutate).toHaveBeenCalledWith(
      { csrfToken: 'current-session-csrf' },
      expect.any(Object),
    );

    fireEvent.click(screen.getByRole('button', { name: 'Rimuovi' }));
    expect(unlinkProviderMutation.mutate).toHaveBeenCalledWith(
      {
        externalIdentityRef: '00000000-0000-4000-8000-000000000004',
        csrfToken: 'current-session-csrf',
      },
      expect.any(Object),
    );

    const removalOptions = removePasswordMutation.mutate.mock.calls[0]?.[1] as {
      onError: (error: unknown) => void;
    };
    act(() => {
      removalOptions.onError(
        new WebAuthRemoteError({
          kind: 'server_problem',
          code: 'auth.reauthentication_required',
        } as never),
      );
    });

    const alert = screen.getByRole('alert');
    expect(alert.textContent).toContain(
      'Conferma di nuovo la tua identità prima di modificare le impostazioni di sicurezza.',
    );
    expect(alert.textContent).toContain(
      'Aggiorna la conferma della tua identità, poi ripeti l’operazione.',
    );
  });

  it('does not offer browser methods that the build has disabled', () => {
    vi.stubEnv('VITE_DANTE_GOOGLE_CLIENT_ID', '');
    vi.stubEnv('VITE_DANTE_APPLE_ENABLED', 'false');
    vi.stubEnv('VITE_DANTE_PASSKEY_ENABLED', 'false');
    setMethods({ password_established: true, providers: [], passkeys: [] });

    render(<AccessSecurityPage />);

    expect(screen.queryByRole('button', { name: 'Collega Google' })).toBeNull();
    expect(screen.queryByRole('button', { name: 'Collega Apple' })).toBeNull();
    expect(
      screen.queryByRole('button', { name: 'Conferma con passkey' }),
    ).toBeNull();
    expect(
      screen.queryByRole('button', { name: 'Aggiungi passkey' }),
    ).toBeNull();
  });

  it('does not invent authenticator controls while the authoritative methods query is pending', () => {
    methodsRefetch = vi.fn();
    vi.mocked(useAuthenticationMethodsQuery).mockReturnValue({
      data: undefined,
      isPending: true,
      isError: false,
      error: null,
      refetch: methodsRefetch,
    } as never);

    render(<AccessSecurityPage />);

    expect(
      screen.getByText('Caricamento delle impostazioni di sicurezza…'),
    ).toBeTruthy();
    expect(
      screen.queryByRole('button', { name: 'Aggiungi password' }),
    ).toBeNull();
    expect(screen.queryByRole('button', { name: 'Collega Google' })).toBeNull();
    expect(
      screen.queryByRole('button', { name: 'Aggiungi passkey' }),
    ).toBeNull();
  });

  it('surfaces methods-query failure without guessing account security state and allows retry', () => {
    methodsRefetch = vi.fn().mockResolvedValue({});
    vi.mocked(useAuthenticationMethodsQuery).mockReturnValue({
      data: undefined,
      isPending: false,
      isError: true,
      error: new WebAuthRemoteError({ kind: 'network_unavailable' } as never),
      refetch: methodsRefetch,
    } as never);

    render(<AccessSecurityPage />);

    expect(screen.getByRole('alert').textContent).toContain(
      'Il servizio Access non è raggiungibile.',
    );
    expect(
      screen.queryByRole('button', { name: 'Aggiungi password' }),
    ).toBeNull();

    fireEvent.click(screen.getByRole('button', { name: 'Riprova' }));
    expect(methodsRefetch).toHaveBeenCalledTimes(1);
  });
});
