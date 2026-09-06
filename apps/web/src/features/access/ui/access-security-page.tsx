import { useMemo, useState, type FormEvent } from 'react';
import { Link } from '@tanstack/react-router';
import { useTranslation } from 'react-i18next';

import {
  appleAuthenticationEnabledFromBuild,
  googleAuthenticationEnabledFromBuild,
  passkeyAuthenticationEnabledFromBuild,
  WebAuthRemoteError,
} from '../application/auth-ui-boundary';
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
import {
  isAuthenticatedAccessSession,
  useAuthSessionQuery,
} from '../application/auth-session';
import { useReauthenticateMutation } from '../application/auth-lifecycle';
import { isValidNewPassword } from '../model/access-flow';
import { GoogleIdentityButton } from './provider-button';
import '../access.css';
import '../access-security.css';

type SecurityError = Readonly<{
  message: string;
  reauthenticationRequired: boolean;
}>;

type GoogleSecurityFlow = Readonly<{
  kind: 'link' | 'reauthenticate';
  preparation: GoogleAuthenticationPreparation;
}>;

export function AccessSecurityPage() {
  const { t } = useTranslation('common');
  const sessionQuery = useAuthSessionQuery();
  const sessionData = sessionQuery.data;
  const session = isAuthenticatedAccessSession(sessionData)
    ? sessionData
    : null;
  const authenticated = session !== null;
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
  const [passkeyLabel, setPasskeyLabel] = useState('');
  const [passwordReauth, setPasswordReauth] = useState('');
  const [editingPasskeyRef, setEditingPasskeyRef] = useState<string | null>(
    null,
  );
  const [editingPasskeyLabel, setEditingPasskeyLabel] = useState('');
  const [googleFlow, setGoogleFlow] = useState<GoogleSecurityFlow | null>(null);
  const [lastError, setLastError] = useState<SecurityError | null>(null);
  const [successMessage, setSuccessMessage] = useState<string | null>(null);

  const googleEnabled = googleAuthenticationEnabledFromBuild();
  const appleEnabled = appleAuthenticationEnabledFromBuild();
  const passkeyEnabled = passkeyAuthenticationEnabledFromBuild();
  const csrfToken = session?.csrf_token ?? null;
  const methods = methodsQuery.data;
  const providerCodes = useMemo(
    () =>
      new Set(
        methods?.providers.map((provider) => provider.provider_code) ?? [],
      ),
    [methods?.providers],
  );
  const passwordEstablished = methods?.password_established === true;
  const activePasskeyCount = methods?.passkeys.length ?? 0;
  const googleLinked = providerCodes.has('google');
  const appleLinked = providerCodes.has('apple');
  const canReauthenticateWithGoogle = googleEnabled && googleLinked;
  const canReauthenticateWithApple = appleEnabled && appleLinked;
  const canReauthenticateWithPasskey = passkeyEnabled && activePasskeyCount > 0;
  const hasInlineReauthenticationMethod =
    passwordEstablished ||
    canReauthenticateWithGoogle ||
    canReauthenticateWithApple ||
    canReauthenticateWithPasskey;
  const showProviderManagement =
    googleEnabled || appleEnabled || (methods?.providers.length ?? 0) > 0;
  const showPasskeyManagement = passkeyEnabled || activePasskeyCount > 0;

  function providerDisplayName(providerCode: string): string {
    if (providerCode === 'google') {
      return t(($) => $.common.access.provider.googleName);
    }
    if (providerCode === 'apple') {
      return t(($) => $.common.access.provider.appleName);
    }
    return providerCode;
  }

  function errorFor(error: unknown): SecurityError {
    if (!(error instanceof WebAuthRemoteError)) {
      return {
        message: t(($) => $.common.access.security.errorOperation),
        reauthenticationRequired: false,
      };
    }
    const failure = error.failure;
    if (failure.kind !== 'server_problem') {
      return {
        message:
          failure.kind === 'network_unavailable'
            ? t(($) => $.common.access.security.errorServiceUnreachable)
            : t(($) => $.common.access.security.errorOperation),
        reauthenticationRequired: false,
      };
    }
    switch (failure.code) {
      case 'auth.reauthentication_required':
        return {
          message: t(
            ($) => $.common.access.security.errorReauthenticationRequired,
          ),
          reauthenticationRequired: true,
        };
      case 'auth.authenticator_removal_blocked':
        return {
          message: t(($) => $.common.access.security.errorRemovalBlocked),
          reauthenticationRequired: false,
        };
      case 'auth.password_already_established':
        return {
          message: t(
            ($) => $.common.access.security.errorPasswordAlreadyEstablished,
          ),
          reauthenticationRequired: false,
        };
      case 'auth.passkey_already_registered':
        return {
          message: t(
            ($) => $.common.access.security.errorPasskeyAlreadyRegistered,
          ),
          reauthenticationRequired: false,
        };
      case 'auth.passkey_not_found':
        return {
          message: t(($) => $.common.access.security.errorPasskeyNotFound),
          reauthenticationRequired: false,
        };
      case 'dependency.provider_unavailable':
      case 'service.unavailable':
        return {
          message: t(($) => $.common.access.security.errorServiceUnavailable),
          reauthenticationRequired: false,
        };
      default:
        return {
          message: t(($) => $.common.access.security.errorOperation),
          reauthenticationRequired: false,
        };
    }
  }

  function clearFeedback() {
    setLastError(null);
    setSuccessMessage(null);
  }

  function handleError(error: unknown) {
    setSuccessMessage(null);
    setLastError(errorFor(error));
  }

  function handleProviderBrowserError() {
    setGoogleFlow(null);
    setSuccessMessage(null);
    setLastError({
      message: t(($) => $.common.access.security.errorGoogleControl),
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
        message: t(($) => $.common.access.security.errorSessionUnavailable),
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

  function prepareGoogleSecurityFlow(kind: GoogleSecurityFlow['kind']) {
    clearFeedback();
    if (
      !googleEnabled ||
      csrfToken === null ||
      prepareGoogleMutation.isPending
    ) {
      return;
    }
    setGoogleFlow(null);
    prepareGoogleMutation.mutate(
      {
        purpose: kind === 'link' ? 'link' : 'reauthenticate',
        returnTarget: 'security',
        csrfToken,
      },
      {
        onSuccess: (preparation) => {
          if (preparation === null) {
            setLastError({
              message: t(($) => $.common.access.security.errorOperation),
              reauthenticationRequired: false,
            });
            return;
          }
          setGoogleFlow({ kind, preparation });
        },
        onError: handleError,
      },
    );
  }

  function completeGoogleSecurityFlow(credential: string) {
    const flow = googleFlow;
    if (flow === null || completeGoogleMutation.isPending) {
      return;
    }
    clearFeedback();
    completeGoogleMutation.mutate(
      { preparation: flow.preparation, credential },
      {
        onSuccess: (result) => {
          setGoogleFlow(null);
          if (result.outcome !== 'authenticated') {
            setLastError({
              message: t(($) => $.common.access.security.errorOperation),
              reauthenticationRequired: false,
            });
            return;
          }
          if (flow.kind === 'reauthenticate') {
            setSuccessMessage(
              t(($) => $.common.access.security.reauthComplete),
            );
            return;
          }
          void refreshMethods()
            .then(() => {
              setSuccessMessage(
                t(($) => $.common.access.security.providerLinked),
              );
            })
            .catch(handleError);
        },
        onError: (error) => {
          setGoogleFlow(null);
          handleError(error);
        },
      },
    );
  }

  function linkApple() {
    clearFeedback();
    if (!appleEnabled || csrfToken === null || appleMutation.isPending) {
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

  function reauthenticateApple() {
    clearFeedback();
    if (
      !canReauthenticateWithApple ||
      csrfToken === null ||
      appleMutation.isPending
    ) {
      return;
    }
    appleMutation.mutate(
      {
        purpose: 'reauthenticate',
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
        onSuccess: () => {
          void refreshMethods()
            .then(() => {
              setSuccessMessage(
                t(($) => $.common.access.security.providerRemoved),
              );
            })
            .catch(handleError);
        },
        onError: handleError,
      },
    );
  }

  function registerPasskey(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    clearFeedback();
    if (!passkeyEnabled || csrfToken === null) {
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
          setPasskeyLabel('');
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
    if (
      !passwordEstablished ||
      csrfToken === null ||
      passwordReauth.length === 0
    ) {
      return;
    }
    passwordReauthMutation.mutate(
      { password: passwordReauth, csrfToken },
      {
        onSuccess: () => {
          setPasswordReauth('');
          setGoogleFlow(null);
          setSuccessMessage(t(($) => $.common.access.security.reauthComplete));
        },
        onError: handleError,
      },
    );
  }

  function reauthenticatePasskey() {
    clearFeedback();
    if (!canReauthenticateWithPasskey || csrfToken === null) {
      return;
    }
    passkeyReauthMutation.mutate(
      { csrfToken },
      {
        onSuccess: () => {
          setGoogleFlow(null);
          setSuccessMessage(t(($) => $.common.access.security.reauthComplete));
        },
        onError: handleError,
      },
    );
  }

  if (sessionQuery.isPending || (authenticated && methodsQuery.isPending)) {
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

  if (methodsQuery.isError) {
    return (
      <main className="access-security-shell">
        <section className="access-security-card">
          <h1>{t(($) => $.common.access.security.title)}</h1>
          <p>{t(($) => $.common.access.security.body)}</p>
          <div className="access-security-feedback is-error" role="alert">
            <strong>{errorFor(methodsQuery.error).message}</strong>
          </div>
          <button
            className="access-secondary-button"
            type="button"
            onClick={() => void methodsQuery.refetch()}
          >
            {t(($) => $.common.access.action.tryAgain)}
          </button>
        </section>
      </main>
    );
  }

  return (
    <main className="access-security-shell">
      <header className="access-security-header">
        <div>
          <p className="access-kicker">
            {t(($) => $.common.access.kicker.access)}
          </p>
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
        {hasInlineReauthenticationMethod ? (
          <div className="access-security-actions">
            {passwordEstablished ? (
              <form
                className="access-security-inline-form"
                onSubmit={reauthenticatePassword}
              >
                <input
                  type="password"
                  autoComplete="current-password"
                  aria-label={t(($) => $.common.access.field.password)}
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
            ) : null}

            {canReauthenticateWithGoogle ? (
              googleFlow?.kind === 'reauthenticate' ? (
                <GoogleIdentityButton
                  label={t(($) => $.common.access.provider.google)}
                  clientId={googleFlow.preparation.clientId}
                  nonce={googleFlow.preparation.begun.nonce}
                  disabled={completeGoogleMutation.isPending}
                  onCredential={completeGoogleSecurityFlow}
                  onError={handleProviderBrowserError}
                />
              ) : (
                <button
                  className="access-secondary-button"
                  type="button"
                  disabled={prepareGoogleMutation.isPending}
                  aria-busy={prepareGoogleMutation.isPending}
                  onClick={() => prepareGoogleSecurityFlow('reauthenticate')}
                >
                  {t(($) => $.common.access.provider.google)}
                </button>
              )
            ) : null}

            {canReauthenticateWithApple ? (
              <button
                className="access-secondary-button"
                type="button"
                disabled={appleMutation.isPending}
                aria-busy={appleMutation.isPending}
                onClick={reauthenticateApple}
              >
                {t(($) => $.common.access.provider.apple)}
              </button>
            ) : null}

            {canReauthenticateWithPasskey ? (
              <button
                className="access-secondary-button"
                type="button"
                disabled={passkeyReauthMutation.isPending}
                onClick={reauthenticatePasskey}
              >
                {t(($) => $.common.access.security.reauthPasskey)}
              </button>
            ) : null}
          </div>
        ) : (
          <p>{t(($) => $.common.access.security.reauthNoInlineMethod)}</p>
        )}
      </section>

      <section className="access-security-card">
        <h2>{t(($) => $.common.access.security.passwordTitle)}</h2>
        {passwordEstablished ? (
          <button
            className="access-danger-button"
            type="button"
            disabled={removePasswordMutation.isPending}
            onClick={removePassword}
          >
            {t(($) => $.common.access.security.removePassword)}
          </button>
        ) : (
          <form
            className="access-security-inline-form"
            onSubmit={submitPassword}
          >
            <input
              type="password"
              autoComplete="new-password"
              aria-label={t(($) => $.common.access.security.newPassword)}
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

      {showProviderManagement ? (
        <section className="access-security-card">
          <div className="access-security-section-heading">
            <div>
              <h2>{t(($) => $.common.access.security.providersTitle)}</h2>
              <p>{t(($) => $.common.access.security.providersBody)}</p>
            </div>
            <div className="access-security-actions">
              {googleEnabled && !googleLinked ? (
                googleFlow?.kind === 'link' ? (
                  <GoogleIdentityButton
                    label={t(($) => $.common.access.security.linkGoogle)}
                    clientId={googleFlow.preparation.clientId}
                    nonce={googleFlow.preparation.begun.nonce}
                    disabled={completeGoogleMutation.isPending}
                    onCredential={completeGoogleSecurityFlow}
                    onError={handleProviderBrowserError}
                  />
                ) : (
                  <button
                    className="access-secondary-button"
                    type="button"
                    disabled={prepareGoogleMutation.isPending}
                    aria-busy={prepareGoogleMutation.isPending}
                    onClick={() => prepareGoogleSecurityFlow('link')}
                  >
                    {t(($) => $.common.access.security.linkGoogle)}
                  </button>
                )
              ) : null}
              {appleEnabled && !appleLinked ? (
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
                  <strong>{providerDisplayName(provider.provider_code)}</strong>
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
      ) : null}

      {showPasskeyManagement ? (
        <section className="access-security-card">
          <div className="access-security-section-heading">
            <div>
              <h2>{t(($) => $.common.access.security.passkeysTitle)}</h2>
              <p>{t(($) => $.common.access.security.passkeysBody)}</p>
            </div>
          </div>
          {passkeyEnabled ? (
            <form
              className="access-security-inline-form"
              onSubmit={registerPasskey}
            >
              <input
                value={passkeyLabel}
                maxLength={100}
                placeholder={t(
                  ($) => $.common.access.security.passkeyLabelPlaceholder,
                )}
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
          ) : null}
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
                      aria-label={t(
                        ($) => $.common.access.security.passkeyLabel,
                      )}
                      onChange={(event) =>
                        setEditingPasskeyLabel(event.target.value)
                      }
                    />
                  ) : (
                    <strong>{passkey.label}</strong>
                  )}
                  <span>
                    {passkey.transports.join(', ') ||
                      t(
                        ($) => $.common.access.security.passkeyTransportUnknown,
                      )}
                  </span>
                </div>
                <div className="access-security-actions">
                  {editingPasskeyRef === passkey.passkey_credential_ref ? (
                    <button
                      className="access-secondary-button"
                      type="button"
                      disabled={updatePasskeyMutation.isPending}
                      onClick={() =>
                        savePasskeyLabel(passkey.passkey_credential_ref)
                      }
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
                    onClick={() =>
                      removePasskey(passkey.passkey_credential_ref)
                    }
                  >
                    {t(($) => $.common.access.security.remove)}
                  </button>
                </div>
              </article>
            ))}
          </div>
        </section>
      ) : null}
    </main>
  );
}
