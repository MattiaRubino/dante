import { defineConfig } from '@playwright/test';

const baseURL = 'https://127.0.0.1:4173';

process.env.DANTE_E2E_SIGNIN_RATE_CAPACITY = '2';

export default defineConfig({
  testDir: './e2e/auth',
  fullyParallel: false,
  workers: 1,
  retries: 0,
  reporter: 'line',
  use: {
    baseURL,
    headless: true,
    ignoreHTTPSErrors: true,
    trace: 'retain-on-failure',
  },
  projects: [
    {
      name: 'chromium',
      use: { browserName: 'chromium' },
    },
    {
      name: 'firefox',
      use: { browserName: 'firefox' },
    },
    {
      name: 'webkit',
      use: { browserName: 'webkit' },
    },
  ],
  webServer: {
    command:
      'uv run --project ../backend python ../../tooling/run-access-auth-stack.py',
    url: baseURL,
    reuseExistingServer: false,
    timeout: 180_000,
    stdout: 'pipe',
    stderr: 'pipe',
    ignoreHTTPSErrors: true,
    gracefulShutdown: {
      signal: 'SIGTERM',
      timeout: 10_000,
    },
  },
});
