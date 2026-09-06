export default {
  forbidden: [
    {
      name: 'not-to-unresolvable',
      comment: 'Production frontend source imports must resolve.',
      severity: 'error',
      from: {
        path: '^(apps/(web|mobile)|packages/(api-client|design-tokens|i18n|time))/',
      },
      to: {
        pathNot: '^virtual:dante-day-ribbon-backdrop$',
        couldNotResolve: true,
      },
    },
    {
      name: 'no-circular-source',
      comment:
        'Current frontend source/package dependencies must remain acyclic.',
      severity: 'error',
      from: {
        path: '^(apps/(web|mobile)|packages/(api-client|design-tokens|i18n|time))/',
      },
      to: {
        circular: true,
      },
    },
    {
      name: 'web-routes-use-feature-public-api',
      comment:
        'Web routes may consume a feature only through approved public entrypoints, never through feature internals.',
      severity: 'error',
      from: {
        path: '^apps/web/src/routes/',
      },
      to: {
        path: '^apps/web/src/features/[^/]+/(?!(?:index|route-contract)\\.(ts|tsx)$)',
      },
    },
    {
      name: 'access-ui-model-use-application-boundary',
      comment:
        'Access UI/model cannot bypass its application boundary to reach transport or the API client.',
      severity: 'error',
      from: {
        path: '^apps/web/src/features/access/(ui|model)/',
      },
      to: {
        path: ['^apps/web/src/platform/auth/', '^packages/api-client/'],
      },
    },
    {
      name: 'access-feature-no-api-client-direct',
      comment:
        'Access consumes the API client only through the Web remote data-source boundary.',
      severity: 'error',
      from: {
        path: '^apps/web/src/features/access/',
      },
      to: {
        path: '^packages/api-client/',
      },
    },
    {
      name: 'web-no-generated-api-client-internals',
      comment:
        'Web consumes @dante/api-client through its governed package boundary, never raw Orval generated internals.',
      severity: 'error',
      from: {
        path: '^apps/web/src/',
      },
      to: {
        path: '^packages/api-client/src/generated/',
      },
    },
    {
      name: 'observability-has-no-product-data-dependencies',
      comment:
        'Telemetry adapters remain cross-cutting and privacy-safe; they cannot import product features, Auth transport or API data contracts.',
      severity: 'error',
      from: {
        path: '^apps/web/src/platform/observability/',
      },
      to: {
        path: [
          '^apps/web/src/features/',
          '^apps/web/src/platform/auth/',
          '^packages/api-client/',
        ],
      },
    },
    {
      name: 'web-not-to-mobile',
      comment:
        'Web and Mobile are sibling deployables, never source dependencies.',
      severity: 'error',
      from: {
        path: '^apps/web/',
      },
      to: {
        path: '^apps/mobile/',
      },
    },
    {
      name: 'mobile-not-to-web',
      comment:
        'Web and Mobile are sibling deployables, never source dependencies.',
      severity: 'error',
      from: {
        path: '^apps/mobile/',
      },
      to: {
        path: '^apps/web/',
      },
    },
    {
      name: 'shared-not-to-apps',
      comment:
        'Shared packages cannot depend on deployable application source.',
      severity: 'error',
      from: {
        path: '^packages/(api-client|design-tokens|i18n|time)/',
      },
      to: {
        path: '^apps/',
      },
    },
    {
      name: 'production-not-to-prototypes',
      comment: 'Production frontend code cannot depend on prototype evidence.',
      severity: 'error',
      from: {
        path: '^(apps/(web|mobile)|packages/(api-client|design-tokens|i18n|time))/',
      },
      to: {
        path: '^prototypes/',
      },
    },
    {
      name: 'shared-core-no-framework',
      comment:
        'Shared cores remain framework/platform-free unless a later bounded decision explicitly changes that.',
      severity: 'error',
      from: {
        path: '^packages/(api-client|design-tokens|i18n|time)/',
      },
      to: {
        path: [
          '^react$',
          '^react/',
          '^react-dom$',
          '^react-dom/',
          '^react-i18next$',
          '^react-i18next/',
          '^react-native$',
          '^react-native-',
          '^react-native/',
          '^expo$',
          '^expo-',
          '^expo/',
          '^vite$',
          '^vite/',
          '^@vitejs/',
          'node_modules/react$',
          'node_modules/react/',
          'node_modules/react-dom$',
          'node_modules/react-dom/',
          'node_modules/react-i18next$',
          'node_modules/react-i18next/',
          'node_modules/react-native$',
          'node_modules/react-native-',
          'node_modules/react-native/',
          'node_modules/expo$',
          'node_modules/expo-',
          'node_modules/expo/',
          'node_modules/vite$',
          'node_modules/vite/',
          'node_modules/@vitejs/',
        ],
      },
    },
  ],
  options: {
    doNotFollow: {
      path: 'node_modules',
    },
    tsPreCompilationDeps: true,
    combinedDependencies: false,
    skipAnalysisNotInRules: true,
    enhancedResolveOptions: {
      exportsFields: ['exports'],
      aliasFields: ['browser'],
      conditionNames: [
        'import',
        'require',
        'react-native',
        'browser',
        'default',
      ],
      extensions: [
        '.js',
        '.jsx',
        '.cjs',
        '.mjs',
        '.ts',
        '.tsx',
        '.cts',
        '.mts',
        '.d.ts',
        '.json',
      ],
    },
  },
};
