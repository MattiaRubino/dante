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

type AccessFlowPanelProps = FlowProps &
  Readonly<{
    onCredentialSubmit: (email: string, password: string) => void;
    onLogOut: () => void;
    signInPending: boolean;
    logOutPending: boolean;
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

function SignupPasswordScreen({ flow, dispatch }: FlowProps) {
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
    dispatch({ type: 'REQUEST_SIGN_UP' });
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

        <button className="access-primary-button" type="submit">
          {t(($) => $.common.access.action.createAccount)}
        </button>
      </form>
      <AccessConditionNotice condition={flow.condition} />
    </AccessPanelFrame>
  );
}

function ForgotPasswordScreen({ flow, dispatch }: FlowProps) {
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
    dispatch({ type: 'REQUEST_RECOVERY', email: trimmedEmail });
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
        <button className="access-primary-button" type="submit">
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

export function AccessFlowPanel({
  flow,
  dispatch,
  onCredentialSubmit,
  onLogOut,
  signInPending,
  logOutPending,
}: AccessFlowPanelProps) {
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
          pending={signInPending}
        />
      );
    case 'SIGN_UP_EMAIL':
      return <SignupEmailScreen flow={flow} dispatch={dispatch} />;
    case 'SIGN_UP_PASSWORD':
      return <SignupPasswordScreen flow={flow} dispatch={dispatch} />;
    case 'FORGOT_PASSWORD':
      return <ForgotPasswordScreen flow={flow} dispatch={dispatch} />;
    case 'AUTHENTICATED_RETURN':
      return (
        <AccessAuthenticatedReturnPanel
          condition={flow.condition}
          onLogOut={onLogOut}
          pending={logOutPending}
        />
      );
    default:
      return <AccessDownstreamPanel flow={flow} dispatch={dispatch} />;
  }
}
