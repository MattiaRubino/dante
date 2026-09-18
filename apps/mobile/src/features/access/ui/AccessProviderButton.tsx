import { Pressable, StyleSheet, Text, View } from 'react-native';

import { accessTheme } from '../theme/accessTheme';

type AccessProvider = 'google' | 'apple';

type AccessProviderButtonProps = Readonly<{
  provider: AccessProvider;
  label: string;
  onPress?: () => void;
  disabled?: boolean;
}>;

export function AccessProviderButton({
  provider,
  label,
  onPress,
  disabled = false,
}: AccessProviderButtonProps) {
  const isUnavailable = disabled || onPress === undefined;
  const mark = provider === 'google' ? 'G' : '';

  return (
    <Pressable
      accessibilityRole="button"
      accessibilityState={{ disabled: isUnavailable }}
      disabled={isUnavailable}
      onPress={onPress}
      style={({ pressed }) => [
        styles.button,
        pressed && !isUnavailable ? styles.pressed : null,
        disabled ? styles.disabled : null,
      ]}
    >
      <View style={styles.markSlot}>
        <Text
          style={[
            styles.mark,
            provider === 'google' ? styles.googleMark : styles.appleMark,
          ]}
        >
          {mark}
        </Text>
      </View>
      <Text style={styles.label}>{label}</Text>
      <View style={styles.markSlot} />
    </Pressable>
  );
}

const styles = StyleSheet.create({
  button: {
    width: '100%',
    minHeight: 54,
    flexDirection: 'row',
    alignItems: 'center',
    borderWidth: 1,
    borderColor: accessTheme.colors.divider,
    borderRadius: accessTheme.radii.control,
    backgroundColor: accessTheme.colors.surface,
    paddingHorizontal: accessTheme.spacing.md,
    shadowColor: accessTheme.colors.ink,
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.04,
    shadowRadius: 8,
    elevation: 1,
  },
  pressed: {
    backgroundColor: accessTheme.colors.surfaceMuted,
    transform: [{ scale: 0.997 }],
  },
  disabled: {
    opacity: 0.5,
  },
  markSlot: {
    width: 30,
    alignItems: 'center',
    justifyContent: 'center',
  },
  mark: {
    fontSize: 20,
    fontWeight: '800',
    lineHeight: 24,
  },
  googleMark: {
    color: '#4285f4',
  },
  appleMark: {
    color: accessTheme.colors.ink,
  },
  label: {
    flex: 1,
    color: accessTheme.colors.ink,
    fontSize: 15,
    fontWeight: '700',
    textAlign: 'center',
  },
});
