import type { PropsWithChildren } from 'react';
import { useMemo } from 'react';
import { useRouter } from 'expo-router';
import { PanResponder, StyleSheet, View } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';

import { AppBottomBar, type AppShellDestination } from './AppBottomBar';
import { AppTopBar } from './AppTopBar';

const PRIMARY_DESTINATIONS = ['home', 'timeline', 'worlds'] as const;
const PRIMARY_PATHS = ['/home', '/timeline', '/worlds'] as const;

type PrimaryDestination = (typeof PRIMARY_DESTINATIONS)[number];

type PrimaryScreenFrameProps = PropsWithChildren<{
  active: AppShellDestination;
  title: string;
}>;

function isPrimaryDestination(
  destination: AppShellDestination,
): destination is PrimaryDestination {
  return PRIMARY_DESTINATIONS.includes(destination as PrimaryDestination);
}

export function PrimaryScreenFrame({
  active,
  children,
  title,
}: PrimaryScreenFrameProps) {
  const router = useRouter();

  const panResponder = useMemo(
    () =>
      PanResponder.create({
        onMoveShouldSetPanResponder: (_, gestureState) => {
          if (!isPrimaryDestination(active)) {
            return false;
          }

          const horizontal = Math.abs(gestureState.dx);
          const vertical = Math.abs(gestureState.dy);

          return horizontal > 18 && horizontal > vertical * 1.2;
        },
        onPanResponderRelease: (_, gestureState) => {
          if (!isPrimaryDestination(active)) {
            return;
          }

          const currentIndex = PRIMARY_DESTINATIONS.indexOf(active);
          const passedDistance = Math.abs(gestureState.dx) >= 72;
          const passedVelocity = Math.abs(gestureState.vx) >= 0.15;

          if (!passedDistance && !passedVelocity) {
            return;
          }

          const direction = gestureState.dx < 0 ? 1 : -1;
          const targetIndex = currentIndex + direction;

          if (targetIndex < 0 || targetIndex >= PRIMARY_PATHS.length) {
            return;
          }

          router.replace(PRIMARY_PATHS[targetIndex]);
        },
      }),
    [active, router],
  );

  return (
    <SafeAreaView edges={['top', 'bottom']} style={styles.safeArea}>
      <AppTopBar title={title} />
      <View style={styles.content} {...panResponder.panHandlers}>
        {children}
      </View>
      <AppBottomBar active={active} />
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  safeArea: {
    flex: 1,
    backgroundColor: '#0b1020',
  },
  content: {
    flex: 1,
    justifyContent: 'center',
    paddingHorizontal: 20,
    paddingVertical: 24,
  },
});
