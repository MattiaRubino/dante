import {
  useState,
  type Dispatch,
  type FormEvent,
  type ReactNode,
} from 'react';
import { useTranslation } from 'react-i18next';

import {
  isValidAccessEmail,
  isValidNewPassword,
  type AccessFlowEvent,
  type AccessFlowState,
  type AccessProvider,
} from '../model/access-flow';
import { AccessConditionNotice } from './access-condition-notice';
import { AccessSignInPanel } from './access-sign-in-panel';
import { ProviderButton } from './provider-button';

type FlowProps = Readonly<{
  flow: AccessFlowState;
  dispatch: Dispatch<AccessFlowEvent>;
}>;

type PanelFrameProps = Readonly<{
  titleId: string;
  kicker: string;
  title: string;
  body?: string;
  onBack?: () => void;
  children: ReactNode;
  footer?: ReactNode;
}>;

function PanelFrame({
  titleId,
  kicker,
  title,
  body,
  onBack,
  children,
  footer,
}: PanelFrameProps) {
  const { t } = useTranslation('common');

  return (
    <section className="access-panel" aria-labelledby={titleId}>
      <div className="access-panel-inner">
        <div className="access-panel-heading-row">
          <p className="access-kicker">{kicker}</p>
          {onBack ? (
            <button
              className="access-inline-action access-back-action"
              type="button"
              onClick={onBack}
            >
              ← {t(($) => $.common.access.action.back)}
            </button>
          ) : null}
        </div>
        <h1 id={titleId}>{title}</h1>
        {body ? <p className="access-signin-copy">{body}</p> : null}
        <div className="access-flow-content">{children}</div>
        {footer ? <div className="access-flow-footer">{footer}</div> : null}
      </div>
    </section>
  );
}

function PasswordToggle({
  showPassword,
  onToggle,
}: Readonly<{ showPassword: boolean; onToggle: () => void }>) {
  const { t } = useTranslation('common');
  const label = showPassword
    ? t(($) => $.common.access.action.hidePassword)
    : t(($) => $.common.access.action.showPassword);

  return (
    <button
      className="access-password-toggle"
      type="button"
      aria-label={label}
      aria-pressed={showPassword}
      onClick={onToggle}
    >
      <svg
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
        strokeWidth="1.8"
        focusable="false"
        aria-hidden="true"
      >
        <path d="M2.5 12s3.4-6 9.5-6 9.5 6 9.5 6-3.4 6-9.5 6-9.5-6-9.5-6Z" />
        <circle cx="12" cy="12" r="2.7" />
        {showPassword ? <path d="m4 4 16 16" /> : null}
      </svg>
    </button>
  );
}

function SignupEmailScreen({ flow, dispatch }: FlowProps) {
  const { t } = useTranslation('common');
  const initialEmail =
    flow.screen.id === 'SIGN_UP_EMAIL' ? flow.screen.email : '';
  const [email, setEmail] = useState(initialEmail);
  const [error, setError] = useState<string>();

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
    <PanelFrame
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
      <div className="access-progress" aria-label={t(($) => $.common.access.signup.progress)}>
        <span className="is-active">{t(($) => $.common.access.signup.stepEmail)}</span>
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
              setError(undefined);
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
    </PanelFrame>
  );
}

function SignupPasswordScreen({ flow, dispatch }: FlowProps) {
  const { t } = useTranslation('common');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState<string>();
  const email = flow.screen.id === 'SIGN_UP_PASSWORD' ? flow.screen.email : '';

  function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (!isValidNewPassword(password)) {
      setError(t(($) => $.common.access.validation.passwordMinimum));
      return;
    }
    dispatch({ type: 'REQUEST_SIGN_UP' });
  }

  return (
    <PanelFrame
      titleId="access-signup-password-title"
      kicker={t(($) => $.common.access.kicker.access)}
      title={t(($) => $.common.access.signupPassword.title)}
      body={t(($) => $.common.access.signupPassword.body)}
      onBack={() => dispatch({ type: 'CHANGE_SIGN_UP_EMAIL' })}
    >
      <div className="access-progress" aria-label={t(($) => $.common.access.signup.progress)}>
        <span>{t(($) => $.common.access.signup.stepEmail)}</span>
        <span className="is-active">{t(($) => $.common.access.signup.stepPassword)}</span>
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
          <label htmlFor="access-new-password">
            {t(($) => $.common.access.field.password)}
          </label>
          <div className="access-input-wrap">
            <input
              id="access-new-password"
              name="new-password"
              type={showPassword ? 'text' : 'password'}
              autoComplete="new-password"
              value={password}
              aria-invalid={Boolean(error)}
              aria-describedby={error ? 'access-new-password-error' : 'access-password-guide'}
              onChange={(event) => {
                setPassword(event.target.value);
                setError(undefined);
              }}
            />
            <PasswordToggle
              showPassword={showPassword}
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
    </PanelFrame>
  );
}

function ForgotPasswordScreen({ flow, dispatch }: FlowProps) {
  const { t } = useTranslation('common');
  const initialEmail =
    flow.screen.id === 'FORGOT_PASSWORD' ? flow.screen.email : '';
  const [email, setEmail] = useState(initialEmail);
  const [error, setError] = useState<string>();

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
    <PanelFrame
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
            aria-describedby={error ? 'access-recovery-email-error' : undefined}
            onChange={(event) => {
              setEmail(event.target.value);
              setError(undefined);
            }}
          />
          {error ? (
            <span id="access-recovery-email-error" className="access-field-error">
              {error}
            </span>
          ) : null}
        </div>
        <button className="access-primary-button" type="submit">
          {t(($) => $.common.access.forgot.action)}
        </button>
      </form>
      <p className="access-security-note">
        {t(($) => $.common.access.forgot.privacy)}
      </p>
      <AccessConditionNotice condition={flow.condition} />
    </PanelFrame>
  );
}

function VerifyEmailScreen({ flow, dispatch }: FlowProps) {
  const { t } = useTranslation('common');
  const [code, setCode] = useState('');
  const [error, setError] = useState<string>();
  const email = flow.screen.id === 'VERIFY_EMAIL' ? flow.screen.email : '';

  function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (!/^\d{6}$/.test(code)) {
      setError(t(($) => $.common.access.validation.verificationCode));
      return;
    }
    dispatch({ type: 'REQUEST_VERIFY_EMAIL' });
  }

  return (
    <PanelFrame
      titleId="access-verify-title"
      kicker={t(($) => $.common.access.kicker.access)}
      title={t(($) => $.common.access.verify.title)}
      body={t(($) => $.common.access.verify.body)}
    >
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
            aria-invalid={Boolean(error)}
            onChange={(event) => {
              setCode(event.target.value.replace(/\D/g, '').slice(0, 6));
              setError(undefined);
            }}
          />
          {error ? <span className="access-field-error">{error}</span> : null}
        </div>
        <button className="access-primary-button" type="submit">
          {t(($) => $.common.access.verify.action)}
        </button>
      </form>
      <div className="access-secondary-actions">
        <button
          className="access-inline-action"
          type="button"
          onClick={() => dispatch({ type: 'REQUEST_RESEND_VERIFICATION' })}
        >
          {t(($) => $.common.access.verify.resend)}
        </button>
        <button
          className="access-inline-action"
          type="button"
          onClick={() => dispatch({ type: 'CREATE_ACCOUNT' })}
        >
          {t(($) => $.common.access.action.changeEmail)}
        </button>
      </div>
      <p className="access-security-note">
        {t(($) => $.common.access.verify.privacy)}
      </p>
      <AccessConditionNotice condition={flow.condition} />
    </PanelFrame>
  );
}

function RecoverySentScreen({ flow, dispatch }: FlowProps) {
  const { t } = useTranslation('common');
  const email = flow.screen.id === 'RECOVERY_SENT' ? flow.screen.email : '';

  return (
    <PanelFrame
      titleId="access-recovery-sent-title"
      kicker={t(($) => $.common.access.kicker.access)}
      title={t(($) => $.common.access.recovery.title)}
      body={t(($) => $.common.access.recovery.body)}
    >
      <p className="access-email-context">{email}</p>
      <button
        className="access-primary-button"
        type="button"
        onClick={() => dispatch({ type: 'RECOVERY_SENT_CONTINUE' })}
      >
        {t(($) => $.common.access.action.backSignin)}
      </button>
    </PanelFrame>
  );
}

function ResetPasswordScreen({ flow, dispatch }: FlowProps) {
  const { t } = useTranslation('common');
  const [password, setPassword] = useState('');
  const [confirm, setConfirm] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState<string>();

  function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (!isValidNewPassword(password)) {
      setError(t(($) => $.common.access.validation.passwordMinimum));
      return;
    }
    if (password !== confirm) {
      setError(t(($) => $.common.access.validation.passwordMismatch));
      return;
    }
    dispatch({ type: 'REQUEST_RESET_PASSWORD' });
  }

  return (
    <PanelFrame
      titleId="access-reset-title"
      kicker={t(($) => $.common.access.kicker.access)}
      title={t(($) => $.common.access.reset.title)}
      body={t(($) => $.common.access.reset.body)}
    >
      <form className="access-flow-form" onSubmit={submit} noValidate>
        <div className="access-field">
          <label htmlFor="access-reset-password">
            {t(($) => $.common.access.reset.new)}
          </label>
          <div className="access-input-wrap">
            <input
              id="access-reset-password"
              type={showPassword ? 'text' : 'password'}
              autoComplete="new-password"
              value={password}
              onChange={(event) => {
                setPassword(event.target.value);
                setError(undefined);
              }}
            />
            <PasswordToggle
              showPassword={showPassword}
              onToggle={() => setShowPassword((value) => !value)}
            />
          </div>
        </div>
        <div className="access-field">
          <label htmlFor="access-reset-confirm">
            {t(($) => $.common.access.reset.confirm)}
          </label>
          <input
            id="access-reset-confirm"
            type={showPassword ? 'text' : 'password'}
            autoComplete="new-password"
            value={confirm}
            aria-invalid={Boolean(error)}
            onChange={(event) => {
              setConfirm(event.target.value);
              setError(undefined);
            }}
          />
          {error ? <span className="access-field-error">{error}</span> : null}
        </div>
        <button className="access-primary-button" type="submit">
          {t(($) => $.common.access.reset.action)}
        </button>
      </form>
      <AccessConditionNotice condition={flow.condition} />
    </PanelFrame>
  );
}

function SetupNameScreen({ dispatch }: Pick<FlowProps, 'dispatch'>) {
  const { t } = useTranslation('common');
  const [name, setName] = useState('');

  return (
    <PanelFrame
      titleId="access-setup-name-title"
      kicker={t(($) => $.common.access.kicker.setup)}
      title={t(($) => $.common.access.setupName.title)}
      body={t(($) => $.common.access.setupName.body)}
    >
      <form
        className="access-flow-form"
        onSubmit={(event) => {
          event.preventDefault();
          dispatch({ type: 'SETUP_NAME_ACCEPTED', preferredName: name.trim() });
        }}
      >
        <div className="access-field">
          <label htmlFor="access-preferred-name">
            {t(($) => $.common.access.setupName.label)}
          </label>
          <input
            id="access-preferred-name"
            autoComplete="name"
            value={name}
            onChange={(event) => setName(event.target.value)}
          />
        </div>
        <button className="access-primary-button" type="submit">
          {t(($) => $.common.access.action.continue)}
        </button>
      </form>
    </PanelFrame>
  );
}

function SetupLocaleScreen({ dispatch }: Pick<FlowProps, 'dispatch'>) {
  const { t, i18n } = useTranslation('common');
  const timezone = Intl.DateTimeFormat().resolvedOptions().timeZone || 'UTC';

  return (
    <PanelFrame
      titleId="access-setup-locale-title"
      kicker={t(($) => $.common.access.kicker.setup)}
      title={t(($) => $.common.access.setupLocale.title)}
      body={t(($) => $.common.access.setupLocale.body)}
    >
      <dl className="access-settings-summary">
        <div>
          <dt>{t(($) => $.common.access.setupLocale.language)}</dt>
          <dd>{i18n.language.toLowerCase().startsWith('it') ? 'Italiano' : 'English'}</dd>
        </div>
        <div>
          <dt>{t(($) => $.common.access.setupLocale.timezone)}</dt>
          <dd>{timezone}</dd>
        </div>
      </dl>
      <p className="access-security-note">
        {t(($) => $.common.access.setupLocale.note)}
      </p>
      <button
        className="access-primary-button"
        type="button"
        onClick={() => dispatch({ type: 'SETUP_LOCALE_ACCEPTED' })}
      >
        {t(($) => $.common.access.action.continue)}
      </button>
    </PanelFrame>
  );
}

function SetupStartScreen({ dispatch }: Pick<FlowProps, 'dispatch'>) {
  const { t } = useTranslation('common');
  const choices = [
    ['real', t(($) => $.common.access.start.real), t(($) => $.common.access.start.realBody)],
    ['import', t(($) => $.common.access.start.import), t(($) => $.common.access.start.importBody)],
    ['demo', t(($) => $.common.access.start.demo), t(($) => $.common.access.start.demoBody)],
    ['skip', t(($) => $.common.access.start.skip), t(($) => $.common.access.start.skipBody)],
  ] as const;

  return (
    <PanelFrame
      titleId="access-setup-start-title"
      kicker={t(($) => $.common.access.kicker.setup)}
      title={t(($) => $.common.access.setupStart.title)}
      body={t(($) => $.common.access.setupStart.body)}
    >
      <div className="access-choice-list">
        {choices.map(([choice, title, body]) => (
          <button
            key={choice}
            className="access-choice-card"
            type="button"
            onClick={() => dispatch({ type: 'SETUP_START_CHOICE', choice })}
          >
            <strong>{title}</strong>
            <span>{body}</span>
          </button>
        ))}
      </div>
    </PanelFrame>
  );
}

function PreparedBackendScreen({
  flow,
  dispatch,
  kind,
}: FlowProps & Readonly<{ kind: 'first-action' | 'import' }>) {
  const { t } = useTranslation('common');
  const isFirstAction = kind === 'first-action';
  const [value, setValue] = useState('');

  return (
    <PanelFrame
      titleId={isFirstAction ? 'access-first-action-title' : 'access-import-title'}
      kicker={t(($) => $.common.access.kicker.setup)}
      title={
        isFirstAction
          ? t(($) => $.common.access.firstAction.title)
          : t(($) => $.common.access.importFlow.title)
      }
      body={
        isFirstAction
          ? t(($) => $.common.access.firstAction.body)
          : t(($) => $.common.access.importFlow.body)
      }
    >
      {isFirstAction ? (
        <div className="access-field">
          <label htmlFor="access-first-action">
            {t(($) => $.common.access.firstAction.label)}
          </label>
          <input
            id="access-first-action"
            value={value}
            onChange={(event) => setValue(event.target.value)}
          />
        </div>
      ) : (
        <div className="access-info-stack">
          <p>{t(($) => $.common.access.importFlow.google)}</p>
          <p>{t(($) => $.common.access.importFlow.file)}</p>
        </div>
      )}
      <button
        className="access-primary-button"
        type="button"
        onClick={() =>
          dispatch({ type: isFirstAction ? 'REQUEST_FIRST_ACTION' : 'REQUEST_IMPORT' })
        }
      >
        {isFirstAction
          ? t(($) => $.common.access.firstAction.action)
          : t(($) => $.common.access.action.continue)}
      </button>
      <AccessConditionNotice condition={flow.condition} />
    </PanelFrame>
  );
}

export function AccessFlowPanel({ flow, dispatch }: FlowProps) {
  const { t } = useTranslation('common');
  const screen = flow.screen;

  switch (screen.id) {
    case 'SIGN_IN':
      return (
        <AccessSignInPanel
          condition={flow.condition}
          onCreateAccount={() => dispatch({ type: 'CREATE_ACCOUNT' })}
          onForgotPassword={() => dispatch({ type: 'FORGOT_PASSWORD' })}
          onCredentialSubmit={() => dispatch({ type: 'REQUEST_SIGN_IN' })}
          onProvider={(provider) => dispatch({ type: 'REQUEST_PROVIDER', provider })}
        />
      );
    case 'SIGN_UP_EMAIL':
      return <SignupEmailScreen flow={flow} dispatch={dispatch} />;
    case 'SIGN_UP_PASSWORD':
      return <SignupPasswordScreen flow={flow} dispatch={dispatch} />;
    case 'VERIFY_EMAIL':
      return <VerifyEmailScreen flow={flow} dispatch={dispatch} />;
    case 'FORGOT_PASSWORD':
      return <ForgotPasswordScreen flow={flow} dispatch={dispatch} />;
    case 'RECOVERY_SENT':
      return <RecoverySentScreen flow={flow} dispatch={dispatch} />;
    case 'RESET_PASSWORD':
      return <ResetPasswordScreen flow={flow} dispatch={dispatch} />;
    case 'RESET_COMPLETE':
      return (
        <PanelFrame
          titleId="access-reset-complete-title"
          kicker={t(($) => $.common.access.kicker.access)}
          title={t(($) => $.common.access.reset.doneTitle)}
          body={t(($) => $.common.access.reset.doneBody)}
        >
          <button
            className="access-primary-button"
            type="button"
            onClick={() => dispatch({ type: 'RESET_COMPLETE_CONTINUE' })}
          >
            {t(($) => $.common.access.action.backSignin)}
          </button>
        </PanelFrame>
      );
    case 'PROVIDER_PENDING':
      return (
        <PanelFrame
          titleId="access-provider-pending-title"
          kicker={t(($) => $.common.access.kicker.access)}
          title={t(($) => $.common.access.provider.wait)}
          body={t(($) => $.common.access.provider.body)}
        >
          <div className="access-wait-indicator" aria-hidden="true" />
          <p className="access-security-note">
            {t(($) => $.common.access.provider.scopeNote)}
          </p>
        </PanelFrame>
      );
    case 'PROVIDER_ERROR':
      return (
        <PanelFrame
          titleId="access-provider-error-title"
          kicker={t(($) => $.common.access.kicker.access)}
          title={t(($) => $.common.access.providerError.title)}
          body={t(($) => $.common.access.providerError.body)}
        >
          <p className="access-security-note">
            <strong>{t(($) => $.common.access.providerError.safe)}</strong>{' '}
            {t(($) => $.common.access.providerError.retry)}
          </p>
          <button
            className="access-primary-button"
            type="button"
            onClick={() => dispatch({ type: 'PROVIDER_RETRY' })}
          >
            {t(($) => $.common.access.action.tryAgain)}
          </button>
        </PanelFrame>
      );
    case 'ACCOUNT_LINK':
      return (
        <PanelFrame
          titleId="access-link-title"
          kicker={t(($) => $.common.access.kicker.access)}
          title={t(($) => $.common.access.link.title)}
          body={t(($) => $.common.access.link.body)}
        >
          {screen.email ? <p className="access-email-context">{screen.email}</p> : null}
          <button
            className="access-primary-button"
            type="button"
            onClick={() => dispatch({ type: 'REQUEST_ACCOUNT_LINK' })}
          >
            {t(($) => $.common.access.link.action)}
          </button>
          <button
            className="access-secondary-button"
            type="button"
            onClick={() => dispatch({ type: 'ACCOUNT_LINK_OTHER_ACCOUNT' })}
          >
            {t(($) => $.common.access.link.other)}
          </button>
          <AccessConditionNotice condition={flow.condition} />
        </PanelFrame>
      );
    case 'AUTHENTICATED_RETURN':
      return (
        <PanelFrame
          titleId="access-authenticated-return-title"
          kicker={t(($) => $.common.access.kicker.access)}
          title={t(($) => $.common.access.authenticated.title)}
          body={t(($) => $.common.access.authenticated.body)}
        >
          <AccessConditionNotice
            condition={{ kind: 'backend-required', operation: 'sign-in' }}
          />
        </PanelFrame>
      );
    case 'REAUTH':
      return (
        <PanelFrame
          titleId="access-reauth-title"
          kicker={t(($) => $.common.access.kicker.access)}
          title={t(($) => $.common.access.reauth.title)}
          body={t(($) => $.common.access.reauth.body)}
        >
          <button
            className="access-primary-button"
            type="button"
            onClick={() => dispatch({ type: 'REQUEST_REAUTH' })}
          >
            {t(($) => $.common.access.action.signin)}
          </button>
          <button
            className="access-secondary-button"
            type="button"
            onClick={() => dispatch({ type: 'REAUTH_CANCEL' })}
          >
            {t(($) => $.common.access.action.cancel)}
          </button>
          <AccessConditionNotice condition={flow.condition} />
        </PanelFrame>
      );
    case 'SETUP_NAME':
      return <SetupNameScreen dispatch={dispatch} />;
    case 'SETUP_LOCALE':
      return <SetupLocaleScreen dispatch={dispatch} />;
    case 'SETUP_START':
      return <SetupStartScreen dispatch={dispatch} />;
    case 'FIRST_ACTION':
      return (
        <PreparedBackendScreen
          flow={flow}
          dispatch={dispatch}
          kind="first-action"
        />
      );
    case 'IMPORT':
      return <PreparedBackendScreen flow={flow} dispatch={dispatch} kind="import" />;
    case 'DEMO':
      return (
        <PanelFrame
          titleId="access-demo-title"
          kicker={t(($) => $.common.access.kicker.setup)}
          title={t(($) => $.common.access.demo.title)}
          body={t(($) => $.common.access.demo.body)}
        >
          <div className="access-demo-card">
            <strong>{t(($) => $.common.access.demo.item)}</strong>
            <span>{t(($) => $.common.access.demo.itemBody)}</span>
          </div>
          <button
            className="access-primary-button"
            type="button"
            onClick={() => dispatch({ type: 'DEMO_COMPLETE' })}
          >
            {t(($) => $.common.access.demo.action)}
          </button>
        </PanelFrame>
      );
    case 'HOME_HANDOFF':
      return (
        <PanelFrame
          titleId="access-home-handoff-title"
          kicker={t(($) => $.common.access.kicker.setup)}
          title={t(($) => $.common.access.home.title)}
          body={t(($) => $.common.access.home.body)}
        >
          <p className="access-security-note">
            {t(($) => $.common.access.home.pending)}
          </p>
        </PanelFrame>
      );
  }
}
