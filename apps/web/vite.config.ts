import { createHash } from 'node:crypto';
import { readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';

import { tanstackRouter } from '@tanstack/router-plugin/vite';
import react from '@vitejs/plugin-react';
import { defineConfig, type Plugin } from 'vite';

const DAY_RIBBON_MODULE_ID = 'virtual:dante-day-ribbon-backdrop';
const RESOLVED_DAY_RIBBON_MODULE_ID = `\0${DAY_RIBBON_MODULE_ID}`;
const DAY_RIBBON_PROTOTYPE_PATH = fileURLToPath(
  new URL('../../prototypes/frontend/home/current/home.html', import.meta.url),
);
const DAY_RIBBON_ASSET_BYTES = 281_038;
const DAY_RIBBON_ASSET_SHA256 =
  '9a273c238835dfd66b65544004d75e2adba03971add634a35e86d7fe10f0cc4d';

type DayRibbonAsset = Readonly<{
  base64: string;
  bytes: Buffer;
}>;

function dayRibbonBackdropPlugin(): Plugin {
  let command: 'build' | 'serve' = 'serve';
  let cachedAsset: DayRibbonAsset | null = null;

  const readBackdrop = (): DayRibbonAsset => {
    if (cachedAsset) {
      return cachedAsset;
    }

    const prototype = readFileSync(DAY_RIBBON_PROTOTYPE_PATH, 'utf8');
    const match =
      /var BACKDROP_HREF = 'data:image\/png;base64,([A-Za-z0-9+/=]+)'/.exec(
        prototype,
      );
    if (!match?.[1]) {
      throw new Error('Accepted Home day-ribbon backdrop was not found.');
    }

    const bytes = Buffer.from(match[1], 'base64');
    const sha256 = createHash('sha256').update(bytes).digest('hex');
    if (
      bytes.byteLength !== DAY_RIBBON_ASSET_BYTES ||
      sha256 !== DAY_RIBBON_ASSET_SHA256
    ) {
      throw new Error(
        `Accepted Home day-ribbon backdrop identity mismatch: bytes=${bytes.byteLength} sha256=${sha256}`,
      );
    }

    cachedAsset = { base64: match[1], bytes };
    return cachedAsset;
  };

  return {
    name: 'dante-day-ribbon-backdrop',
    enforce: 'pre',
    configResolved(config) {
      command = config.command;
    },
    resolveId(id) {
      return id === DAY_RIBBON_MODULE_ID ? RESOLVED_DAY_RIBBON_MODULE_ID : null;
    },
    load(id) {
      if (id !== RESOLVED_DAY_RIBBON_MODULE_ID) {
        return null;
      }

      const asset = readBackdrop();
      if (command === 'serve') {
        return `export default ${JSON.stringify(`data:image/png;base64,${asset.base64}`)};`;
      }

      const referenceId = this.emitFile({
        type: 'asset',
        name: 'day-ribbon-backdrop.png',
        source: asset.bytes,
      });
      return `export default import.meta.ROLLUP_FILE_URL_${referenceId};`;
    },
  };
}

export default defineConfig({
  plugins: [
    dayRibbonBackdropPlugin(),
    tanstackRouter({
      target: 'react',
      autoCodeSplitting: true,
    }),
    react(),
  ],
});
