import { Image, StyleSheet, View } from 'react-native';

import { accessTheme } from '../theme/accessTheme';

export const danteSymbolSource = require('../../../../../../assets/brand/logo/qa/dante-symbol-master-v0-production-qa.png') as number;
const danteWordmarkSource = require('../../../../../../assets/brand/wordmark/qa/dante-wordmark-master-v0-production-qa.png') as number;

export function AccessBrandLockup() {
  return (
    <View style={styles.lockup} accessibilityRole="header">
      <Image source={danteSymbolSource} style={styles.symbol} resizeMode="contain" />
      <Image source={danteWordmarkSource} style={styles.wordmark} resizeMode="contain" />
    </View>
  );
}

const styles = StyleSheet.create({
  lockup: {
    minHeight: 44,
    flexDirection: 'row',
    alignItems: 'center',
    gap: accessTheme.spacing.sm,
  },
  symbol: {
    width: 38,
    height: 38,
  },
  wordmark: {
    width: 118,
    height: 34,
  },
});
