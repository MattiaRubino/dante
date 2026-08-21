import type { ExpoConfig } from 'expo/config';

const config: ExpoConfig = {
  name: 'DANTE Mobile',
  slug: 'dante-mobile',
  version: '0.0.0',
  orientation: 'portrait',
  scheme: 'dante',
  userInterfaceStyle: 'automatic',
  plugins: ['expo-router'],
  experiments: {
    typedRoutes: true,
  },
};

export default config;
