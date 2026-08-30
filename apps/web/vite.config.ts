import { tanstackRouter } from '@tanstack/router-plugin/vite';
import react from '@vitejs/plugin-react';
import { defineConfig } from 'vite';

import { dayRibbonBackdropPlugin } from './config/day-ribbon-backdrop-plugin.ts';

export default defineConfig({
  plugins: [
    dayRibbonBackdropPlugin(),
    tanstackRouter({
      target: 'react',
      autoCodeSplitting: true,
    }),
    react(),
  ],
});
