import { spawnSync } from 'node:child_process';
import { mkdtemp, readFile, rm, writeFile } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { dirname, join, resolve } from 'node:path';
import process from 'node:process';
import { fileURLToPath } from 'node:url';

const thisFile = fileURLToPath(import.meta.url);
const repoRoot = resolve(dirname(thisFile), '..');

const generatedPaths = [
  'packages/design-tokens/generated/web.css',
  'packages/design-tokens/generated/native.ts',
  'apps/web/src/routeTree.gen.ts',
];

const snapshots = new Map();
let tempRoot;

function run(command, args, label) {
  const result = spawnSync(command, args, {
    cwd: repoRoot,
    encoding: 'utf8',
    stdio: ['ignore', 'pipe', 'pipe'],
    env: process.env,
  });

  if (result.stdout) {
    process.stdout.write(result.stdout);
  }

  if (result.stderr) {
    process.stderr.write(result.stderr);
  }

  if (result.error) {
    throw result.error;
  }

  if (result.status !== 0) {
    throw new Error(`${label} failed with exit code ${result.status}`);
  }
}

async function snapshotGeneratedFiles() {
  for (const relativePath of generatedPaths) {
    snapshots.set(relativePath, await readFile(join(repoRoot, relativePath)));
  }
}

async function regenerate() {
  run(
    'pnpm',
    ['--filter', '@dante/design-tokens', 'generate'],
    'design-token generation',
  );

  tempRoot = await mkdtemp(join(tmpdir(), 'dante-fm06b-'));

  run(
    'pnpm',
    [
      '--filter',
      '@dante/web',
      'exec',
      'vite',
      'build',
      '--outDir',
      join(tempRoot, 'web-dist'),
      '--emptyOutDir',
    ],
    'TanStack Router generation through the real Vite plugin',
  );
}

async function findDrift() {
  const drifted = [];

  for (const relativePath of generatedPaths) {
    const regenerated = await readFile(join(repoRoot, relativePath));
    const original = snapshots.get(relativePath);

    if (!original.equals(regenerated)) {
      drifted.push(relativePath);
    }
  }

  return drifted;
}

async function restoreSnapshots() {
  for (const [relativePath, content] of snapshots) {
    await writeFile(join(repoRoot, relativePath), content);
  }

  if (tempRoot) {
    await rm(tempRoot, { recursive: true, force: true });
  }
}

let drifted = [];
let failure;

try {
  await snapshotGeneratedFiles();
  await regenerate();
  drifted = await findDrift();
} catch (error) {
  failure = error;
} finally {
  await restoreSnapshots();
}

if (failure) {
  process.stderr.write(
    `generated-source check could not complete: ${failure.message}\n`,
  );
  process.exitCode = 1;
} else if (drifted.length > 0) {
  process.stderr.write('Generated source drift detected:\n');

  for (const relativePath of drifted) {
    process.stderr.write(`- ${relativePath}\n`);
  }

  process.stderr.write(
    'Regenerate the owning source with the real generator and commit the generated output.\n',
  );
  process.exitCode = 1;
} else {
  process.stdout.write(
    `PASS: generated sources are deterministic and current (${generatedPaths.length} files)\n`,
  );
}
