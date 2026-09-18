import { useRouter } from 'expo-router';

import { SignInScreen } from '../../src/features/access/ui/SignInScreen';

export default function SignInRoute() {
  const router = useRouter();

  return (
    <SignInScreen onCreateAccount={() => router.push('/create-account')} />
  );
}
