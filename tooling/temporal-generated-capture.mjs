/* Temporary local-only CI capture; deleted after canonical output is committed. */
import { spawnSync } from 'node:child_process';
import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';

function run(binary, args) {
  const result = spawnSync(binary, args, {
    cwd: resolve('.'),
    encoding: 'utf8',
    stdio: 'inherit',
  });
  if (result.error) throw result.error;
  if (result.status !== 0) throw new Error(`${binary} exited ${result.status}`);
}

run('pnpm', [
  'exec',
  'prettier',
  '--write',
  'apps/web/src/features/home/ui/timeline/event-inspector-actions.tsx',
  'tooling/temporal-generated-capture.mjs',
]);
run('pnpm', ['api:generate']);
const status = spawnSync(
  'git',
  ['status', '--porcelain', '--untracked-files=all'],
  { encoding: 'utf8' },
);
if (status.error || status.status !== 0) throw new Error('Cannot list generated deltas');
const filePaths = new Set([
  'apps/web/src/features/home/ui/timeline/event-inspector-actions.tsx',
]);
for (const line of status.stdout.split('\n')) {
  const path = line.slice(3).trim();
  if (
    path.startsWith('packages/api-client/openapi/') ||
    path.startsWith('packages/api-client/src/generated/')
  ) {
    filePaths.add(path);
  }
}
for (const filePath of [...filePaths].sort()) {
  const encoded = readFileSync(filePath).toString('base64');
  const chunkSize = 2048;
  const count = Math.ceil(encoded.length / chunkSize);
  for (let index = 0; index < count; index += 1) {
    process.stdout.write(
      `DANTE_TEMPORAL_CAPTURE:${encodeURIComponent(filePath)}:${index}:${count}:${encoded.slice(index * chunkSize, (index + 1) * chunkSize)}\n`,
    );
  }
}
