import { Image, StyleSheet, Text, View } from 'react-native';
import { useTranslation } from 'react-i18next';

import { accessTheme } from '../theme/accessTheme';
import { AccessButton } from './AccessButton';
import { danteSymbolSource } from './AccessBrandLockup';
import { AccessScreen } from './AccessScreen';

type WelcomeScreenProps = Readonly<{
  onContinue: () => void;
}>;

export function WelcomeScreen({ onContinue }: WelcomeScreenProps) {
  const { t } = useTranslation('common');

  return (
    <AccessScreen>
      <View style={styles.hero}>
        <View style={styles.markWrap} accessibilityElementsHidden importantForAccessibility="no-hide-descendants">
          <View style={styles.markHalo} />
          <Image source={danteSymbolSource} style={styles.mark} resizeMode="contain" />
        </View>

        <Text style={styles.kicker}>DANTE</Text>
        <Text style={styles.title} accessibilityRole="header">
          {t(($) => $.common.access.stage.titleFirst)}{'\n'}
          {t(($) => $.common.access.stage.titleSecond)}
        </Text>
        <Text style={styles.body}>{t(($) => $.common.access.stage.body)}</Text>

        <View style={styles.action}>
          <AccessButton
            label={t(($) => $.common.access.action.continue)}
            onPress={onContinue}
          />
        </View>

        <View style={styles.footRow}>
          <View style={styles.footDot} />
          <Text style={styles.foot}>{t(($) => $.common.access.stage.foot)}</Text>
        </View>
      </View>
    </AccessScreen>
  );
}

const styles = StyleSheet.create({
  hero: {
    width: '100%',
    maxWidth: 560,
    alignSelf: 'center',
  },
  markWrap: {
    width: 112,
    height: 112,
    alignItems: 'center',
    justifyContent: 'center',
    marginBottom: accessTheme.spacing.xl,
  },
  markHalo: {
    position: 'absolute',
    width: 104,
    height: 104,
    borderRadius: 52,
    backgroundColor: accessTheme.colors.surfaceMuted,
  },
  mark: {
    width: 78,
    height: 78,
  },
  kicker: {
    marginBottom: accessTheme.spacing.md,
    color: accessTheme.colors.accentText,
    fontSize: 12,
    fontWeight: '800',
    letterSpacing: 1.6,
  },
  title: {
    color: accessTheme.colors.ink,
    fontSize: 42,
    fontWeight: '700',
    letterSpacing: -1.7,
    lineHeight: 45,
  },
  body: {
    maxWidth: 500,
    marginTop: accessTheme.spacing.lg,
    color: accessTheme.colors.textSecondary,
    fontSize: 17,
    lineHeight: 27,
  },
  action: {
    marginTop: 36,
  },
  footRow: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 9,
    marginTop: accessTheme.spacing.xl,
  },
  footDot: {
    width: 6,
    height: 6,
    borderRadius: 3,
    backgroundColor: accessTheme.colors.accent,
  },
  foot: {
    flex: 1,
    color: accessTheme.colors.textMuted,
    fontSize: 12,
    lineHeight: 18,
  },
});
