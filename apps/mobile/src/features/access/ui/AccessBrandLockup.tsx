import { Image, StyleSheet, View } from 'react-native';

import danteSymbolSource from '../../../../assets/brand/dante-symbol.png';
import { accessTheme } from '../theme/accessTheme';

export { danteSymbolSource };

export function AccessBrandLockup() {
  return (
    <View
      accessible
      accessibilityRole="image"
      accessibilityLabel="DANTE"
      style={styles.lockup}
    >
      <View style={styles.halo} />
      <Image
        source={danteSymbolSource}
        style={styles.symbol}
        resizeMode="contain"
      />
    </View>
  );
}

const styles = StyleSheet.create({
  lockup: {
    width: 72,
    height: 72,
    alignItems: 'center',
    justifyContent: 'center',
  },
  halo: {
    position: 'absolute',
    width: 72,
    height: 72,
    borderRadius: 36,
    backgroundColor: accessTheme.colors.surfaceMuted,
  },
  symbol: {
    width: 54,
    height: 54,
  },
});
