#!/usr/bin/env node

import { readFile, stat } from 'node:fs/promises';
import process from 'node:process';
import { fileURLToPath } from 'node:url';
import { dirname, join, relative, resolve } from 'node:path';

const scriptDirectory = dirname(fileURLToPath(import.meta.url));
const repositoryRoot = resolve(scriptDirectory, '..', '..');
const webDistribution = join(repositoryRoot, 'apps', 'web', 'dist');
const manifestPath = join(webDistribution, '.vite', 'manifest.json');

const ENTRY_BUDGET_BYTES = 500 * 1024;
const OBSERVABILITY_BUDGET_BYTES = 300 * 1024;
const OBSERVABILITY_RUNTIME = 'src/platform/observability/runtime.ts';

function fail(message) {
  process.stderr.write(`web observability bundle check failed: ${message}\n`);
  process.exitCode = 1;
}

async function fileSize(file) {
  return (await stat(join(webDistribution, file))).size;
}

let manifest;
try {
  manifest = JSON.parse(await readFile(manifestPath, 'utf8'));
} catch (error) {
  fail(
    `cannot read ${relative(repositoryRoot, manifestPath)}: ${error.message}`,
  );
  process.exit();
}

const entries = Object.entries(manifest);
const applicationEntry = entries.find(([, chunk]) => chunk.isEntry === true);
const observabilityEntry = entries.find(
  ([source]) => source === OBSERVABILITY_RUNTIME,
);

if (applicationEntry === undefined) {
  fail('Vite manifest has no application entry');
}
if (observabilityEntry === undefined) {
  fail('Vite manifest has no Faro runtime chunk');
}

if (applicationEntry !== undefined && observabilityEntry !== undefined) {
  const [observabilitySource, observabilityChunk] = observabilityEntry;
  if (observabilityChunk.isDynamicEntry !== true) {
    fail('Faro runtime must remain a dynamic entry');
  }
  if (!applicationEntry[1].dynamicImports?.includes(observabilitySource)) {
    fail('application entry must lazy-load the governed Faro runtime chunk');
  }

  const [entrySize, observabilitySize] = await Promise.all([
    fileSize(applicationEntry[1].file),
    fileSize(observabilityChunk.file),
  ]);
  if (entrySize > ENTRY_BUDGET_BYTES) {
    fail(
      `initial Web entry is ${entrySize} bytes; budget is ${ENTRY_BUDGET_BYTES}`,
    );
  }
  if (observabilitySize > OBSERVABILITY_BUDGET_BYTES) {
    fail(
      `Faro chunk is ${observabilitySize} bytes; budget is ${OBSERVABILITY_BUDGET_BYTES}`,
    );
  }

  if (process.exitCode === undefined) {
    process.stdout.write(
      `PASS: Web entry ${entrySize} B; lazy Faro ${observabilitySize} B\n`,
    );
  }
}
