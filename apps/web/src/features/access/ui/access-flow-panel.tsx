import { useState, type Dispatch, type FormEvent } from 'react';
import { useTranslation } from 'react-i18next';

import {
  isValidAccessEmail,
  isValidNewPassword,
  type AccessFlowEvent,
  type AccessFlowState,
  type AccessProvider,
} from '../model/access-flow';
import { AccessAuthenticatedReturnPanel } from './access-authenticated-return-panel';
import { AccessConditionNotice } from './access-condition-notice';
import { AccessDownstreamPanel } from './access-downstream-panel';
import { AccessPanelFrame, AccessPasswordToggle } from './access-panel-frame';
import { AccessSignInPanel } from './access-sign-in-panel';
import { ProviderButton } from './provider-button';

type FlowProps = Readonly<{
  flow: AccessFlowState;
  dispatch: Dispatch<AccessFlowEvent>;
}>;

export type AccessRecoveryEntryState = 'none' | 'validating' | 'error';

type AccessPendingState = Readonly<{
  signIn: boolean;
  signUp: boolean;
  verify: boolean;
  resend: boolean;
  recovery: boolean;
  reset: boolean;
  reauth: boolean;
  logOut: boolean;
}>;

type AccessFlowPanelProps = FlowProps &
  Readonly<{
    recoveryEntryState: AccessRecoveryEntryState;
    onRetryRecoveryValidation: () => void;
    onCredentialSubmit: (email: string, password: string) => void;
    onSignupSubmit: (email: string, password: string) => void;
    onVerifySubmit: (code: string) => void;
    onResendVerification: () => void;
    onRecoverySubmit: (email: string) => void;
    onResetPassword: (password: string) => void;
    onReauthenticate: (password: string) => void;
    onLogOut: () => void;
    pending: AccessPendingState;
  }>;

function SignupEmailScreen({ flow, dispatch }: FlowProps) {
  const { t } = useTranslation('common');
  const initialEmail =
    flow.screen.id === 'SIGN_UP_EMAIL' ? flow.screen.email : '';
  const [email, setEmail] = useState(initialEmail);
  const [error, setError] = useState<string | null>(null);

  function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const trimmedEmail = email.trim();
    if (!isValidAccessEmail(trimmedEmail)) {
      setError(t(($) => $.common.access.validation.email));
      return;
    }
    dispatch({ type: 'SIGN_UP_EMAIL_ACCEPTED', email: trimmedEmail });
  }

  function provider(provider: AccessProvider) {
    dispatch({ type: 'REQUEST_PROVIDER', provider });
  }

  return (
    <AccessPanelFrame
      titleId="access-signup-email-title"
      kicker={t(($) => $.common.access.kicker.access)}
      title={t(($) => $.common.access.signup.title)}
      body={t(($) => $.common.access.signup.body)}
      onBack={() => dispatch({ type: 'BACK_TO_SIGN_IN' })}
      footer={
        <div className="access-new-account">
          <span>{t(($) => $.common.access.signup.existing)}</span>
          <button
            className="access-inline-action access-create-account"
            type="button"
            onClick={() => dispatch({ type: 'BACK_TO_SIGN_IN' })}
          >
            {t(($) => $.common.access.action.signin)}
          </button>
        </div>
      }
    >
      <div
        className="access-progress"
        aria-label={t(($) => $.common.access.signup.progress)}
      >
        <span className="is-active">
          {t(($) => $.common.access.signup.stepEmail)}
        </span>
        <span>{t(($) => $.common.access.signup.stepPassword)}</span>
        <span>{t(($) => $.common.access.signup.stepVerify)}</span>
      </div>

      <form className="access-flow-form" onSubmit={submit} noValidate>
        <div className="access-field">
          <label htmlFor="access-signup-email">
            {t(($) => $.common.access.field.email)}
          </label>
          <input
            id="access-signup-email"
            name="email"
            type="email"
            autoComplete="email"
            inputMode="email"
            value={email}
            placeholder={t(($) => $.common.access.field.emailPlaceholder)}
            aria-invalid={Boolean(error)}
            aria-describedby={error ? 'access-signup-email-error' : undefined}
            onChange={(event) => {
              setEmail(event.target.value);
              setError(null);
            }}
          />
          {error ? (
            <span id="access-signup-email-error" className="access-field-error">
              {error}
            </span>
          ) : null}
        </div>
        <button className="access-primary-button" type="submit">
          {t(($) => $.common.access.signup.continueEmail)}
        </button>
      </form>

      <div className="access-divider" aria-hidden="true">
        <span />
        <p>{t(($) => $.common.access.signup.orProvider)}</p>
        <span />
      </div>

      <div className="access-provider-stack">
        <ProviderButton
          provider="google"
          label={t(($) => $.common.access.signup.google)}
          onClick={() => provider('google')}
        />
        <ProviderButton
          provider="apple"
          label={t(($) => $.common.access.signup.apple)}
          onClick={() => provider('apple')}
        />
      </div>
      <AccessConditionNotice condition={flow.condition} />
    </AccessPanelFrame>
  );
}

function SignupPasswordScreen({
  flow,
  dispatch,
  onSubmit,
  pending,
}: FlowProps &
  Readonly<{
    onSubmit: (email: string, password: string) => void;
    pending: boolean;
  }>) {
  const { t } = useTranslation('common');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const email = flow.screen.id === 'SIGN_UP_PASSWORD' ? flow.screen.email : '';
  const passwordLabel = t(($) => $.common.access.field.password);

  function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (!isValidNewPassword(password)) {
      setError(t(($) => $.common.access.validation.passwordMinimum));
      return;
    }
    onSubmit(email, password);
  }

  return (
    <AccessPanelFrame
      titleId="access-signup-password-title"
      kicker={t(($) => $.common.access.kicker.access)}
      title={t(($) => $.common.access.signupPassword.title)}
      body={t(($) => $.common.access.signupPassword.body)}
      onBack={() => dispatch({ type: 'CHANGE_SIGN_UP_EMAIL' })}
    >
      <div
        className="access-progress"
        aria-label={t(($) => $.common.access.signup.progress)}
      >
        <span>{t(($) => $.common.access.signup.stepEmail)}</span>
        <span className="is-active">
          {t(($) => $.common.access.signup.stepPassword)}
        </span>
        <span>{t(($) => $.common.access.signup.stepVerify)}</span>
      </div>

      <div className="access-email-summary">
        <span>{t(($) => $.common.access.field.email)}</span>
        <strong>{email}</strong>
        <button
          className="access-inline-action"
          type="button"
          disabled={pending}
          onClick={() => dispatch({ type: 'CHANGE_SIGN_UP_EMAIL' })}
        >
          {t(($) => $.common.access.action.changeEmail)}
        </button>
      </div>

      <form className="access-flow-form" onSubmit={submit} noValidate>
        <div className="access-field">
          <label htmlFor="access-new-password">{passwordLabel}</label>
          <div className="access-input-wrap">
            <input
              id="access-new-password"
              name="new-password"
              type={showPassword ? 'text' : 'password'}
              autoComplete="new-password"
              value={password}
              disabled={pending}
              aria-invalid={Boolean(error)}
              aria-describedby={
                error ? 'access-new-password-error' : 'access-password-guide'
              }
              onChange={(event) => {
                setPassword(event.target.value);
                setError(null);
              }}
            />
            <AccessPasswordToggle
              showPassword={showPassword}
              controls="access-new-password"
              fieldLabel={passwordLabel}
              onToggle={() => setShowPassword((value) => !value)}
            />
          </div>
          {error ? (
            <span id="access-new-password-error" className="access-field-error">
              {error}
            </span>
          ) : null}
        </div>

        <div id="access-password-guide" className="access-password-guide">
          <strong>{t(($) => $.common.access.password.guideTitle)}</strong>
          <span>{t(($) => $.common.access.password.proposal)}</span>
          <p>{t(($) => $.common.access.password.manager)}</p>
        </div>

        <button
          className="access-primary-button"
          type="submit"
          disabled={pending}
          aria-busy={pending}
        >
          {t(($) => $.common.access.action.createAccount)}
        </button>
      </form>
      <AccessConditionNotice condition={flow.condition} />
    </AccessPanelFrame>
  );
}

function VerifyEmailScreen({
  flow,
  dispatch,
  onSubmit,
  onResend,
  verifyPending,
  resendPending,
}: FlowProps &
  Readonly<{
    onSubmit: (code: string) => void;
    onResend: () => void;
    verifyPending: boolean;
    resendPending: boolean;
  }>) {
  const { t } = useTranslation('common');
  const [code, setCode] = useState('');
  const [error, setError] = useState<string | null>(null);
  const email = flow.screen.id === 'VERIFY_EMAIL' ? flow.screen.email : '';

  function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (!/^\d{6}$/.test(code)) {
      setError(t(($) => $.common.access.validation.verificationCode));
      return;
    }
    onSubmit(code);
  }

  return (
    <AccessPanelFrame
      titleId="access-verify-title"
      kicker={t(($) => $.common.access.kicker.access)}
      title={t(($) => $.common.access.verify.title)}
      body={t(($) => $.common.access.verify.body)}
    >
      <div
        className="access-progress"
        aria-label={t(($) => $.common.access.signup.progress)}
      >
        <span>{t(($) => $.common.access.signup.stepEmail)}</span>
        <span>{t(($) => $.common.access.signup.stepPassword)}</span>
        <span className="is-active">
          {t(($) => $.common.access.signup.stepVerify)}
        </span>
      </div>
      <p className="access-email-context">{email}</p>
      <form className="access-flow-form" onSubmit={submit} noValidate>
        <div className="access-field">
          <label htmlFor="access-verification-code">
            {t(($) => $.common.access.field.verificationCode)}
          </label>
          <input
            id="access-verification-code"
            className="access-code-input"
            name="verification-code"
            type="text"
            inputMode="numeric"
            autoComplete="one-time-code"
            maxLength={6}
            value={code}
            disabled={verifyPending}
            aria-invalid={Boolean(error)}
            aria-describedby={
              error
                ? 'access-verification-code-error'
                : 'access-verification-code-help'
            }
            onChange={(event) => {
              setCode(event.target.value.replace(/\D/g, '').slice(0, 6));
              setError(null);
            }}
          />
          {error ? (
            <span
              id="access-verification-code-error"
              className="access-field-error"
            >
              {error}
            </span>
          ) : null}
        </div>
        <button
          className="access-primary-button"
          type="submit"
          disabled={verifyPending || resendPending}
          aria-busy={verifyPending}
        >
          {t(($) => $.common.access.verify.action)}
        </button>
      </form>
      <div className="access-secondary-actions">
        <button
          className="access-inline-action"
          type="button"
          disabled={verifyPending || resendPending}
          onClick={onResend}
        >
          {t(($) => $.common.access.verify.resend)}
        </button>
        <button
          className="access-inline-action"
          type="button"
          disabled={verifyPending || resendPending}
          onClick={() => dispatch({ type: 'CREATE_ACCOUNT' })}
        >
          {t(($) => $.common.access.action.changeEmail)}
        </button>
      </div>
      <p id="access-verification-code-help" className="access-security-note">
        {t(($) => $.common.access.verify.privacy)}
      </p>
      <AccessConditionNotice condition={flow.condition} />
    </AccessPanelFrame>
  );
}

function ForgotPasswordScreen({
  flow,
  dispatch,
  onSubmit,
  pending,
}: FlowProps &
  Readonly<{ onSubmit: (email: string) => void; pending: boolean }>) {
  const { t } = useTranslation('common');
  const initialEmail =
    flow.screen.id === 'FORGOT_PASSWORD' ? flow.screen.email : '';
  const [email, setEmail] = useState(initialEmail);
  const [error, setError] = useState<string | null>(null);

  function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const trimmedEmail = email.trim();
    if (!isValidAccessEmail(trimmedEmail)) {
      setError(t(($) => $.common.access.validation.email));
      return;
    }
    onSubmit(trimmedEmail);
  }

  return (
    <AccessPanelFrame
      titleId="access-forgot-title"
      kicker={t(($) => $.common.access.kicker.access)}
      title={t(($) => $.common.access.forgot.title)}
      body={t(($) => $.common.access.forgot.body)}
      onBack={() => dispatch({ type: 'BACK_TO_SIGN_IN' })}
    >
      <form className="access-flow-form" onSubmit={submit} noValidate>
        <div className="access-field">
          <label htmlFor="access-recovery-email">
            {t(($) => $.common.access.field.email)}
          </label>
          <input
            id="access-recovery-email"
            name="email"
            type="email"
            autoComplete="email"
            inputMode="email"
            value={email}
            disabled={pending}
            placeholder={t(($) => $.common.access.field.emailPlaceholder)}
            aria-invalid={Boolean(error)}
            aria-describedby={
              error ? 'access-recovery-email-error' : 'access-recovery-note'
            }
            onChange={(event) => {
              setEmail(event.target.value);
              setError(null);
            }}
          />
          {error ? (
            <span
              id="access-recovery-email-error"
              className="access-field-error"
            >
              {error}
            </span>
          ) : null}
        </div>
        <button
          className="access-primary-button"
          type="submit"
          disabled={pending}
          aria-busy={pending}
        >
          {t(($) => $.common.access.forgot.action)}
        </button>
      </form>
      <p id="access-recovery-note" className="access-security-note">
        {t(($) => $.common.access.forgot.privacy)}
      </p>
      <AccessConditionNotice condition={flow.condition} />
    </AccessPanelFrame>
  );
}

function ResetPasswordScreen({
  flow,
  onSubmit,
  pending,
}: Pick<FlowProps, 'flow'> &
  Readonly<{ onSubmit: (password: string) => void; pending: boolean }>) {
  const { t } = useTranslation('common');
  const [password, setPassword] = useState('');
  const [confirm, setConfirm] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirm, setShowConfirm] = useState(false);
  const [passwordError, setPasswordError] = useState<string | null>(null);
  const [confirmError, setConfirmError] = useState<string | null>(null);

  function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const minimumError = !isValidNewPassword(password)
      ? t(($) => $.common.access.validation.passwordMinimum)
      : null;
    const mismatchError =
      !minimumError && password !== confirm
        ? t(($) => $.common.access.validation.passwordMismatch)
        : null;
    setPasswordError(minimumError);
    setConfirmError(mismatchError);
    if (minimumError || mismatchError) {
      return;
    }
    onSubmit(password);
  }

  const newPasswordLabel = t(($) => $.common.access.reset.new);
  const confirmPasswordLabel = t(($) => $.common.access.reset.confirm);

  return (
    <AccessPanelFrame
      titleId="access-reset-title"
      kicker={t(($) => $.common.access.kicker.access)}
      title={t(($) => $.common.access.reset.title)}
      body={t(($) => $.common.access.reset.body)}
    >
      <form className="access-flow-form" onSubmit={submit} noValidate>
        <div className="access-field">
          <label htmlFor="access-reset-password">{newPasswordLabel}</label>
          <div className="access-input-wrap">
            <input
              id="access-reset-password"
              name="new-password"
              type={showPassword ? 'text' : 'password'}
              autoComplete="new-password"
              value={password}
              disabled={pending}
              aria-invalid={Boolean(passwordError)}
              aria-describedby={
                passwordError
                  ? 'access-reset-password-error'
                  : 'access-reset-password-guide'
              }
              onChange={(event) => {
                setPassword(event.target.value);
                setPasswordError(null);
                setConfirmError(null);
              }}
            />
            <AccessPasswordToggle
              showPassword={showPassword}
              controls="access-reset-password"
              fieldLabel={newPasswordLabel}
              onToggle={() => setShowPassword((value) => !value)}
            />
          </div>
          {passwordError ? (
            <span
              id="access-reset-password-error"
              className="access-field-error"
            >
              {passwordError}
            </span>
          ) : null}
        </div>
        <div id="access-reset-password-guide" className="access-password-guide">
          <strong>{t(($) => $.common.access.password.guideTitle)}</strong>
          <span>{t(($) => $.common.access.password.proposal)}</span>
          <p>{t(($) => $.common.access.password.manager)}</p>
        </div>
        <div className="access-field">
          <label htmlFor="access-reset-confirm">{confirmPasswordLabel}</label>
          <div className="access-input-wrap">
            <input
              id="access-reset-confirm"
              name="confirm-password"
              type={showConfirm ? 'text' : 'password'}
              autoComplete="new-password"
              value={confirm}
              disabled={pending}
              aria-invalid={Boolean(confirmError)}
              aria-describedby={
                confirmError ? 'access-reset-confirm-error' : undefined
              }
              onChange={(event) => {
                setConfirm(event.target.value);
                setConfirmError(null);
              }}
            />
            <AccessPasswordToggle
              showPassword={showConfirm}
              controls="access-reset-confirm"
              fieldLabel={confirmPasswordLabel}
              onToggle={() => setShowConfirm((value) => !value)}
            />
          </div>
          {confirmError ? (
            <span
              id="access-reset-confirm-error"
              className="access-field-error"
            >
              {confirmError}
            </span>
          ) : null}
        </div>
        <button
          className="access-primary-button"
          type="submit"
          disabled={pending}
          aria-busy={pending}
        >
          {t(($) => $.common.access.reset.action)}
        </button>
      </form>
      <AccessConditionNotice condition={flow.condition} />
    </AccessPanelFrame>
  );
}

function ReauthenticateScreen({
  flow,
  dispatch,
  onSubmit,
  pending,
}: FlowProps &
  Readonly<{ onSubmit: (password: string) => void; pending: boolean }>) {
  const { t } = useTranslation('common');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const passwordLabel = t(($) => $.common.access.field.password);

  function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (!password) {
      setError(t(($) => $.common.access.validation.passwordRequired));
      return;
    }
    onSubmit(password);
  }

  return (
    <AccessPanelFrame
      titleId="access-reauth-title"
      kicker={t(($) => $.common.access.kicker.access)}
      title={t(($) => $.common.access.reauth.title)}
      body={t(($) => $.common.access.reauth.body)}
    >
      <form className="access-flow-form" onSubmit={submit} noValidate>
        <div className="access-field">
          <label htmlFor="access-reauth-password">{passwordLabel}</label>
          <div className="access-input-wrap">
            <input
              id="access-reauth-password"
              name="password"
              type={showPassword ? 'text' : 'password'}
              autoComplete="current-password"
              value={password}
              disabled={pending}
              aria-invalid={Boolean(error)}
              aria-describedby={
                error ? 'access-reauth-password-error' : undefined
              }
              onChange={(event) => {
                setPassword(event.target.value);
                setError(null);
              }}
            />
            <AccessPasswordToggle
              showPassword={showPassword}
              controls="access-reauth-password"
              fieldLabel={passwordLabel}
              onToggle={() => setShowPassword((value) => !value)}
            />
          </div>
          {error ? (
            <span
              id="access-reauth-password-error"
              className="access-field-error"
            >
              {error}
            </span>
          ) : null}
        </div>
        <button
          className="access-primary-button"
          type="submit"
          disabled={pending}
          aria-busy={pending}
        >
          {t(($) => $.common.access.reauth.action)}
        </button>
      </form>
      <button
        className="access-secondary-button"
        type="button"
        disabled={pending}
        onClick={() => dispatch({ type: 'REAUTH_CANCEL' })}
      >
        {t(($) => $.common.access.action.cancel)}
      </button>
      <AccessConditionNotice condition={flow.condition} />
    </AccessPanelFrame>
  );
}

function RecoveryValidationScreen({
  flow,
  state,
  onRetry,
}: Readonly<{
  flow: AccessFlowState;
  state: Exclude<AccessRecoveryEntryState, 'none'>;
  onRetry: () => void;
}>) {
  const { t } = useTranslation('common');
  return (
    <AccessPanelFrame
      titleId="access-recovery-validating-title"
      kicker={t(($) => $.common.access.kicker.access)}
      title={t(($) => $.common.access.recovery.validatingTitle)}
      body={t(($) => $.common.access.recovery.validatingBody)}
    >
      {state === 'validating' ? (
        <div className="access-wait-indicator" aria-hidden="true" />
      ) : (
        <button
          className="access-primary-button"
          type="button"
          onClick={onRetry}
        >
          {t(($) => $.common.access.action.tryAgain)}
        </button>
      )}
      <AccessConditionNotice condition={flow.condition} />
    </AccessPanelFrame>
  );
}

export function AccessFlowPanel({
  flow,
  dispatch,
  recoveryEntryState,
  onRetryRecoveryValidation,
  onCredentialSubmit,
  onSignupSubmit,
  onVerifySubmit,
  onResendVerification,
  onRecoverySubmit,
  onResetPassword,
  onReauthenticate,
  onLogOut,
  pending,
}: AccessFlowPanelProps) {
  if (recoveryEntryState !== 'none') {
    return (
      <RecoveryValidationScreen
        flow={flow}
        state={recoveryEntryState}
        onRetry={onRetryRecoveryValidation}
      />
    );
  }

  const screen = flow.screen;
  switch (screen.id) {
    case 'SIGN_IN':
      return (
        <AccessSignInPanel
          condition={flow.condition}
          onCreateAccount={() => dispatch({ type: 'CREATE_ACCOUNT' })}
          onForgotPassword={() => dispatch({ type: 'FORGOT_PASSWORD' })}
          onCredentialSubmit={onCredentialSubmit}
          onProvider={(provider) =>
            dispatch({ type: 'REQUEST_PROVIDER', provider })
          }
          pending={pending.signIn}
        />
      );
    case 'SIGN_UP_EMAIL':
      return <SignupEmailScreen flow={flow} dispatch={dispatch} />;
    case 'SIGN_UP_PASSWORD':
      return (
        <SignupPasswordScreen
          flow={flow}
          dispatch={dispatch}
          onSubmit={onSignupSubmit}
          pending={pending.signUp}
        />
      );
    case 'VERIFY_EMAIL':
      return (
        <VerifyEmailScreen
          flow={flow}
          dispatch={dispatch}
          onSubmit={onVerifySubmit}
          onResend={onResendVerification}
          verifyPending={pending.verify}
          resendPending={pending.resend}
        />
      );
    case 'FORGOT_PASSWORD':
      return (
        <ForgotPasswordScreen
          flow={flow}
          dispatch={dispatch}
          onSubmit={onRecoverySubmit}
          pending={pending.recovery}
        />
      );
    case 'RESET_PASSWORD':
      return (
        <ResetPasswordScreen
          flow={flow}
          onSubmit={onResetPassword}
          pending={pending.reset}
        />
      );
    case 'REAUTH':
      return (
        <ReauthenticateScreen
          flow={flow}
          dispatch={dispatch}
          onSubmit={onReauthenticate}
          pending={pending.reauth}
        />
      );
    case 'AUTHENTICATED_RETURN':
      return (
        <AccessAuthenticatedReturnPanel
          condition={flow.condition}
          onLogOut={onLogOut}
          pending={pending.logOut}
        />
      );
    default:
      return <AccessDownstreamPanel flow={flow} dispatch={dispatch} />;
  }
}
