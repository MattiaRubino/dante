import { useRouter } from 'expo-router';

import { WelcomeScreen } from '../../src/features/access/ui/WelcomeScreen';

export default function WelcomeRoute() {
  const router = useRouter();

  return <WelcomeScreen onContinue={() => router.push('/sign-in')} />;
}
