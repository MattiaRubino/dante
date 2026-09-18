import { useRouter } from 'expo-router';
import { SafeAreaView, StyleSheet } from 'react-native';

import { SectionPlaceholder } from '../src/ui/navigation/SectionPlaceholder';

export default function AiRoute() {
  const router = useRouter();

  return (
    <SafeAreaView style={styles.screen}>
      <SectionPlaceholder
        eyebrow="GLOBAL ACTION"
        title="DANTE AI"
        copy="AI is a global entry point rather than a peer navigation section. Chat, voice and backend behavior will be activated only when their real product contract is scoped."
        actionLabel="Close"
        onAction={() => router.back()}
      />
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  screen: {
    flex: 1,
    justifyContent: 'center',
    backgroundColor: '#0b1020',
    paddingHorizontal: 24,
  },
});
