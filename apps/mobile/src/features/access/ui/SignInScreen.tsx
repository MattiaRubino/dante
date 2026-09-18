import { useState } from 'react';
import { StyleSheet, Text, View } from 'react-native';
import { useTranslation } from 'react-i18next';

import { accessTheme } from '../theme/accessTheme';
import { AccessButton } from './AccessButton';
import { AccessScreen } from './AccessScreen';
import { AccessTextField } from './AccessTextField';

type SignInScreenProps = Readonly<{
  onBack: () => void;
  onSubmit?: (email: string, password: string) => void;
}>;

export function SignInScreen({ onBack, onSubmit }: SignInScreenProps) {
  const { t } = useTranslation('common');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  return (
    <AccessScreen compact>
      <View style={styles.frame}>
        <View style={styles.panel}>
          <Text style={styles.kicker}>{t(($) => $.common.access.kicker.access)}</Text>
          <Text style={styles.title} accessibilityRole="header">
            {t(($) => $.common.access.signin.title)}
          </Text>
          <Text style={styles.body}>{t(($) => $.common.access.signin.body)}</Text>

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

          <View style={styles.actions}>
            <AccessButton
              label={t(($) => $.common.access.action.signin)}
              onPress={
                onSubmit === undefined
                  ? undefined
                  : () => onSubmit(email.trim(), password)
              }
            />
            <AccessButton
              label={t(($) => $.common.access.action.back)}
              variant="text"
              onPress={onBack}
            />
          </View>

          <Text style={styles.legal}>
            {t(($) => $.common.access.legal.prefix)}{' '}
            {t(($) => $.common.access.legal.terms)} · {t(($) => $.common.access.legal.privacy)}
          </Text>
        </View>
      </View>
    </AccessScreen>
  );
}

const styles = StyleSheet.create({
  frame: {
    width: '100%',
    maxWidth: 520,
    alignSelf: 'center',
    paddingTop: accessTheme.spacing.lg,
  },
  panel: {
    width: '100%',
    borderWidth: 1,
    borderColor: accessTheme.colors.divider,
    borderRadius: accessTheme.radii.card,
    backgroundColor: accessTheme.colors.surface,
    paddingHorizontal: accessTheme.spacing.lg,
    paddingTop: accessTheme.spacing.xl,
    paddingBottom: accessTheme.spacing.lg,
    shadowColor: accessTheme.colors.ink,
    shadowOffset: { width: 0, height: 14 },
    shadowOpacity: 0.08,
    shadowRadius: 28,
    elevation: 3,
  },
  kicker: {
    marginBottom: accessTheme.spacing.md,
    color: accessTheme.colors.textMuted,
    fontSize: 11,
    fontWeight: '800',
    letterSpacing: 1.5,
    textTransform: 'uppercase',
  },
  title: {
    color: accessTheme.colors.ink,
    fontSize: 31,
    fontWeight: '700',
    letterSpacing: -1,
    lineHeight: 36,
  },
  body: {
    marginTop: accessTheme.spacing.sm,
    color: accessTheme.colors.textMuted,
    fontSize: 14,
    lineHeight: 22,
  },
  fields: {
    gap: accessTheme.spacing.md,
    marginTop: 28,
  },
  actions: {
    gap: accessTheme.spacing.sm,
    marginTop: accessTheme.spacing.lg,
  },
  legal: {
    marginTop: accessTheme.spacing.lg,
    color: accessTheme.colors.textMuted,
    fontSize: 11,
    lineHeight: 17,
    textAlign: 'center',
  },
});
