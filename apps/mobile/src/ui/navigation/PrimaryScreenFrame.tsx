import type { PropsWithChildren } from 'react';
import { useMemo } from 'react';
import { PanResponder, StyleSheet, View } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';

import { AppBottomBar, type AppShellDestination } from './AppBottomBar';
import { AppTopBar } from './AppTopBar';

export type { AppShellDestination } from './AppBottomBar';

const PRIMARY_DESTINATIONS = ['home', 'timeline', 'worlds'] as const;

type PrimaryDestination = (typeof PRIMARY_DESTINATIONS)[number];

type PrimaryScreenFrameProps = PropsWithChildren<{
  active: AppShellDestination;
  title: string;
  onNavigate: (destination: AppShellDestination) => void;
  onAi: () => void;
  onMore: () => void;
}>;

function isPrimaryDestination(
  destination: AppShellDestination,
): destination is PrimaryDestination {
  return PRIMARY_DESTINATIONS.includes(destination as PrimaryDestination);
}

export function PrimaryScreenFrame({
  active,
  children,
  onAi,
  onMore,
  onNavigate,
  title,
}: PrimaryScreenFrameProps) {
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

          if (targetIndex < 0 || targetIndex >= PRIMARY_DESTINATIONS.length) {
            return;
          }

          onNavigate(PRIMARY_DESTINATIONS[targetIndex]);
        },
      }),
    [active, onNavigate],
  );

  return (
    <SafeAreaView edges={['top', 'bottom']} style={styles.safeArea}>
      <AppTopBar title={title} onMore={onMore} />
      <View style={styles.content} {...panResponder.panHandlers}>
        {children}
      </View>
      <AppBottomBar active={active} onNavigate={onNavigate} onAi={onAi} />
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
    backgroundColor: '#0b1020',
  },
});
