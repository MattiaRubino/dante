import { randomUUID } from 'node:crypto';

import { defineConfig } from '@playwright/test';

const authPort = Number(process.env.DANTE_E2E_WEB_PORT ?? 4173);
if (!Number.isInteger(authPort) || authPort < 1 || authPort > 65535) {
  throw new Error('DANTE_E2E_WEB_PORT must be a valid TCP port');
}
const baseURL = `https://127.0.0.1:${authPort}`;

process.env.DANTE_E2E_CONTROL_ID ??= randomUUID();
process.env.DANTE_E2E_SIGNIN_RATE_CAPACITY = '2';

export default defineConfig({
  testDir: './e2e/auth',
  fullyParallel: false,
  workers: 1,
  retries: 0,
  timeout: 60_000,
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
