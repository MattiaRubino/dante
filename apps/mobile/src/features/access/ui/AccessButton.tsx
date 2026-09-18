import { ActivityIndicator, Pressable, StyleSheet, Text } from 'react-native';

import { accessTheme } from '../theme/accessTheme';

type AccessButtonVariant = 'primary' | 'secondary' | 'text';

type AccessButtonProps = Readonly<{
  label: string;
  onPress?: () => void;
  variant?: AccessButtonVariant;
  disabled?: boolean;
  loading?: boolean;
}>;

function labelStyleFor(variant: AccessButtonVariant) {
  switch (variant) {
    case 'primary':
      return styles.primaryLabel;
    case 'secondary':
      return styles.secondaryLabel;
    case 'text':
      return styles.textLabel;
  }
}

export function AccessButton({
  label,
  onPress,
  variant = 'primary',
  disabled = false,
  loading = false,
}: AccessButtonProps) {
  const inactive = disabled || loading || onPress === undefined;

  return (
    <Pressable
      accessibilityRole="button"
      accessibilityState={{ disabled: inactive, busy: loading }}
      disabled={inactive}
      onPress={onPress}
      style={({ pressed }) => [
        styles.base,
        styles[variant],
        pressed && !inactive ? styles.pressed : null,
        inactive ? styles.disabled : null,
      ]}
    >
      {loading ? (
        <ActivityIndicator
          size="small"
          color={variant === 'primary' ? accessTheme.colors.onInk : accessTheme.colors.ink}
        />
      ) : (
        <Text style={[styles.label, labelStyleFor(variant)]}>{label}</Text>
      )}
    </Pressable>
  );
}

const styles = StyleSheet.create({
  base: {
    minHeight: 52,
    alignItems: 'center',
    justifyContent: 'center',
    borderRadius: accessTheme.radii.control,
    paddingHorizontal: accessTheme.spacing.lg,
  },
  primary: {
    backgroundColor: accessTheme.colors.ink,
  },
  secondary: {
    borderWidth: 1,
    borderColor: accessTheme.colors.border,
    backgroundColor: accessTheme.colors.surface,
  },
  text: {
    minHeight: 44,
    backgroundColor: 'transparent',
  },
  pressed: {
    opacity: 0.82,
    transform: [{ scale: 0.995 }],
  },
  disabled: {
    opacity: 0.42,
  },
  label: {
    fontSize: 15,
    fontWeight: '700',
    textAlign: 'center',
  },
  primaryLabel: {
    color: accessTheme.colors.onInk,
  },
  secondaryLabel: {
    color: accessTheme.colors.ink,
  },
  textLabel: {
    color: accessTheme.colors.textSecondary,
  },
});
