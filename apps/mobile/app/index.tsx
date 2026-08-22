import { radii } from '@dante/design-tokens/native';
import { StatusBar } from 'expo-status-bar';
import { useTranslation } from 'react-i18next';
import { StyleSheet, Text, View } from 'react-native';
import { Gesture, GestureDetector } from 'react-native-gesture-handler';
import Animated, {
  useAnimatedStyle,
  useSharedValue,
  withTiming,
} from 'react-native-reanimated';
import { SafeAreaView } from 'react-native-safe-area-context';

export default function MobileRuntimeReady() {
  const { t } = useTranslation('common');
  const pressed = useSharedValue(0);

  const tapGesture = Gesture.Tap()
    .onBegin(() => {
      pressed.value = withTiming(1, { duration: 80 });
    })
    .onFinalize(() => {
      pressed.value = withTiming(0, { duration: 120 });
    });

  const animatedStyle = useAnimatedStyle(() => ({
    opacity: 1 - pressed.value * 0.08,
    transform: [{ scale: 1 - pressed.value * 0.04 }],
  }));

  return (
    <SafeAreaView style={styles.safeArea}>
      <StatusBar style="light" />
      <View style={styles.screen}>
        <View style={styles.card}>
          <Text style={styles.eyebrow}>
            {t(($) => $.common.runtime.mobile.eyebrow)}
          </Text>
          <Text style={styles.title}>
            {t(($) => $.common.runtime.mobile.title)}
          </Text>
          <Text style={styles.copy}>
            {t(($) => $.common.runtime.mobile.description)}
          </Text>

          <View style={styles.statusGrid}>
            <View style={styles.statusItem}>
              <Text style={styles.statusLabel}>
                {t(($) => $.common.runtime.labels.route)}
              </Text>
              <Text style={styles.statusValue}>/</Text>
            </View>
            <View style={styles.statusItem}>
              <Text style={styles.statusLabel}>
                {t(($) => $.common.runtime.labels.purpose)}
              </Text>
              <Text style={styles.statusValue}>
                {t(($) => $.common.runtime.mobile.purpose)}
              </Text>
            </View>
          </View>

          <GestureDetector gesture={tapGesture}>
            <Animated.View style={[styles.gestureProbe, animatedStyle]}>
              <Text style={styles.gestureProbeTitle}>
                {t(($) => $.common.gesture.title)}
              </Text>
              <Text style={styles.gestureProbeCopy}>
                {t(($) => $.common.gesture.description)}
              </Text>
            </Animated.View>
          </GestureDetector>
        </View>
      </View>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  safeArea: {
    flex: 1,
    backgroundColor: '#111827',
  },
  screen: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
    padding: 24,
  },
  card: {
    width: '100%',
    maxWidth: 620,
    borderWidth: 1,
    borderColor: '#374151',
    borderRadius: radii.card,
    backgroundColor: '#1f2937',
    padding: 28,
  },
  eyebrow: {
    marginBottom: 12,
    color: '#d1d5db',
    fontSize: 12,
    fontWeight: '700',
    letterSpacing: 1.4,
  },
  title: {
    color: '#f9fafb',
    fontSize: 42,
    fontWeight: '500',
    lineHeight: 46,
  },
  copy: {
    marginTop: 18,
    color: '#d1d5db',
    fontSize: 16,
    lineHeight: 24,
  },
  statusGrid: {
    flexDirection: 'row',
    gap: 12,
    marginTop: 28,
  },
  statusItem: {
    flex: 1,
    minHeight: 84,
    borderRadius: radii.panel,
    backgroundColor: '#111827',
    padding: 16,
  },
  statusLabel: {
    color: '#9ca3af',
    fontSize: 11,
    fontWeight: '700',
    letterSpacing: 1,
    textTransform: 'uppercase',
  },
  statusValue: {
    marginTop: 8,
    color: '#f3f4f6',
    fontSize: 15,
    fontWeight: '600',
  },
  gestureProbe: {
    marginTop: 16,
    borderWidth: 1,
    borderColor: '#4b5563',
    borderRadius: radii.panel,
    backgroundColor: '#273449',
    padding: 16,
  },
  gestureProbeTitle: {
    color: '#f9fafb',
    fontSize: 15,
    fontWeight: '700',
  },
  gestureProbeCopy: {
    marginTop: 6,
    color: '#d1d5db',
    fontSize: 14,
    lineHeight: 20,
  },
});
