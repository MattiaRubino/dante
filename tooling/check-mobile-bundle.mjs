import { spawnSync } from 'node:child_process';
import { access, mkdtemp, readdir, rm, stat } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { dirname, join, relative, resolve, sep } from 'node:path';
import process from 'node:process';
import { fileURLToPath } from 'node:url';

const thisFile = fileURLToPath(import.meta.url);
const repoRoot = resolve(dirname(thisFile), '..');
const mobileRoot = join(repoRoot, 'apps', 'mobile');

async function collectFiles(root) {
  const files = [];

  async function walk(current) {
    for (const entry of await readdir(current, { withFileTypes: true })) {
      const absolute = join(current, entry.name);

      if (entry.isDirectory()) {
        await walk(absolute);
      } else if (entry.isFile()) {
        files.push(absolute);
      }
    }
  }

  await walk(root);
  return files;
}

function runExpoExport(outputDir) {
  const result = spawnSync(
    'pnpm',
    [
      'exec',
      'expo',
      'export',
      '--platform',
      'android',
      '--output-dir',
      outputDir,
    ],
    {
      cwd: mobileRoot,
      encoding: 'utf8',
      stdio: ['ignore', 'pipe', 'pipe'],
      env: {
        ...process.env,
        CI: '1',
        EXPO_NO_TELEMETRY: '1',
      },
    },
  );

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
    throw new Error(
      `Expo Android export failed with exit code ${result.status}`,
    );
  }
}

const tempRoot = await mkdtemp(join(tmpdir(), 'dante-fm06d-mobile-'));
const outputDir = join(tempRoot, 'dist');

let failure;
let bundleEvidence;

try {
  runExpoExport(outputDir);

  const files = await collectFiles(outputDir);
  const androidBundles = files.filter((file) => {
    const normalized = file.split(sep);
    return file.endsWith('.hbc') && normalized.includes('android');
  });

  if (androidBundles.length === 0) {
    throw new Error(
      'Expo export produced no Android Hermes .hbc bundle under the temporary output',
    );
  }

  const bundleStats = await Promise.all(
    androidBundles.map(async (file) => ({
      file,
      size: (await stat(file)).size,
    })),
  );

  const empty = bundleStats.filter(({ size }) => size <= 0);
  if (empty.length > 0) {
    throw new Error(
      `Expo export produced empty Hermes bundle(s): ${empty
        .map(({ file }) => relative(outputDir, file))
        .join(', ')}`,
    );
  }

  bundleEvidence = bundleStats
    .map(
      ({ file, size }) =>
        `${relative(outputDir, file)} (${size.toLocaleString('en-US')} bytes)`,
    )
    .join('\n');
} catch (error) {
  failure = error;
} finally {
  await rm(tempRoot, { recursive: true, force: true });
}

let tempStillExists = true;
try {
  await access(tempRoot);
} catch {
  tempStillExists = false;
}

if (tempStillExists) {
  process.stderr.write(
    `Mobile bundle smoke cleanup failed: temporary directory still exists: ${tempRoot}\n`,
  );
  process.exitCode = 1;
} else if (failure) {
  process.stderr.write(`Mobile bundle smoke failed: ${failure.message}\n`);
  process.exitCode = 1;
} else {
  process.stdout.write('PASS: Android Hermes bundle smoke\n');
  process.stdout.write(`${bundleEvidence}\n`);
  process.stdout.write('PASS: temporary mobile export removed\n');
}
