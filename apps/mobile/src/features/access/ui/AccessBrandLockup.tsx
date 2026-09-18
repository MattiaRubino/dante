import { Image, StyleSheet, View } from 'react-native';

import danteSymbolSource from '../../../../assets/brand/dante-symbol.png';
import danteWordmarkSource from '../../../../assets/brand/dante-wordmark.png';
import { accessTheme } from '../theme/accessTheme';

export { danteSymbolSource };

export function AccessBrandLockup() {
  return (
    <View style={styles.lockup} accessibilityRole="header">
      <Image
        source={danteSymbolSource}
        style={styles.symbol}
        resizeMode="contain"
      />
      <Image
        source={danteWordmarkSource}
        style={styles.wordmark}
        resizeMode="contain"
      />
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
