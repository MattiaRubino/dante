import { StyleSheet, Text, View } from 'react-native';

import type { SignUpStep } from '../model/signUpFlow';
import { accessTheme } from '../theme/accessTheme';

type SignUpProgressProps = Readonly<{
  step: SignUpStep;
  emailLabel: string;
  passwordLabel: string;
  verifyLabel: string;
  accessibilityLabel: string;
}>;

const STEP_ORDER: readonly SignUpStep[] = ['email', 'password', 'verify'];

export function SignUpProgress({
  step,
  emailLabel,
  passwordLabel,
  verifyLabel,
  accessibilityLabel,
}: SignUpProgressProps) {
  const currentIndex = STEP_ORDER.indexOf(step);
  const labels: Record<SignUpStep, string> = {
    email: emailLabel,
    password: passwordLabel,
    verify: verifyLabel,
  };

  return (
    <View
      accessible
      accessibilityLabel={accessibilityLabel}
      style={styles.progress}
    >
      {STEP_ORDER.map((candidate, index) => {
        const active = candidate === step;
        const complete = index < currentIndex;
        const reached = index <= currentIndex;

        return (
          <View key={candidate} style={styles.step}>
            <View
              style={[
                styles.track,
                reached ? styles.trackReached : null,
                active ? styles.trackActive : null,
              ]}
            />
            <Text
              style={[
                styles.label,
                complete ? styles.labelComplete : null,
                active ? styles.labelActive : null,
              ]}
            >
              {labels[candidate]}
            </Text>
          </View>
        );
      })}
    </View>
  );
}

const styles = StyleSheet.create({
  progress: {
    flexDirection: 'row',
    gap: 8,
    marginBottom: 26,
  },
  step: {
    flex: 1,
    gap: 8,
  },
  track: {
    height: 4,
    borderRadius: 2,
    backgroundColor: accessTheme.colors.divider,
  },
  trackReached: {
    backgroundColor: 'rgba(234, 92, 18, 0.38)',
  },
  trackActive: {
    backgroundColor: accessTheme.colors.accent,
  },
  label: {
    color: accessTheme.colors.textMuted,
    fontSize: 11,
    fontWeight: '700',
    letterSpacing: 0.25,
  },
  labelComplete: {
    color: accessTheme.colors.accentText,
  },
  labelActive: {
    color: accessTheme.colors.ink,
  },
});
