import { defineConfig } from 'orval';

export default defineConfig({
  dante: {
    input: {
      target: './openapi/dante-v1.openapi.json',
    },
    output: {
      mode: 'single',
      target: './src/generated/dante.ts',
      schemas: {
        path: './src/generated/model',
        type: 'zod',
      },
      client: 'fetch',
      clean: true,
      headers: true,
      override: {
        fetch: {
          forceSuccessResponse: false,
          includeHttpResponseReturnType: true,
          runtimeValidation: false,
          serializeResponseHeaders: false,
          useRuntimeFetcher: true,
        },
        zod: {
          strict: {
            response: true,
          },
          variant: 'mini',
          version: 4,
        },
      },
    },
  },
});
