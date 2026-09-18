import type { ExpoConfig } from 'expo/config';

const config: ExpoConfig = {
  name: 'DANTE Mobile',
  slug: 'dante-mobile',
  version: '0.0.0',
  orientation: 'portrait',
  scheme: 'dante',
  userInterfaceStyle: 'automatic',
  android: {
    package: 'com.dantearc.dante',
  },
  plugins: ['expo-router', 'expo-system-ui'],
  experiments: {
    typedRoutes: true,
  },
};

export default config;
