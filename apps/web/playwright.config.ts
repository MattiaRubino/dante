import { defineConfig } from '@playwright/test';

// Playwright may evaluate this config in multiple processes. The default port
// must therefore be stable across the runner, web server, and workers.
const e2ePort = Number(process.env.PLAYWRIGHT_PORT ?? 43117);
const baseURL = `http://127.0.0.1:${e2ePort}`;

// The authoritative standalone browser gate keeps its historical single
// worker. Only the opt-in isolated parallel runner sets this value; browser
// contexts and fixtures remain test-local.
const nonAuthWorkers = Number(process.env.DANTE_E2E_NONAUTH_WORKERS ?? 1);
if (!Number.isInteger(nonAuthWorkers) || nonAuthWorkers < 1 || nonAuthWorkers > 6) {
  throw new Error('DANTE_E2E_NONAUTH_WORKERS must be an integer from 1 to 6');
}

export default defineConfig({
  testDir: './e2e',
  testIgnore: ['**/auth/**'],
  fullyParallel: false,
  workers: nonAuthWorkers,
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
