import type { Href } from 'expo-router';
import { Stack, usePathname, useRouter } from 'expo-router';

import {
  PrimaryScreenFrame,
  type AppShellDestination,
} from '../../src/ui/navigation/PrimaryScreenFrame';

const APP_PATHS: Record<AppShellDestination, Href> = {
  home: '/home',
  timeline: '/timeline',
  worlds: '/worlds',
  more: '/more',
};

const APP_TITLES: Record<AppShellDestination, string> = {
  home: 'Home',
  timeline: 'Timeline',
  worlds: 'Worlds',
  more: 'More',
};

function getActiveDestination(pathname: string): AppShellDestination {
  if (pathname.startsWith('/timeline')) {
    return 'timeline';
  }

  if (pathname.startsWith('/worlds')) {
    return 'worlds';
  }

  if (pathname.startsWith('/more')) {
    return 'more';
  }

  return 'home';
}

export default function AppLayout() {
  const pathname = usePathname();
  const router = useRouter();
  const active = getActiveDestination(pathname);

  const navigate = (destination: AppShellDestination) => {
    router.replace(APP_PATHS[destination]);
  };

  return (
    <PrimaryScreenFrame
      active={active}
      title={APP_TITLES[active]}
      onNavigate={navigate}
      onAi={() => router.push('/ai')}
      onMore={() => navigate('more')}
    >
      <Stack screenOptions={{ headerShown: false, animation: 'fade' }} />
    </PrimaryScreenFrame>
  );
}
