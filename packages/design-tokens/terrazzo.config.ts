import { defineConfig } from '@terrazzo/cli';
import css from '@terrazzo/plugin-css';

import nativePlugin from './tooling/native-plugin.ts';

export default defineConfig({
  tokens: ['./tokens/primitives.json', './tokens/semantic.json'],
  outDir: './generated',
  plugins: [
    css({
      filename: 'web.css',
      variableName: (token) =>
        `--dante-${token.id.replace(/\./g, '-').toLowerCase()}`,
    }),
    nativePlugin(),
  ],
});
