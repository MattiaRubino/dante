import { Pressable, StyleSheet, Text, View } from 'react-native';

type SectionPlaceholderProps = {
  eyebrow?: string;
  title: string;
  copy: string;
  actionLabel?: string;
  onAction?: () => void;
};

export function SectionPlaceholder({
  actionLabel,
  copy,
  eyebrow,
  onAction,
  title,
}: SectionPlaceholderProps) {
  return (
    <View style={styles.screen}>
      <View style={styles.container}>
        {eyebrow ? <Text style={styles.eyebrow}>{eyebrow}</Text> : null}
        <Text style={styles.title}>{title}</Text>
        <Text style={styles.copy}>{copy}</Text>

        {actionLabel && onAction ? (
          <Pressable
            accessibilityRole="button"
            onPress={onAction}
            style={({ pressed }) => [
              styles.action,
              pressed && styles.actionPressed,
            ]}
          >
            <Text style={styles.actionText}>{actionLabel}</Text>
          </Pressable>
        ) : null}
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  screen: {
    flex: 1,
    justifyContent: 'center',
    backgroundColor: '#0b1020',
    paddingHorizontal: 20,
    paddingVertical: 24,
  },
  container: {
    width: '100%',
    maxWidth: 620,
    alignSelf: 'center',
    borderWidth: 1,
    borderColor: '#25304a',
    borderRadius: 24,
    backgroundColor: '#11182a',
    paddingHorizontal: 24,
    paddingVertical: 28,
  },
  eyebrow: {
    marginBottom: 12,
    color: '#7481a0',
    fontSize: 11,
    fontWeight: '800',
    letterSpacing: 1.5,
  },
  title: {
    color: '#f4f7ff',
    fontSize: 34,
    fontWeight: '600',
    letterSpacing: -0.7,
  },
  copy: {
    marginTop: 14,
    color: '#aab4ce',
    fontSize: 15,
    lineHeight: 23,
  },
  action: {
    alignSelf: 'flex-start',
    minHeight: 46,
    justifyContent: 'center',
    marginTop: 24,
    borderWidth: 1,
    borderColor: '#53658f',
    borderRadius: 16,
    backgroundColor: '#1b2744',
    paddingHorizontal: 18,
  },
  actionPressed: {
    opacity: 0.82,
  },
  actionText: {
    color: '#f4f7ff',
    fontSize: 14,
    fontWeight: '700',
  },
});
