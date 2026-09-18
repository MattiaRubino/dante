import { Pressable, StyleSheet, Text, View } from 'react-native';

export type AppShellDestination = 'home' | 'timeline' | 'worlds' | 'more';

type AppBottomBarProps = {
  active: AppShellDestination;
  onNavigate: (destination: AppShellDestination) => void;
  onAi: () => void;
};

type NavDestination = {
  id: AppShellDestination;
  label: string;
};

const LEFT_DESTINATIONS: readonly NavDestination[] = [
  { id: 'home', label: 'Home' },
  { id: 'timeline', label: 'Timeline' },
];

const RIGHT_DESTINATIONS: readonly NavDestination[] = [
  { id: 'worlds', label: 'Worlds' },
  { id: 'more', label: 'More' },
];

export function AppBottomBar({
  active,
  onAi,
  onNavigate,
}: AppBottomBarProps) {
  const renderDestination = (destination: NavDestination) => {
    const isActive = destination.id === active;

    return (
      <Pressable
        key={destination.id}
        accessibilityRole="tab"
        accessibilityState={{ selected: isActive }}
        onPress={() => onNavigate(destination.id)}
        style={({ pressed }) => [styles.destination, pressed && styles.pressed]}
      >
        <View style={[styles.marker, isActive && styles.markerActive]} />
        <Text style={[styles.label, isActive && styles.labelActive]}>
          {destination.label}
        </Text>
      </Pressable>
    );
  };

  return (
    <View style={styles.container}>
      <View style={styles.side}>{LEFT_DESTINATIONS.map(renderDestination)}</View>

      <Pressable
        accessibilityRole="button"
        accessibilityLabel="Open DANTE AI"
        onPress={onAi}
        style={({ pressed }) => [styles.aiButton, pressed && styles.aiButtonPressed]}
      >
        <Text style={styles.aiText}>AI</Text>
      </Pressable>

      <View style={styles.side}>{RIGHT_DESTINATIONS.map(renderDestination)}</View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    minHeight: 72,
    flexDirection: 'row',
    alignItems: 'center',
    borderTopWidth: StyleSheet.hairlineWidth,
    borderTopColor: '#25304a',
    backgroundColor: '#0b1020',
    paddingHorizontal: 8,
    paddingVertical: 8,
  },
  side: {
    flex: 1,
    flexDirection: 'row',
  },
  destination: {
    flex: 1,
    minHeight: 50,
    alignItems: 'center',
    justifyContent: 'center',
    gap: 5,
    borderRadius: 14,
  },
  pressed: {
    backgroundColor: '#151d32',
  },
  marker: {
    width: 4,
    height: 4,
    borderRadius: 2,
    backgroundColor: '#46516d',
  },
  markerActive: {
    width: 16,
    backgroundColor: '#dbe4ff',
  },
  label: {
    color: '#7f8aa7',
    fontSize: 11,
    fontWeight: '600',
  },
  labelActive: {
    color: '#f4f7ff',
  },
  aiButton: {
    width: 58,
    height: 58,
    alignItems: 'center',
    justifyContent: 'center',
    borderWidth: 1,
    borderColor: '#7588bd',
    borderRadius: 29,
    backgroundColor: '#1b2744',
    marginHorizontal: 6,
    transform: [{ translateY: -9 }],
  },
  aiButtonPressed: {
    transform: [{ translateY: -9 }, { scale: 0.96 }],
  },
  aiText: {
    color: '#f4f7ff',
    fontSize: 13,
    fontWeight: '800',
    letterSpacing: 0.8,
  },
});
