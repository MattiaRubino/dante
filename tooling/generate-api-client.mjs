import { spawnSync } from 'node:child_process';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const thisFile = fileURLToPath(import.meta.url);
const repoRoot = resolve(dirname(thisFile), '..');
const backendRoot = join(repoRoot, 'apps/backend');
const openapiRelativePath = 'packages/api-client/openapi/dante-v1.openapi.json';
const generatedRelativePath = 'packages/api-client/src/generated';

function run(command, args, { cwd = repoRoot, label }) {
  const result = spawnSync(command, args, {
    cwd,
    encoding: 'utf8',
    stdio: 'inherit',
  });

  if (result.error) {
    throw result.error;
  }

  if (result.status !== 0) {
    throw new Error(`${label} failed with exit code ${result.status}`);
  }
}

run(
  'uv',
  [
    'run',
    '--locked',
    'python',
    '-m',
    'dante.bootstrap.openapi_export',
    join(repoRoot, openapiRelativePath),
  ],
  {
    cwd: backendRoot,
    label: 'deterministic FastAPI OpenAPI export',
  },
);

run('pnpm', ['--filter', '@dante/api-client', 'generate'], {
  label: 'Orval API client generation',
});

run(
  'pnpm',
  [
    'exec',
    'prettier',
    '--write',
    openapiRelativePath,
    generatedRelativePath,
  ],
  {
    label: 'generated API formatting',
  },
);
