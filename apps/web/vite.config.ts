import { readFileSync } from 'node:fs';

import { tanstackRouter } from '@tanstack/router-plugin/vite';
import react from '@vitejs/plugin-react';
import { defineConfig, type PreviewOptions } from 'vite';

function accessAuthPreview(): PreviewOptions | undefined {
  const apiTarget = process.env.DANTE_E2E_API_TARGET;
  const certPath = process.env.DANTE_E2E_TLS_CERT;
  const keyPath = process.env.DANTE_E2E_TLS_KEY;

  if (
    apiTarget === undefined &&
    certPath === undefined &&
    keyPath === undefined
  ) {
    return undefined;
  }

  if (
    apiTarget === undefined ||
    certPath === undefined ||
    keyPath === undefined
  ) {
    throw new Error(
      'DANTE full-stack preview requires API target plus TLS certificate and key.',
    );
  }

  return {
    host: '127.0.0.1',
    port: 4173,
    strictPort: true,
    https: {
      cert: readFileSync(certPath),
      key: readFileSync(keyPath),
    },
    proxy: {
      '/api/v1': {
        target: apiTarget,
        changeOrigin: false,
      },
    },
  };
}

const preview = accessAuthPreview();

export default defineConfig({
  build: {
    manifest: true,
  },
  plugins: [
    tanstackRouter({
      target: 'react',
      autoCodeSplitting: true,
    }),
    react(),
  ],
  ...(preview === undefined ? {} : { preview }),
});
