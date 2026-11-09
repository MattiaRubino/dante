import { defineConfig } from 'vitest/config';

import { dayRibbonBackdropPlugin } from './config/day-ribbon-backdrop-plugin.ts';

export default defineConfig({
  plugins: [dayRibbonBackdropPlugin()],
  test: {
    environment: 'jsdom',
    include: ['src/**/*.test.{ts,tsx}'],
  },
});
