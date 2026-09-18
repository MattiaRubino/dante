import { useRef, useState } from 'react';
import {
  Keyboard,
  Platform,
  Pressable,
  StyleSheet,
  Text,
  TextInput,
  View,
} from 'react-native';
import { useTranslation } from 'react-i18next';

import {
  EMPTY_SIGN_IN_FORM_ERRORS,
  hasSignInFormErrors,
  normalizeSignInEmail,
  validateSignInEmail,
  validateSignInForm,
  validateSignInPassword,
  type SignInFormErrors,
} from '../model/signInForm';
import { accessTheme } from '../theme/accessTheme';
import { AccessBrandLockup } from './AccessBrandLockup';
import { AccessButton } from './AccessButton';
import { AccessProviderButton } from './AccessProviderButton';
import { AccessScreen } from './AccessScreen';
import { AccessTextField } from './AccessTextField';

type SignInScreenProps = Readonly<{
  onSubmit?: (email: string, password: string) => void | Promise<void>;
  onGooglePress?: () => void;
  onApplePress?: () => void;
  onForgotPassword?: () => void;
  onCreateAccount?: () => void;
}>;

type TouchedState = Readonly<{
  email: boolean;
  password: boolean;
}>;

const EMPTY_TOUCHED: TouchedState = {
  email: false,
  password: false,
};

export function SignInScreen({
  onSubmit,
  onGooglePress,
  onApplePress,
  onForgotPassword,
  onCreateAccount,
}: SignInScreenProps) {
  const { t } = useTranslation('common');
  const passwordInputRef = useRef<TextInput>(null);
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [errors, setErrors] = useState<SignInFormErrors>(
    EMPTY_SIGN_IN_FORM_ERRORS,
  );
  const [touched, setTouched] = useState<TouchedState>(EMPTY_TOUCHED);
  const [submitting, setSubmitting] = useState(false);

  const emailErrorMessage =
    errors.email === 'email'
      ? t(($) => $.common.access.validation.email)
      : undefined;
  const passwordErrorMessage =
    errors.password === 'passwordRequired'
      ? t(($) => $.common.access.validation.passwordRequired)
      : undefined;

  function handleEmailChange(value: string) {
    setEmail(value);
    if (touched.email) {
      setErrors((current) => ({
        ...current,
        email: validateSignInEmail(value),
      }));
    }
  }

  function handleEmailBlur() {
    const normalized = normalizeSignInEmail(email);
    setEmail(normalized);
    setTouched((current) => ({ ...current, email: true }));
    setErrors((current) => ({
      ...current,
      email: validateSignInEmail(normalized),
    }));
  }

  function handlePasswordChange(value: string) {
    setPassword(value);
    if (touched.password) {
      setErrors((current) => ({
        ...current,
        password: validateSignInPassword(value),
      }));
    }
  }

  function handlePasswordBlur() {
    setTouched((current) => ({ ...current, password: true }));
    setErrors((current) => ({
      ...current,
      password: validateSignInPassword(password),
    }));
  }

  async function handleSubmit() {
    if (submitting) {
      return;
    }

    const normalizedEmail = normalizeSignInEmail(email);
    const nextErrors = validateSignInForm(normalizedEmail, password);

    setEmail(normalizedEmail);
    setTouched({ email: true, password: true });
    setErrors(nextErrors);

    if (hasSignInFormErrors(nextErrors)) {
      return;
    }

    Keyboard.dismiss();

    if (onSubmit === undefined) {
      return;
    }

    setSubmitting(true);
    try {
      await onSubmit(normalizedEmail, password);
    } finally {
      setSubmitting(false);
    }
  }

  function triggerSubmit() {
    void handleSubmit();
  }

  const googlePress = submitting ? undefined : onGooglePress;
  const applePress = submitting ? undefined : onApplePress;
  const forgotPasswordPress = submitting ? undefined : onForgotPassword;
  const createAccountPress = submitting ? undefined : onCreateAccount;

  return (
    <AccessScreen>
      <View style={styles.frame}>
        <View style={styles.brandRow}>
          <AccessBrandLockup />
        </View>

        <View style={styles.heading}>
          <Text style={styles.title} accessibilityRole="header">
            {t(($) => $.common.access.signin.title)}
          </Text>
          <Text style={styles.body}>
            {t(($) => $.common.access.signin.body)}
          </Text>
        </View>

        <View style={styles.providerStack}>
          <AccessProviderButton
            provider="google"
            label={t(($) => $.common.access.provider.google)}
            {...(googlePress === undefined ? {} : { onPress: googlePress })}
          />
          {Platform.OS === 'ios' ? (
            <AccessProviderButton
              provider="apple"
              label={t(($) => $.common.access.provider.apple)}
              {...(applePress === undefined ? {} : { onPress: applePress })}
            />
          ) : null}
        </View>

        <View style={styles.divider} accessibilityElementsHidden>
          <View style={styles.dividerLine} />
          <Text style={styles.dividerLabel}>
            {t(($) => $.common.access.common.or)}
          </Text>
          <View style={styles.dividerLine} />
        </View>

        <View style={styles.fields}>
          <AccessTextField
            label={t(($) => $.common.access.field.email)}
            value={email}
            onChangeText={handleEmailChange}
            onBlur={handleEmailBlur}
            onSubmitEditing={() => passwordInputRef.current?.focus()}
            placeholder={t(($) => $.common.access.field.emailPlaceholder)}
            autoComplete="email"
            keyboardType="email-address"
            textContentType="emailAddress"
            returnKeyType="next"
            editable={!submitting}
            {...(emailErrorMessage === undefined
              ? {}
              : { error: emailErrorMessage })}
          />
          <AccessTextField
            label={t(($) => $.common.access.field.password)}
            value={password}
            onChangeText={handlePasswordChange}
            onBlur={handlePasswordBlur}
            onSubmitEditing={triggerSubmit}
            inputRef={passwordInputRef}
            secure
            showLabel={t(($) => $.common.access.action.showPassword)}
            hideLabel={t(($) => $.common.access.action.hidePassword)}
            autoComplete="current-password"
            textContentType="password"
            returnKeyType="done"
            editable={!submitting}
            {...(passwordErrorMessage === undefined
              ? {}
              : { error: passwordErrorMessage })}
          />
        </View>

        <Pressable
          accessibilityRole="button"
          accessibilityState={{ disabled: forgotPasswordPress === undefined }}
          disabled={forgotPasswordPress === undefined}
          {...(forgotPasswordPress === undefined
            ? {}
            : { onPress: forgotPasswordPress })}
          style={({ pressed }) => [
            styles.forgot,
            pressed ? styles.inlinePressed : null,
          ]}
        >
          <Text style={styles.inlineAction}>
            {t(($) => $.common.access.signin.forgot)}
          </Text>
        </Pressable>

        <View style={styles.primaryAction}>
          <AccessButton
            label={t(($) => $.common.access.action.signin)}
            onPress={triggerSubmit}
            loading={submitting}
          />
        </View>

        <View style={styles.signupRow}>
          <Text style={styles.signupCopy}>
            {t(($) => $.common.access.signin.new)}
          </Text>
          <Pressable
            accessibilityRole="button"
            accessibilityState={{ disabled: createAccountPress === undefined }}
            disabled={createAccountPress === undefined}
            {...(createAccountPress === undefined
              ? {}
              : { onPress: createAccountPress })}
            style={({ pressed }) => [
              styles.signupActionWrap,
              pressed ? styles.inlinePressed : null,
            ]}
          >
            <Text style={styles.signupAction}>
              {t(($) => $.common.access.action.createAccount)}
            </Text>
          </Pressable>
        </View>

        <Text style={styles.legal}>
          {t(($) => $.common.access.legal.prefix)}{' '}
          <Text style={styles.legalLink}>
            {t(($) => $.common.access.legal.terms)}
          </Text>{' '}
          ·{' '}
          <Text style={styles.legalLink}>
            {t(($) => $.common.access.legal.privacy)}
          </Text>
        </Text>
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
  brandRow: {
    alignItems: 'center',
    marginBottom: 28,
  },
  heading: {
    marginBottom: 26,
  },
  title: {
    color: accessTheme.colors.ink,
    fontSize: 30,
    fontWeight: '700',
    letterSpacing: -0.9,
    lineHeight: 36,
  },
  body: {
    marginTop: accessTheme.spacing.sm,
    color: accessTheme.colors.textSecondary,
    fontSize: 15,
    lineHeight: 22,
  },
  providerStack: {
    gap: 12,
  },
  divider: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 12,
    marginVertical: 24,
  },
  dividerLine: {
    flex: 1,
    height: StyleSheet.hairlineWidth,
    backgroundColor: accessTheme.colors.divider,
  },
  dividerLabel: {
    color: accessTheme.colors.textMuted,
    fontSize: 12,
    fontWeight: '600',
  },
  fields: {
    gap: accessTheme.spacing.md,
  },
  forgot: {
    minHeight: 40,
    alignSelf: 'flex-end',
    justifyContent: 'center',
    marginTop: 2,
    paddingHorizontal: 2,
  },
  inlineAction: {
    color: accessTheme.colors.accentText,
    fontSize: 13,
    fontWeight: '700',
  },
  inlinePressed: {
    opacity: 0.6,
  },
  primaryAction: {
    marginTop: 10,
  },
  signupRow: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    alignItems: 'center',
    justifyContent: 'center',
    gap: 5,
    marginTop: 22,
  },
  signupCopy: {
    color: accessTheme.colors.textMuted,
    fontSize: 13,
  },
  signupActionWrap: {
    minHeight: 36,
    justifyContent: 'center',
  },
  signupAction: {
    color: accessTheme.colors.accentText,
    fontSize: 13,
    fontWeight: '700',
  },
  legal: {
    marginTop: 30,
    color: accessTheme.colors.textMuted,
    fontSize: 11,
    lineHeight: 17,
    textAlign: 'center',
  },
  legalLink: {
    color: accessTheme.colors.textSecondary,
    textDecorationLine: 'underline',
  },
});
