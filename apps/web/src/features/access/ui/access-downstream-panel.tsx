import { useState, type Dispatch, type FormEvent } from 'react';
import { useTranslation } from 'react-i18next';

import {
  isValidNewPassword,
  type AccessFlowEvent,
  type AccessFlowState,
  type AccessProvider,
} from '../model/access-flow';
import { AccessConditionNotice } from './access-condition-notice';
import {
  AccessPanelFrame,
  AccessPasswordToggle,
} from './access-panel-frame';

type DownstreamProps = Readonly<{
  flow: AccessFlowState;
  dispatch: Dispatch<AccessFlowEvent>;
}>;

function providerName(
  provider: AccessProvider,
  t: ReturnType<typeof useTranslation<'common'>>['t'],
) {
  return provider === 'google'
    ? t(($) => $.common.access.provider.googleName)
    : t(($) => $.common.access.provider.appleName);
}

function VerifyEmailScreen({ flow, dispatch }: DownstreamProps) {
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
    dispatch({ type: 'REQUEST_VERIFY_EMAIL' });
  }

  return (
    <AccessPanelFrame
      titleId="access-verify-title"
      kicker={t(($) => $.common.access.kicker.access)}
      title={t(($) => $.common.access.verify.title)}
      body={t(($) => $.common.access.verify.body)}
    >
      <div className="access-progress" aria-label={t(($) => $.common.access.signup.progress)}>
        <span>{t(($) => $.common.access.signup.stepEmail)}</span>
        <span>{t(($) => $.common.access.signup.stepPassword)}</span>
        <span className="is-active">{t(($) => $.common.access.signup.stepVerify)}</span>
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
            aria-invalid={Boolean(error)}
            aria-describedby={
              error ? 'access-verification-code-error' : 'access-verification-code-help'
            }
            onChange={(event) => {
              setCode(event.target.value.replace(/\D/g, '').slice(0, 6));
              setError(null);
            }}
          />
          {error ? (
            <span id="access-verification-code-error" className="access-field-error">
              {error}
            </span>
          ) : null}
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

      <p id="access-verification-code-help" className="access-security-note">
        {t(($) => $.common.access.verify.privacy)}
      </p>
      <AccessConditionNotice condition={flow.condition} />
    </AccessPanelFrame>
  );
}

function RecoverySentScreen({ flow, dispatch }: DownstreamProps) {
  const { t } = useTranslation('common');
  const email = flow.screen.id === 'RECOVERY_SENT' ? flow.screen.email : '';

  return (
    <AccessPanelFrame
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
    </AccessPanelFrame>
  );
}

function ResetPasswordScreen({ flow, dispatch }: DownstreamProps) {
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
    const mismatchError = !minimumError && password !== confirm
      ? t(($) => $.common.access.validation.passwordMismatch)
      : null;

    setPasswordError(minimumError);
    setConfirmError(mismatchError);

    if (minimumError || mismatchError) {
      return;
    }

    dispatch({ type: 'REQUEST_RESET_PASSWORD' });
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
              aria-invalid={Boolean(passwordError)}
              aria-describedby={
                passwordError ? 'access-reset-password-error' : 'access-reset-password-guide'
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
            <span id="access-reset-password-error" className="access-field-error">
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
              aria-invalid={Boolean(confirmError)}
              aria-describedby={confirmError ? 'access-reset-confirm-error' : undefined}
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
            <span id="access-reset-confirm-error" className="access-field-error">
              {confirmError}
            </span>
          ) : null}
        </div>

        <button className="access-primary-button" type="submit">
          {t(($) => $.common.access.reset.action)}
        </button>
      </form>
      <AccessConditionNotice condition={flow.condition} />
    </AccessPanelFrame>
  );
}

function SetupNameScreen({ dispatch }: Pick<DownstreamProps, 'dispatch'>) {
  const { t } = useTranslation('common');
  const [name, setName] = useState('');
  const [error, setError] = useState<string | null>(null);

  function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const preferredName = name.trim();
    if (!preferredName) {
      setError(t(($) => $.common.access.validation.preferredName));
      return;
    }
    dispatch({ type: 'SETUP_NAME_ACCEPTED', preferredName });
  }

  return (
    <AccessPanelFrame
      titleId="access-setup-name-title"
      kicker={t(($) => $.common.access.kicker.setup)}
      title={t(($) => $.common.access.setupName.title)}
      body={t(($) => $.common.access.setupName.body)}
    >
      <form className="access-flow-form" onSubmit={submit} noValidate>
        <div className="access-field">
          <label htmlFor="access-preferred-name">
            {t(($) => $.common.access.setupName.label)}
          </label>
          <input
            id="access-preferred-name"
            name="preferred-name"
            autoComplete="name"
            value={name}
            aria-invalid={Boolean(error)}
            aria-describedby={error ? 'access-preferred-name-error' : undefined}
            onChange={(event) => {
              setName(event.target.value);
              setError(null);
            }}
          />
          {error ? (
            <span id="access-preferred-name-error" className="access-field-error">
              {error}
            </span>
          ) : null}
        </div>
        <button className="access-primary-button" type="submit">
          {t(($) => $.common.access.action.continue)}
        </button>
      </form>
    </AccessPanelFrame>
  );
}

function SetupLocaleScreen({ dispatch }: Pick<DownstreamProps, 'dispatch'>) {
  const { t, i18n } = useTranslation('common');
  const timezone = Intl.DateTimeFormat().resolvedOptions().timeZone || 'UTC';
  const languageName = i18n.language.toLowerCase().startsWith('it')
    ? t(($) => $.common.access.locale.italian)
    : t(($) => $.common.access.locale.english);

  return (
    <AccessPanelFrame
      titleId="access-setup-locale-title"
      kicker={t(($) => $.common.access.kicker.setup)}
      title={t(($) => $.common.access.setupLocale.title)}
      body={t(($) => $.common.access.setupLocale.body)}
    >
      <dl className="access-settings-summary">
        <div>
          <dt>{t(($) => $.common.access.setupLocale.language)}</dt>
          <dd>{languageName}</dd>
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
    </AccessPanelFrame>
  );
}

function SetupStartScreen({ dispatch }: Pick<DownstreamProps, 'dispatch'>) {
  const { t } = useTranslation('common');
  const choices = [
    ['real', t(($) => $.common.access.start.real), t(($) => $.common.access.start.realBody)],
    ['import', t(($) => $.common.access.start.import), t(($) => $.common.access.start.importBody)],
    ['demo', t(($) => $.common.access.start.demo), t(($) => $.common.access.start.demoBody)],
    ['skip', t(($) => $.common.access.start.skip), t(($) => $.common.access.start.skipBody)],
  ] as const;

  return (
    <AccessPanelFrame
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
    </AccessPanelFrame>
  );
}

function FirstActionScreen({ flow, dispatch }: DownstreamProps) {
  const { t } = useTranslation('common');
  const [value, setValue] = useState('');
  const [error, setError] = useState<string | null>(null);

  function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (!value.trim()) {
      setError(t(($) => $.common.access.validation.firstAction));
      return;
    }
    dispatch({ type: 'REQUEST_FIRST_ACTION' });
  }

  return (
    <AccessPanelFrame
      titleId="access-first-action-title"
      kicker={t(($) => $.common.access.kicker.setup)}
      title={t(($) => $.common.access.firstAction.title)}
      body={t(($) => $.common.access.firstAction.body)}
    >
      <form className="access-flow-form" onSubmit={submit} noValidate>
        <div className="access-field">
          <label htmlFor="access-first-action">
            {t(($) => $.common.access.firstAction.label)}
          </label>
          <input
            id="access-first-action"
            value={value}
            aria-invalid={Boolean(error)}
            aria-describedby={error ? 'access-first-action-error' : undefined}
            onChange={(event) => {
              setValue(event.target.value);
              setError(null);
            }}
          />
          {error ? (
            <span id="access-first-action-error" className="access-field-error">
              {error}
            </span>
          ) : null}
        </div>
        <button className="access-primary-button" type="submit">
          {t(($) => $.common.access.firstAction.action)}
        </button>
      </form>
      <AccessConditionNotice condition={flow.condition} />
    </AccessPanelFrame>
  );
}

function ImportScreen({ flow, dispatch }: DownstreamProps) {
  const { t } = useTranslation('common');

  return (
    <AccessPanelFrame
      titleId="access-import-title"
      kicker={t(($) => $.common.access.kicker.setup)}
      title={t(($) => $.common.access.importFlow.title)}
      body={t(($) => $.common.access.importFlow.body)}
    >
      <div className="access-info-stack">
        <p>{t(($) => $.common.access.importFlow.google)}</p>
        <p>{t(($) => $.common.access.importFlow.file)}</p>
      </div>
      <button
        className="access-primary-button"
        type="button"
        onClick={() => dispatch({ type: 'REQUEST_IMPORT' })}
      >
        {t(($) => $.common.access.action.continue)}
      </button>
      <AccessConditionNotice condition={flow.condition} />
    </AccessPanelFrame>
  );
}

export function AccessDownstreamPanel({ flow, dispatch }: DownstreamProps) {
  const { t } = useTranslation('common');
  const screen = flow.screen;

  switch (screen.id) {
    case 'VERIFY_EMAIL':
      return <VerifyEmailScreen flow={flow} dispatch={dispatch} />;
    case 'RECOVERY_SENT':
      return <RecoverySentScreen flow={flow} dispatch={dispatch} />;
    case 'RESET_PASSWORD':
      return <ResetPasswordScreen flow={flow} dispatch={dispatch} />;
    case 'RESET_COMPLETE':
      return (
        <AccessPanelFrame
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
        </AccessPanelFrame>
      );
    case 'PROVIDER_PENDING': {
      const name = providerName(screen.provider, t);
      return (
        <AccessPanelFrame
          titleId="access-provider-pending-title"
          kicker={t(($) => $.common.access.kicker.access)}
          title={t(($) => $.common.access.provider.wait)}
          body={t(($) => $.common.access.provider.pendingBody)}
        >
          <div className="access-provider-context" aria-label={name}>
            <span>{name}</span>
            <div className="access-wait-indicator" aria-hidden="true" />
          </div>
          <p className="access-security-note">
            {t(($) => $.common.access.provider.scopeNote)}
          </p>
        </AccessPanelFrame>
      );
    }
    case 'PROVIDER_ERROR': {
      const name = providerName(screen.provider, t);
      return (
        <AccessPanelFrame
          titleId="access-provider-error-title"
          kicker={t(($) => $.common.access.kicker.access)}
          title={t(($) => $.common.access.providerError.title)}
          body={t(($) => $.common.access.providerError.body)}
        >
          <p className="access-provider-label">{name}</p>
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
        </AccessPanelFrame>
      );
    }
    case 'ACCOUNT_LINK': {
      const name = providerName(screen.provider, t);
      return (
        <AccessPanelFrame
          titleId="access-link-title"
          kicker={t(($) => $.common.access.kicker.access)}
          title={t(($) => $.common.access.link.title)}
          body={t(($) => $.common.access.link.body)}
        >
          <p className="access-provider-label">{name}</p>
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
        </AccessPanelFrame>
      );
    }
    case 'AUTHENTICATED_RETURN':
      return (
        <AccessPanelFrame
          titleId="access-authenticated-return-title"
          kicker={t(($) => $.common.access.kicker.access)}
          title={t(($) => $.common.access.authenticated.title)}
          body={t(($) => $.common.access.authenticated.body)}
        >
          <div className="access-completion-mark" aria-hidden="true">✓</div>
        </AccessPanelFrame>
      );
    case 'REAUTH':
      return (
        <AccessPanelFrame
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
            {t(($) => $.common.access.reauth.action)}
          </button>
          <button
            className="access-secondary-button"
            type="button"
            onClick={() => dispatch({ type: 'REAUTH_CANCEL' })}
          >
            {t(($) => $.common.access.action.cancel)}
          </button>
          <AccessConditionNotice condition={flow.condition} />
        </AccessPanelFrame>
      );
    case 'SETUP_NAME':
      return <SetupNameScreen dispatch={dispatch} />;
    case 'SETUP_LOCALE':
      return <SetupLocaleScreen dispatch={dispatch} />;
    case 'SETUP_START':
      return <SetupStartScreen dispatch={dispatch} />;
    case 'FIRST_ACTION':
      return <FirstActionScreen flow={flow} dispatch={dispatch} />;
    case 'IMPORT':
      return <ImportScreen flow={flow} dispatch={dispatch} />;
    case 'DEMO':
      return (
        <AccessPanelFrame
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
        </AccessPanelFrame>
      );
    case 'HOME_HANDOFF':
      return (
        <AccessPanelFrame
          titleId="access-home-handoff-title"
          kicker={t(($) => $.common.access.kicker.setup)}
          title={t(($) => $.common.access.home.title)}
          body={t(($) => $.common.access.home.body)}
        >
          <div className="access-completion-mark" aria-hidden="true">✓</div>
        </AccessPanelFrame>
      );
    default:
      return null;
  }
}
