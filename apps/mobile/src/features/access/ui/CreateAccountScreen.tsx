import { useEffect, useReducer, useState } from 'react';
import {
  BackHandler,
  Keyboard,
  Pressable,
  StyleSheet,
  Text,
  View,
} from 'react-native';
import { useTranslation } from 'react-i18next';

import {
  initialSignUpFlowState,
  normalizeSignUpEmail,
  signUpFlowReducer,
  validateSignUpEmail,
  validateSignUpPassword,
  validateVerificationCode,
  type SignUpEmailError,
  type SignUpPasswordError,
  type SignUpVerificationError,
} from '../model/signUpFlow';
import { accessTheme } from '../theme/accessTheme';
import { AccessBrandLockup } from './AccessBrandLockup';
import { AccessButton } from './AccessButton';
import { AccessFieldError } from './AccessFieldError';
import { AccessOtpField } from './AccessOtpField';
import { AccessScreen } from './AccessScreen';
import { AccessTextField } from './AccessTextField';
import { SignUpProgress } from './SignUpProgress';

type CreateAccountScreenProps = Readonly<{
  onBackToSignIn: () => void;
  onRequestCreateAccount?: (
    email: string,
    password: string,
  ) => void | Promise<void>;
  onVerifyCode?: (email: string, code: string) => void | Promise<void>;
  onResendCode?: (email: string) => void | Promise<void>;
}>;

export function CreateAccountScreen({
  onBackToSignIn,
  onRequestCreateAccount,
  onVerifyCode,
  onResendCode,
}: CreateAccountScreenProps) {
  const { t } = useTranslation('common');
  const [flow, dispatch] = useReducer(
    signUpFlowReducer,
    initialSignUpFlowState,
  );
  const [password, setPassword] = useState('');
  const [verificationCode, setVerificationCode] = useState('');
  const [emailError, setEmailError] = useState<SignUpEmailError | null>(null);
  const [passwordError, setPasswordError] =
    useState<SignUpPasswordError | null>(null);
  const [verificationError, setVerificationError] =
    useState<SignUpVerificationError | null>(null);
  const [creating, setCreating] = useState(false);
  const [verifying, setVerifying] = useState(false);
  const [resending, setResending] = useState(false);
  const [operationError, setOperationError] = useState<string | null>(null);

  const interactionPending = creating || verifying || resending;

  function resetToEmail() {
    Keyboard.dismiss();
    dispatch({ type: 'CHANGE_SIGN_UP_EMAIL' });
    setPassword('');
    setVerificationCode('');
    setPasswordError(null);
    setVerificationError(null);
    setOperationError(null);
  }

  useEffect(() => {
    const subscription = BackHandler.addEventListener(
      'hardwareBackPress',
      () => {
        if (flow.step === 'email') {
          return false;
        }

        resetToEmail();
        return true;
      },
    );

    return () => subscription.remove();
  }, [flow.step]);

  function handleBack() {
    if (interactionPending) {
      return;
    }

    if (flow.step === 'email') {
      onBackToSignIn();
      return;
    }

    resetToEmail();
  }

  function handleEmailChange(value: string) {
    dispatch({ type: 'EDIT_EMAIL', email: value });
    if (emailError !== null) {
      setEmailError(validateSignUpEmail(value));
    }
    setOperationError(null);
  }

  function handleEmailContinue() {
    const normalizedEmail = normalizeSignUpEmail(flow.email);
    const nextError = validateSignUpEmail(normalizedEmail);

    dispatch({ type: 'EDIT_EMAIL', email: normalizedEmail });
    setEmailError(nextError);
    setOperationError(null);

    if (nextError !== null) {
      return;
    }

    Keyboard.dismiss();
    dispatch({ type: 'SIGN_UP_EMAIL_ACCEPTED', email: normalizedEmail });
  }

  function handlePasswordChange(value: string) {
    setPassword(value);
    if (passwordError !== null) {
      setPasswordError(validateSignUpPassword(value));
    }
    setOperationError(null);
  }

  async function handleCreateAccount() {
    if (creating) {
      return;
    }

    const nextError = validateSignUpPassword(password);
    setPasswordError(nextError);
    setOperationError(null);

    if (nextError !== null) {
      return;
    }

    Keyboard.dismiss();

    if (onRequestCreateAccount === undefined) {
      return;
    }

    setCreating(true);
    try {
      await onRequestCreateAccount(flow.email, password);
      dispatch({ type: 'SERVER_SIGN_UP_CREATED' });
      setVerificationCode('');
      setVerificationError(null);
    } catch {
      setOperationError(t(($) => $.common.access.failure.unexpectedBody));
    } finally {
      setCreating(false);
    }
  }

  function triggerCreateAccount() {
    void handleCreateAccount();
  }

  function handleVerificationChange(value: string) {
    setVerificationCode(value);
    if (verificationError !== null) {
      setVerificationError(validateVerificationCode(value));
    }
    setOperationError(null);
  }

  async function handleVerify() {
    if (verifying) {
      return;
    }

    const nextError = validateVerificationCode(verificationCode);
    setVerificationError(nextError);
    setOperationError(null);

    if (nextError !== null) {
      return;
    }

    Keyboard.dismiss();

    if (onVerifyCode === undefined) {
      return;
    }

    setVerifying(true);
    try {
      await onVerifyCode(flow.email, verificationCode);
    } catch {
      setOperationError(
        t(($) => $.common.access.failure.verificationInvalidBody),
      );
    } finally {
      setVerifying(false);
    }
  }

  function triggerVerify() {
    void handleVerify();
  }

  async function handleResend() {
    if (resending || onResendCode === undefined) {
      return;
    }

    setResending(true);
    setOperationError(null);
    try {
      await onResendCode(flow.email);
    } catch {
      setOperationError(t(($) => $.common.access.failure.unexpectedBody));
    } finally {
      setResending(false);
    }
  }

  function triggerResend() {
    void handleResend();
  }

  const title =
    flow.step === 'email'
      ? t(($) => $.common.access.signup.title)
      : flow.step === 'password'
        ? t(($) => $.common.access.signupPassword.title)
        : t(($) => $.common.access.verify.title);
  const body =
    flow.step === 'email'
      ? t(($) => $.common.access.signup.body)
      : flow.step === 'password'
        ? t(($) => $.common.access.signupPassword.body)
        : t(($) => $.common.access.verify.body);

  const emailErrorMessage =
    emailError === 'email'
      ? t(($) => $.common.access.validation.email)
      : undefined;
  const passwordErrorMessage =
    passwordError === 'passwordMinimum'
      ? t(($) => $.common.access.validation.passwordMinimum)
      : undefined;
  const verificationErrorMessage =
    verificationError === 'verificationCode'
      ? t(($) => $.common.access.validation.verificationCode)
      : undefined;

  return (
    <AccessScreen>
      <View style={styles.frame}>
        <View style={styles.topBar}>
          <Pressable
            accessibilityRole="button"
            accessibilityLabel={t(($) => $.common.access.action.back)}
            accessibilityState={{ disabled: interactionPending }}
            android_ripple={{ color: 'rgba(34,47,55,0.08)', borderless: true }}
            disabled={interactionPending}
            onPress={handleBack}
            hitSlop={8}
            style={({ pressed }) => [
              styles.backButton,
              pressed ? styles.inlinePressed : null,
            ]}
          >
            <Text style={styles.backArrow}>‹</Text>
            <Text style={styles.backLabel}>
              {t(($) => $.common.access.action.back)}
            </Text>
          </Pressable>

          <AccessBrandLockup />
          <View style={styles.topBarSpacer} />
        </View>

        <View style={styles.heading}>
          <Text style={styles.title} accessibilityRole="header">
            {title}
          </Text>
          <Text style={styles.body}>{body}</Text>
        </View>

        <SignUpProgress
          step={flow.step}
          emailLabel={t(($) => $.common.access.signup.stepEmail)}
          passwordLabel={t(($) => $.common.access.signup.stepPassword)}
          verifyLabel={t(($) => $.common.access.signup.stepVerify)}
          accessibilityLabel={t(($) => $.common.access.signup.progress)}
        />

        {flow.step === 'email' ? (
          <>
            <View style={styles.formStack}>
              <AccessTextField
                label={t(($) => $.common.access.field.email)}
                value={flow.email}
                onChangeText={handleEmailChange}
                onBlur={() => {
                  const normalizedEmail = normalizeSignUpEmail(flow.email);
                  dispatch({ type: 'EDIT_EMAIL', email: normalizedEmail });
                  setEmailError(validateSignUpEmail(normalizedEmail));
                }}
                onSubmitEditing={handleEmailContinue}
                placeholder={t(($) => $.common.access.field.emailPlaceholder)}
                autoComplete="email"
                keyboardType="email-address"
                textContentType="emailAddress"
                returnKeyType="next"
                editable={!interactionPending}
                {...(emailErrorMessage === undefined
                  ? {}
                  : { error: emailErrorMessage })}
              />

              <AccessButton
                label={t(($) => $.common.access.signup.continueEmail)}
                onPress={handleEmailContinue}
                disabled={interactionPending}
              />
            </View>

            <View style={styles.existingRow}>
              <Text style={styles.secondaryCopy}>
                {t(($) => $.common.access.signup.existing)}
              </Text>
              <Pressable
                accessibilityRole="button"
                onPress={onBackToSignIn}
                hitSlop={8}
                style={({ pressed }) =>
                  pressed ? styles.inlinePressed : undefined
                }
              >
                <Text style={styles.inlineAction}>
                  {t(($) => $.common.access.action.signin)}
                </Text>
              </Pressable>
            </View>
          </>
        ) : null}

        {flow.step === 'password' ? (
          <View style={styles.formStack}>
            <View style={styles.summaryCard}>
              <View style={styles.summaryText}>
                <Text style={styles.summaryLabel}>
                  {t(($) => $.common.access.field.email)}
                </Text>
                <Text style={styles.summaryValue} numberOfLines={1}>
                  {flow.email}
                </Text>
              </View>
              <Pressable
                accessibilityRole="button"
                accessibilityState={{ disabled: interactionPending }}
                disabled={interactionPending}
                onPress={resetToEmail}
                hitSlop={8}
                style={({ pressed }) =>
                  pressed ? styles.inlinePressed : undefined
                }
              >
                <Text style={styles.inlineAction}>
                  {t(($) => $.common.access.action.changeEmail)}
                </Text>
              </Pressable>
            </View>

            <AccessTextField
              label={t(($) => $.common.access.field.password)}
              value={password}
              onChangeText={handlePasswordChange}
              onBlur={() => setPasswordError(validateSignUpPassword(password))}
              onSubmitEditing={triggerCreateAccount}
              secure
              showLabel={t(($) => $.common.access.action.showPassword)}
              hideLabel={t(($) => $.common.access.action.hidePassword)}
              autoComplete="new-password"
              textContentType="newPassword"
              returnKeyType="done"
              editable={!interactionPending}
              {...(passwordErrorMessage === undefined
                ? {}
                : { error: passwordErrorMessage })}
            />

            <View style={styles.passwordGuide}>
              <View style={styles.guideAccent} />
              <View style={styles.guideCopy}>
                <View style={styles.guideHeading}>
                  <Text style={styles.guideTitle}>
                    {t(($) => $.common.access.password.guideTitle)}
                  </Text>
                  <Text style={styles.guideProposal}>
                    {t(($) => $.common.access.password.proposal)}
                  </Text>
                </View>
                <Text style={styles.guideBody}>
                  {t(($) => $.common.access.password.manager)}
                </Text>
              </View>
            </View>

            <AccessButton
              label={t(($) => $.common.access.action.createAccount)}
              onPress={triggerCreateAccount}
              loading={creating}
              disabled={verifying || resending}
            />

            {operationError !== null ? (
              <AccessFieldError message={operationError} />
            ) : null}
          </View>
        ) : null}

        {flow.step === 'verify' ? (
          <View style={styles.formStack}>
            <View style={styles.verifyContext}>
              <Text style={styles.verifyContextLabel}>
                {t(($) => $.common.access.field.email)}
              </Text>
              <Text style={styles.verifyContextValue} numberOfLines={1}>
                {flow.email}
              </Text>
            </View>

            <AccessOtpField
              label={t(($) => $.common.access.field.verificationCode)}
              value={verificationCode}
              onChangeText={handleVerificationChange}
              onSubmitEditing={triggerVerify}
              editable={!interactionPending}
              {...(verificationErrorMessage === undefined
                ? {}
                : { error: verificationErrorMessage })}
            />

            <AccessButton
              label={t(($) => $.common.access.verify.action)}
              onPress={triggerVerify}
              loading={verifying}
              disabled={resending}
            />

            <View style={styles.secondaryActions}>
              <Pressable
                accessibilityRole="button"
                accessibilityState={{
                  disabled:
                    interactionPending || onResendCode === undefined,
                }}
                disabled={interactionPending || onResendCode === undefined}
                onPress={triggerResend}
                hitSlop={8}
                style={({ pressed }) => [
                  styles.secondaryAction,
                  pressed ? styles.inlinePressed : null,
                  onResendCode === undefined ? styles.actionDisabled : null,
                ]}
              >
                <Text style={styles.inlineAction}>
                  {t(($) => $.common.access.verify.resend)}
                </Text>
              </Pressable>

              <Pressable
                accessibilityRole="button"
                accessibilityState={{ disabled: interactionPending }}
                disabled={interactionPending}
                onPress={resetToEmail}
                hitSlop={8}
                style={({ pressed }) => [
                  styles.secondaryAction,
                  pressed ? styles.inlinePressed : null,
                ]}
              >
                <Text style={styles.inlineAction}>
                  {t(($) => $.common.access.action.changeEmail)}
                </Text>
              </Pressable>
            </View>

            <Text style={styles.securityNote}>
              {t(($) => $.common.access.verify.privacy)}
            </Text>

            {operationError !== null ? (
              <AccessFieldError message={operationError} />
            ) : null}
          </View>
        ) : null}
      </View>
    </AccessScreen>
  );
}

const styles = StyleSheet.create({
  frame: {
    width: '100%',
    maxWidth: 430,
    alignSelf: 'center',
  },
  topBar: {
    position: 'relative',
    minHeight: 72,
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    marginBottom: 24,
  },
  backButton: {
    position: 'absolute',
    left: 0,
    zIndex: 2,
    minWidth: 84,
    minHeight: 44,
    flexDirection: 'row',
    alignItems: 'center',
    gap: 2,
    borderRadius: 22,
    paddingRight: 10,
  },
  backArrow: {
    color: accessTheme.colors.ink,
    fontSize: 30,
    fontWeight: '400',
    lineHeight: 32,
  },
  backLabel: {
    color: accessTheme.colors.textSecondary,
    fontSize: 13,
    fontWeight: '700',
  },
  topBarSpacer: {
    position: 'absolute',
    right: 0,
    width: 84,
  },
  heading: {
    marginBottom: 22,
  },
  title: {
    color: accessTheme.colors.ink,
    fontSize: 29,
    fontWeight: '700',
    letterSpacing: -0.85,
    lineHeight: 35,
  },
  body: {
    marginTop: accessTheme.spacing.sm,
    color: accessTheme.colors.textSecondary,
    fontSize: 15,
    lineHeight: 22,
  },
  formStack: {
    gap: accessTheme.spacing.md,
  },
  existingRow: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    alignItems: 'center',
    justifyContent: 'center',
    gap: 5,
    marginTop: 24,
  },
  secondaryCopy: {
    color: accessTheme.colors.textMuted,
    fontSize: 13,
  },
  inlineAction: {
    color: accessTheme.colors.accentText,
    fontSize: 13,
    fontWeight: '700',
  },
  inlinePressed: {
    opacity: 0.6,
  },
  actionDisabled: {
    opacity: 0.42,
  },
  summaryCard: {
    minHeight: 66,
    flexDirection: 'row',
    alignItems: 'center',
    gap: 14,
    borderWidth: 1,
    borderColor: accessTheme.colors.divider,
    borderRadius: accessTheme.radii.control,
    backgroundColor: accessTheme.colors.surface,
    paddingHorizontal: 16,
    paddingVertical: 10,
  },
  summaryText: {
    minWidth: 0,
    flex: 1,
    gap: 3,
  },
  summaryLabel: {
    color: accessTheme.colors.textMuted,
    fontSize: 11,
    fontWeight: '700',
    letterSpacing: 0.35,
    textTransform: 'uppercase',
  },
  summaryValue: {
    color: accessTheme.colors.ink,
    fontSize: 14,
    fontWeight: '700',
  },
  passwordGuide: {
    overflow: 'hidden',
    flexDirection: 'row',
    borderRadius: accessTheme.radii.input,
    backgroundColor: accessTheme.colors.surfaceMuted,
  },
  guideAccent: {
    width: 4,
    backgroundColor: accessTheme.colors.accent,
  },
  guideCopy: {
    flex: 1,
    gap: 7,
    paddingHorizontal: 14,
    paddingVertical: 12,
  },
  guideHeading: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    gap: 12,
  },
  guideTitle: {
    color: accessTheme.colors.ink,
    fontSize: 12,
    fontWeight: '700',
  },
  guideProposal: {
    color: accessTheme.colors.accentText,
    fontSize: 12,
    fontWeight: '800',
  },
  guideBody: {
    color: accessTheme.colors.textSecondary,
    fontSize: 12,
    lineHeight: 18,
  },
  verifyContext: {
    gap: 4,
    paddingHorizontal: 2,
  },
  verifyContextLabel: {
    color: accessTheme.colors.textMuted,
    fontSize: 11,
    fontWeight: '700',
    letterSpacing: 0.35,
    textTransform: 'uppercase',
  },
  verifyContextValue: {
    color: accessTheme.colors.ink,
    fontSize: 14,
    fontWeight: '700',
  },
  secondaryActions: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    gap: 16,
  },
  secondaryAction: {
    minHeight: 44,
    justifyContent: 'center',
  },
  securityNote: {
    color: accessTheme.colors.textMuted,
    fontSize: 12,
    lineHeight: 18,
    textAlign: 'center',
  },
});
