import { Image, StyleSheet, View, useWindowDimensions } from 'react-native';

import danteSymbolSource from '../../../../assets/brand/dante-symbol.png';
import { accessTheme } from '../theme/accessTheme';

export function AccessBackgroundMark() {
  const { width } = useWindowDimensions();
  const size = Math.max(
    accessTheme.decorative.backgroundMarkMinSize,
    width * accessTheme.decorative.backgroundMarkScale,
  );

  return (
    <View
      pointerEvents="none"
      style={styles.layer}
      accessible={false}
      accessibilityElementsHidden
      importantForAccessibility="no-hide-descendants"
    >
      <Image
        source={danteSymbolSource}
        resizeMode="contain"
        style={[
          styles.mark,
          {
            width: size,
            height: size,
            left: -size * accessTheme.decorative.backgroundMarkLeftCrop,
            bottom: -size * accessTheme.decorative.backgroundMarkBottomCrop,
          },
        ]}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  layer: {
    position: 'absolute',
    top: 0,
    right: 0,
    bottom: 0,
    left: 0,
    overflow: 'hidden',
  },
  mark: {
    position: 'absolute',
    opacity: accessTheme.decorative.backgroundMarkOpacity,
  },
});
