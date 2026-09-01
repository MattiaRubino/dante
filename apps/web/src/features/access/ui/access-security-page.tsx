import { useMemo, useState, type FormEvent } from 'react';
import { Link } from '@tanstack/react-router';
import { useTranslation } from 'react-i18next';

import type { ProviderBrowserUnavailableError } from '../../../platform/auth/web-auth-provider';
import { WebAuthRemoteError } from '../../../platform/auth/web-auth-remote';
import {
  useEstablishPasswordMutation,
  useAuthenticationMethodsQuery,
  useRemovePasswordMutation,
} from '../application/auth-methods';
import {
  usePasskeyReauthenticationMutation,
  usePasskeyRegistrationMutation,
  useRemovePasskeyMutation,
  useUpdatePasskeyMutation,
} from '../application/auth-passkey';
import {
  type GoogleAuthenticationPreparation,
  useAppleAuthenticationMutation,
  useCompleteGoogleAuthenticationMutation,
  usePrepareGoogleAuthenticationMutation,
  useUnlinkProviderMutation,
} from '../application/auth-provider';
import { useAuthSessionQuery } from '../application/auth-session';
import { useReauthenticateMutation } from '../application/auth-lifecycle';
import { isValidNewPassword } from '../model/access-flow';
import { GoogleIdentityButton } from './provider-button';
import '../access.css';
import '../access-security.css';

type SecurityError = Readonly<{
  message: string;
  reauthenticationRequired: boolean;
}>;

function securityError(error: unknown): SecurityError {
  if (!(error instanceof WebAuthRemoteError)) {
    return {
      message: 'The security operation could not be completed.',
      reauthenticationRequired: false,
    };
  }
  const failure = error.failure;
  if (failure.kind !== 'server_problem') {
    return {
      message:
        failure.kind === 'network_unavailable'
          ? 'The Access service is unreachable.'
          : 'The security operation could not be completed.',
      reauthenticationRequired: false,
    };
  }
  switch (failure.code) {
    case 'auth.reauthentication_required':
      return {
        message: 'Confirm your identity again before changing security settings.',
        reauthenticationRequired: true,
      };
    case 'auth.authenticator_removal_blocked':
      return {
        message:
          'DANTE blocked this removal because it would leave the account without a safe authenticator.',
        reauthenticationRequired: false,
      };
    case 'auth.password_already_established':
      return {
        message: 'This account already has a password.',
        reauthenticationRequired: false,
      };
    case 'auth.passkey_already_registered':
      return {
        message: 'That passkey is already registered with DANTE.',
        reauthenticationRequired: false,
      };
    case 'auth.passkey_not_found':
      return {
        message: 'That passkey is no longer active on this account.',
        reauthenticationRequired: false,
      };
    case 'dependency.provider_unavailable':
    case 'service.unavailable':
      return {
        message: 'The authentication service is temporarily unavailable.',
        reauthenticationRequired: false,
      };
    default:
      return {
        message: failure.problem.detail,
        reauthenticationRequired: false,
      };
  }
}

export function AccessSecurityPage() {
  const { t } = useTranslation('common');
  const sessionQuery = useAuthSessionQuery();
  const authenticated = sessionQuery.data?.authenticated === true;
  const methodsQuery = useAuthenticationMethodsQuery(authenticated);
  const establishPasswordMutation = useEstablishPasswordMutation();
  const removePasswordMutation = useRemovePasswordMutation();
  const prepareGoogleMutation = usePrepareGoogleAuthenticationMutation();
  const completeGoogleMutation = useCompleteGoogleAuthenticationMutation();
  const appleMutation = useAppleAuthenticationMutation();
  const unlinkProviderMutation = useUnlinkProviderMutation();
  const registerPasskeyMutation = usePasskeyRegistrationMutation();
  const updatePasskeyMutation = useUpdatePasskeyMutation();
  const removePasskeyMutation = useRemovePasskeyMutation();
  const passwordReauthMutation = useReauthenticateMutation();
  const passkeyReauthMutation = usePasskeyReauthenticationMutation();

  const [newPassword, setNewPassword] = useState('');
  const [passkeyLabel, setPasskeyLabel] = useState('My passkey');
  const [passwordReauth, setPasswordReauth] = useState('');
  const [editingPasskeyRef, setEditingPasskeyRef] = useState<string | null>(null);
  const [editingPasskeyLabel, setEditingPasskeyLabel] = useState('');
  const [googlePreparation, setGooglePreparation] =
    useState<GoogleAuthenticationPreparation | null>(null);
  const [lastError, setLastError] = useState<SecurityError | null>(null);
  const [successMessage, setSuccessMessage] = useState<string | null>(null);

  const session = authenticated ? sessionQuery.data : null;
  const csrfToken = session?.csrf_token ?? null;
  const methods = methodsQuery.data;
  const providerCodes = useMemo(
    () => new Set(methods?.providers.map((provider) => provider.provider_code) ?? []),
    [methods?.providers],
  );

  function clearFeedback() {
    setLastError(null);
    setSuccessMessage(null);
  }

  function handleError(error: unknown) {
    setSuccessMessage(null);
    setLastError(securityError(error));
  }

  function handleProviderBrowserError(_error: ProviderBrowserUnavailableError) {
    setSuccessMessage(null);
    setLastError({
      message: 'The Google authentication control could not be initialized.',
      reauthenticationRequired: false,
    });
  }

  async function refreshMethods() {
    await methodsQuery.refetch();
  }

  function submitPassword(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    clearFeedback();
    if (csrfToken === null) {
      setLastError({
        message: 'Your session is no longer available.',
        reauthenticationRequired: false,
      });
      return;
    }
    if (!isValidNewPassword(newPassword)) {
      setLastError({
        message: t(($) => $.common.access.validation.passwordMinimum),
        reauthenticationRequired: false,
      });
      return;
    }
    establishPasswordMutation.mutate(
      { newPassword, csrfToken },
      {
        onSuccess: () => {
          setNewPassword('');
          setSuccessMessage(t(($) => $.common.access.security.passwordAdded));
        },
        onError: handleError,
      },
    );
  }

  function removePassword() {
    clearFeedback();
    if (csrfToken === null) {
      return;
    }
    removePasswordMutation.mutate(
      { csrfToken },
      {
        onSuccess: () =>
          setSuccessMessage(t(($) => $.common.access.security.passwordRemoved)),
        onError: handleError,
      },
    );
  }

  function prepareGoogleLink() {
    clearFeedback();
    if (csrfToken === null || prepareGoogleMutation.isPending) {
      return;
    }
    setGooglePreparation(null);
    prepareGoogleMutation.mutate(
      {
        purpose: 'link',
        returnTarget: 'security',
        csrfToken,
      },
      {
        onSuccess: setGooglePreparation,
        onError: handleError,
      },
    );
  }

  function completeGoogleLink(credential: string) {
    const preparation = googlePreparation;
    if (preparation === null || completeGoogleMutation.isPending) {
      return;
    }
    clearFeedback();
    completeGoogleMutation.mutate(
      { preparation, credential },
      {
        onSuccess: async (result) => {
          setGooglePreparation(null);
          if (result.outcome !== 'authenticated') {
            setLastError({
              message: 'Google did not complete the requested account link.',
              reauthenticationRequired: false,
            });
            return;
          }
          await refreshMethods();
          setSuccessMessage(t(($) => $.common.access.security.providerLinked));
        },
        onError: handleError,
      },
    );
  }

  function linkApple() {
    clearFeedback();
    if (csrfToken === null || appleMutation.isPending) {
      return;
    }
    appleMutation.mutate(
      {
        purpose: 'link',
        returnTarget: 'security',
        csrfToken,
      },
      { onError: handleError },
    );
  }

  function unlinkProvider(externalIdentityRef: string) {
    clearFeedback();
    if (csrfToken === null) {
      return;
    }
    unlinkProviderMutation.mutate(
      { externalIdentityRef, csrfToken },
      {
        onSuccess: async () => {
          await refreshMethods();
          setSuccessMessage(t(($) => $.common.access.security.providerRemoved));
        },
        onError: handleError,
      },
    );
  }

  function registerPasskey(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    clearFeedback();
    if (csrfToken === null) {
      return;
    }
    const label = passkeyLabel.trim();
    if (label.length === 0) {
      setLastError({
        message: t(($) => $.common.access.security.passkeyLabelRequired),
        reauthenticationRequired: false,
      });
      return;
    }
    registerPasskeyMutation.mutate(
      { label, csrfToken },
      {
        onSuccess: () => {
          setSuccessMessage(t(($) => $.common.access.security.passkeyAdded));
        },
        onError: handleError,
      },
    );
  }

  function savePasskeyLabel(passkeyCredentialRef: string) {
    clearFeedback();
    if (csrfToken === null || editingPasskeyLabel.trim().length === 0) {
      return;
    }
    updatePasskeyMutation.mutate(
      {
        passkeyCredentialRef,
        label: editingPasskeyLabel.trim(),
        csrfToken,
      },
      {
        onSuccess: () => {
          setEditingPasskeyRef(null);
          setSuccessMessage(t(($) => $.common.access.security.passkeyRenamed));
        },
        onError: handleError,
      },
    );
  }

  function removePasskey(passkeyCredentialRef: string) {
    clearFeedback();
    if (csrfToken === null) {
      return;
    }
    removePasskeyMutation.mutate(
      { passkeyCredentialRef, csrfToken },
      {
        onSuccess: () =>
          setSuccessMessage(t(($) => $.common.access.security.passkeyRemoved)),
        onError: handleError,
      },
    );
  }

  function reauthenticatePassword(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    clearFeedback();
    if (csrfToken === null || passwordReauth.length === 0) {
      return;
    }
    passwordReauthMutation.mutate(
      { password: passwordReauth, csrfToken },
      {
        onSuccess: () => {
          setPasswordReauth('');
          setGooglePreparation(null);
          setSuccessMessage(t(($) => $.common.access.security.reauthComplete));
        },
        onError: handleError,
      },
    );
  }

  function reauthenticatePasskey() {
    clearFeedback();
    if (csrfToken === null) {
      return;
    }
    passkeyReauthMutation.mutate(
      { csrfToken },
      {
        onSuccess: () => {
          setGooglePreparation(null);
          setSuccessMessage(t(($) => $.common.access.security.reauthComplete));
        },
        onError: handleError,
      },
    );
  }

  if (sessionQuery.isPending) {
    return (
      <main className="access-security-shell">
        <p>{t(($) => $.common.access.security.loading)}</p>
      </main>
    );
  }

  if (!authenticated || session === null) {
    return (
      <main className="access-security-shell">
        <section className="access-security-card">
          <h1>{t(($) => $.common.access.security.signinRequired)}</h1>
          <Link className="access-primary-button access-security-link" to="/">
            {t(($) => $.common.access.action.signin)}
          </Link>
        </section>
      </main>
    );
  }

  return (
    <main className="access-security-shell">
      <header className="access-security-header">
        <div>
          <p className="access-kicker">{t(($) => $.common.access.kicker.access)}</p>
          <h1>{t(($) => $.common.access.security.title)}</h1>
          <p>{t(($) => $.common.access.security.body)}</p>
        </div>
        <Link className="access-secondary-button access-security-link" to="/">
          {t(($) => $.common.access.security.backAccess)}
        </Link>
      </header>

      {lastError ? (
        <div className="access-security-feedback is-error" role="alert">
          <strong>{lastError.message}</strong>
          {lastError.reauthenticationRequired ? (
            <span>{t(($) => $.common.access.security.reauthHint)}</span>
          ) : null}
        </div>
      ) : null}
      {successMessage ? (
        <div className="access-security-feedback" role="status">
          {successMessage}
        </div>
      ) : null}

      <section className="access-security-card">
        <h2>{t(($) => $.common.access.security.reauthTitle)}</h2>
        <p>{t(($) => $.common.access.security.reauthBody)}</p>
        <div className="access-security-actions">
          <form className="access-security-inline-form" onSubmit={reauthenticatePassword}>
            <input
              type="password"
              autoComplete="current-password"
              value={passwordReauth}
              placeholder={t(($) => $.common.access.field.password)}
              onChange={(event) => setPasswordReauth(event.target.value)}
            />
            <button
              className="access-secondary-button"
              type="submit"
              disabled={passwordReauthMutation.isPending}
            >
              {t(($) => $.common.access.security.reauthPassword)}
            </button>
          </form>
          <button
            className="access-secondary-button"
            type="button"
            disabled={passkeyReauthMutation.isPending}
            onClick={reauthenticatePasskey}
          >
            {t(($) => $.common.access.security.reauthPasskey)}
          </button>
        </div>
      </section>

      <section className="access-security-card">
        <h2>{t(($) => $.common.access.security.passwordTitle)}</h2>
        {methods?.password_established ? (
          <button
            className="access-danger-button"
            type="button"
            disabled={removePasswordMutation.isPending}
            onClick={removePassword}
          >
            {t(($) => $.common.access.security.removePassword)}
          </button>
        ) : (
          <form className="access-security-inline-form" onSubmit={submitPassword}>
            <input
              type="password"
              autoComplete="new-password"
              value={newPassword}
              placeholder={t(($) => $.common.access.security.newPassword)}
              onChange={(event) => setNewPassword(event.target.value)}
            />
            <button
              className="access-primary-button"
              type="submit"
              disabled={establishPasswordMutation.isPending}
            >
              {t(($) => $.common.access.security.addPassword)}
            </button>
          </form>
        )}
      </section>

      <section className="access-security-card">
        <div className="access-security-section-heading">
          <div>
            <h2>{t(($) => $.common.access.security.providersTitle)}</h2>
            <p>{t(($) => $.common.access.security.providersBody)}</p>
          </div>
          <div className="access-security-actions">
            {!providerCodes.has('google') ? (
              googlePreparation === null ? (
                <button
                  className="access-secondary-button"
                  type="button"
                  disabled={prepareGoogleMutation.isPending}
                  aria-busy={prepareGoogleMutation.isPending}
                  onClick={prepareGoogleLink}
                >
                  {t(($) => $.common.access.security.linkGoogle)}
                </button>
              ) : (
                <GoogleIdentityButton
                  label={t(($) => $.common.access.security.linkGoogle)}
                  clientId={googlePreparation.clientId}
                  nonce={googlePreparation.begun.nonce}
                  disabled={completeGoogleMutation.isPending}
                  onCredential={completeGoogleLink}
                  onError={handleProviderBrowserError}
                />
              )
            ) : null}
            {!providerCodes.has('apple') ? (
              <button
                className="access-secondary-button"
                type="button"
                disabled={appleMutation.isPending}
                aria-busy={appleMutation.isPending}
                onClick={linkApple}
              >
                {t(($) => $.common.access.security.linkApple)}
              </button>
            ) : null}
          </div>
        </div>
        <div className="access-security-list">
          {methods?.providers.map((provider) => (
            <article
              className="access-security-method"
              key={provider.external_identity_ref}
            >
              <div>
                <strong>{provider.provider_code}</strong>
                {provider.provider_email_address ? (
                  <span>{provider.provider_email_address}</span>
                ) : null}
              </div>
              <button
                className="access-danger-button"
                type="button"
                disabled={unlinkProviderMutation.isPending}
                onClick={() => unlinkProvider(provider.external_identity_ref)}
              >
                {t(($) => $.common.access.security.remove)}
              </button>
            </article>
          ))}
        </div>
      </section>

      <section className="access-security-card">
        <div className="access-security-section-heading">
          <div>
            <h2>{t(($) => $.common.access.security.passkeysTitle)}</h2>
            <p>{t(($) => $.common.access.security.passkeysBody)}</p>
          </div>
        </div>
        <form className="access-security-inline-form" onSubmit={registerPasskey}>
          <input
            value={passkeyLabel}
            maxLength={100}
            onChange={(event) => setPasskeyLabel(event.target.value)}
            aria-label={t(($) => $.common.access.security.passkeyLabel)}
          />
          <button
            className="access-primary-button"
            type="submit"
            disabled={registerPasskeyMutation.isPending}
          >
            {t(($) => $.common.access.security.addPasskey)}
          </button>
        </form>
        <div className="access-security-list">
          {methods?.passkeys.map((passkey) => (
            <article
              className="access-security-method"
              key={passkey.passkey_credential_ref}
            >
              <div>
                {editingPasskeyRef === passkey.passkey_credential_ref ? (
                  <input
                    value={editingPasskeyLabel}
                    maxLength={100}
                    onChange={(event) => setEditingPasskeyLabel(event.target.value)}
                  />
                ) : (
                  <strong>{passkey.label}</strong>
                )}
                <span>
                  {passkey.transports.join(', ') ||
                    t(($) => $.common.access.security.passkeyTransportUnknown)}
                </span>
              </div>
              <div className="access-security-actions">
                {editingPasskeyRef === passkey.passkey_credential_ref ? (
                  <button
                    className="access-secondary-button"
                    type="button"
                    disabled={updatePasskeyMutation.isPending}
                    onClick={() => savePasskeyLabel(passkey.passkey_credential_ref)}
                  >
                    {t(($) => $.common.access.security.save)}
                  </button>
                ) : (
                  <button
                    className="access-secondary-button"
                    type="button"
                    onClick={() => {
                      setEditingPasskeyRef(passkey.passkey_credential_ref);
                      setEditingPasskeyLabel(passkey.label);
                    }}
                  >
                    {t(($) => $.common.access.security.rename)}
                  </button>
                )}
                <button
                  className="access-danger-button"
                  type="button"
                  disabled={removePasskeyMutation.isPending}
                  onClick={() => removePasskey(passkey.passkey_credential_ref)}
                >
                  {t(($) => $.common.access.security.remove)}
                </button>
              </div>
            </article>
          ))}
        </div>
      </section>
    </main>
  );
}
