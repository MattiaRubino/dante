import { defineConfig } from '@playwright/test';

// Playwright may evaluate this config in multiple processes. The default port
// must therefore be stable across the runner, web server, and workers.
const e2ePort = Number(process.env.PLAYWRIGHT_PORT ?? 43117);
const baseURL = `http://127.0.0.1:${e2ePort}`;

export default defineConfig({
  testDir: './e2e',
  testIgnore: ['**/auth/**'],
  fullyParallel: false,
  workers: 1,
  retries: 0,
  reporter: 'line',
  use: {
    baseURL,
    browserName: 'chromium',
    headless: true,
    trace: 'retain-on-failure',
  },
  webServer: {
    // Non-auth E2E exercises the frozen interaction contract through the
    // explicit test-only Timeline fixture boundary. Auth/full-stack proofs use
    // playwright.auth.config.ts and therefore keep the real production path.
    command: `pnpm exec vite build --mode test && node ../../tooling/observability/check-web-bundle.mjs && pnpm exec vite preview --host 127.0.0.1 --port ${e2ePort} --strictPort`,
    url: baseURL,
    reuseExistingServer: false,
    timeout: 120_000,
    stdout: 'pipe',
    stderr: 'pipe',
    env: {
      VITE_DANTE_GOOGLE_CLIENT_ID:
        'dante-e2e-client.apps.googleusercontent.com',
      VITE_DANTE_APPLE_ENABLED: 'true',
    },
  },
});
