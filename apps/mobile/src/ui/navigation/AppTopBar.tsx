import { useRouter } from 'expo-router';
import { Pressable, StyleSheet, Text, View } from 'react-native';

type AppTopBarProps = {
  title: string;
};

export function AppTopBar({ title }: AppTopBarProps) {
  const router = useRouter();

  return (
    <View style={styles.container}>
      <View style={styles.identity}>
        <Text style={styles.brand}>DANTE</Text>
        <Text style={styles.title}>{title}</Text>
      </View>

      <Pressable
        accessibilityRole="button"
        accessibilityLabel="Open more options"
        hitSlop={12}
        onPress={() => router.replace('/more')}
        style={({ pressed }) => [styles.action, pressed && styles.actionPressed]}
      >
        <Text style={styles.actionText}>•••</Text>
      </Pressable>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    minHeight: 58,
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    borderBottomWidth: StyleSheet.hairlineWidth,
    borderBottomColor: '#25304a',
    paddingHorizontal: 18,
    backgroundColor: '#0b1020',
  },
  identity: {
    flexDirection: 'row',
    alignItems: 'baseline',
    gap: 10,
  },
  brand: {
    color: '#f4f7ff',
    fontSize: 13,
    fontWeight: '800',
    letterSpacing: 1.8,
  },
  title: {
    color: '#8e9ab8',
    fontSize: 14,
    fontWeight: '600',
  },
  action: {
    minWidth: 44,
    minHeight: 44,
    alignItems: 'center',
    justifyContent: 'center',
    borderRadius: 22,
  },
  actionPressed: {
    backgroundColor: '#151d32',
  },
  actionText: {
    color: '#d8def0',
    fontSize: 18,
    fontWeight: '700',
    letterSpacing: 2,
  },
});
