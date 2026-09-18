import { Platform, Pressable, StyleSheet, Text, View } from 'react-native';
import { useState } from 'react';
import { useTranslation } from 'react-i18next';

import { accessTheme } from '../theme/accessTheme';
import { AccessBrandLockup } from './AccessBrandLockup';
import { AccessButton } from './AccessButton';
import { AccessProviderButton } from './AccessProviderButton';
import { AccessScreen } from './AccessScreen';
import { AccessTextField } from './AccessTextField';

type SignInScreenProps = Readonly<{
  onSubmit?: (email: string, password: string) => void;
  onGooglePress?: () => void;
  onApplePress?: () => void;
  onForgotPassword?: () => void;
  onCreateAccount?: () => void;
}>;

export function SignInScreen({
  onSubmit,
  onGooglePress,
  onApplePress,
  onForgotPassword,
  onCreateAccount,
}: SignInScreenProps) {
  const { t } = useTranslation('common');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

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
            {...(onGooglePress === undefined ? {} : { onPress: onGooglePress })}
          />
          {Platform.OS === 'ios' ? (
            <AccessProviderButton
              provider="apple"
              label={t(($) => $.common.access.provider.apple)}
              {...(onApplePress === undefined ? {} : { onPress: onApplePress })}
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
            onChangeText={setEmail}
            placeholder={t(($) => $.common.access.field.emailPlaceholder)}
            autoComplete="email"
            keyboardType="email-address"
            textContentType="emailAddress"
          />
          <AccessTextField
            label={t(($) => $.common.access.field.password)}
            value={password}
            onChangeText={setPassword}
            secure
            showLabel={t(($) => $.common.access.action.showPassword)}
            hideLabel={t(($) => $.common.access.action.hidePassword)}
            autoComplete="current-password"
            textContentType="password"
          />
        </View>

        <Pressable
          accessibilityRole="button"
          accessibilityState={{ disabled: onForgotPassword === undefined }}
          disabled={onForgotPassword === undefined}
          {...(onForgotPassword === undefined
            ? {}
            : { onPress: onForgotPassword })}
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
            {...(onSubmit === undefined
              ? {}
              : { onPress: () => onSubmit(email.trim(), password) })}
          />
        </View>

        <View style={styles.signupRow}>
          <Text style={styles.signupCopy}>
            {t(($) => $.common.access.signin.new)}
          </Text>
          <Pressable
            accessibilityRole="button"
            accessibilityState={{ disabled: onCreateAccount === undefined }}
            disabled={onCreateAccount === undefined}
            {...(onCreateAccount === undefined
              ? {}
              : { onPress: onCreateAccount })}
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
    fontWeight: '750',
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
