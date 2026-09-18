import { useRouter } from 'expo-router';
import { SafeAreaView, StyleSheet } from 'react-native';

import { SectionPlaceholder } from '../../src/ui/navigation/SectionPlaceholder';

export default function WelcomeRoute() {
  const router = useRouter();

  return (
    <SafeAreaView style={styles.screen}>
      <SectionPlaceholder
        eyebrow="DANTE"
        title="Welcome"
        copy="The public access area is structurally ready. Authentication providers and session restoration will be connected only to the real backend contract."
        actionLabel="Continue to sign in"
        onAction={() => router.push('/sign-in')}
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
