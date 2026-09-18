import { useRouter } from 'expo-router';

import { CreateAccountScreen } from '../../src/features/access/ui/CreateAccountScreen';

export default function CreateAccountRoute() {
  const router = useRouter();

  return (
    <CreateAccountScreen onBackToSignIn={() => router.replace('/sign-in')} />
  );
}
