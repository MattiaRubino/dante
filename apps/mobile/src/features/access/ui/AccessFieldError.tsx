import { StyleSheet, Text, View } from 'react-native';

import { accessTheme } from '../theme/accessTheme';

type AccessFieldErrorProps = Readonly<{
  message: string;
}>;

export function AccessFieldError({ message }: AccessFieldErrorProps) {
  return (
    <View
      accessibilityLiveRegion="polite"
      style={styles.row}
    >
      <View style={styles.badge} accessibilityElementsHidden>
        <Text style={styles.badgeText}>!</Text>
      </View>
      <Text style={styles.message}>{message}</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  row: {
    minHeight: 20,
    flexDirection: 'row',
    alignItems: 'flex-start',
    gap: 7,
    paddingTop: 1,
  },
  badge: {
    width: 16,
    height: 16,
    alignItems: 'center',
    justifyContent: 'center',
    borderWidth: 1,
    borderColor: accessTheme.colors.accentText,
    borderRadius: 8,
  },
  badgeText: {
    color: accessTheme.colors.accentText,
    fontSize: 10,
    fontWeight: '800',
    lineHeight: 12,
  },
  message: {
    flex: 1,
    color: accessTheme.colors.accentText,
    fontSize: 12,
    fontWeight: '600',
    lineHeight: 17,
  },
});
