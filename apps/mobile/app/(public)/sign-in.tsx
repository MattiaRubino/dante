import { useRouter } from 'expo-router';
import { SafeAreaView, StyleSheet } from 'react-native';

import { SectionPlaceholder } from '../../src/ui/navigation/SectionPlaceholder';

export default function SignInRoute() {
  const router = useRouter();

  return (
    <SafeAreaView style={styles.screen}>
      <SectionPlaceholder
        eyebrow="ACCESS"
        title="Sign in"
        copy="This is the access-route shell only. Password, Google, passkey and session behavior are intentionally not invented before the backend identity contract is inspected."
        actionLabel="Back to welcome"
        onAction={() => router.replace('/welcome')}
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
