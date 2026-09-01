export default {
  forbidden: [
    {
      name: 'not-to-unresolvable',
      comment: 'Production frontend source imports must resolve.',
      severity: 'error',
      from: {
        path: '^(apps/(web|mobile)|packages/(design-tokens|i18n|time))/',
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
        path: '^(apps/(web|mobile)|packages/(design-tokens|i18n|time))/',
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
      name: 'world-focus-model-stays-inner',
      comment:
        'World Focus model code is an inner layer and must not depend on application orchestration, UI rendering, or app routes.',
      severity: 'error',
      from: {
        path: '^apps/web/src/features/world-focus/model/',
      },
      to: {
        path: [
          '^apps/web/src/features/world-focus/application/',
          '^apps/web/src/features/world-focus/ui/',
          '^apps/web/src/routes/',
        ],
      },
    },
    {
      name: 'world-focus-application-not-to-ui-or-routes',
      comment:
        'World Focus application code may orchestrate model contracts but cannot depend on React UI or route modules.',
      severity: 'error',
      from: {
        path: '^apps/web/src/features/world-focus/application/',
      },
      to: {
        path: [
          '^apps/web/src/features/world-focus/ui/',
          '^apps/web/src/routes/',
        ],
      },
    },
    {
      name: 'world-focus-not-to-home-internals',
      comment:
        'World Focus is a sibling feature of Home and may not depend on Home internals; any future crossing must use an approved Home public entrypoint.',
      severity: 'error',
      from: {
        path: '^apps/web/src/features/world-focus/',
      },
      to: {
        path: '^apps/web/src/features/home/(?!(?:index|route-contract)\\.(ts|tsx)$)',
      },
    },
    {
      name: 'other-features-use-world-focus-public-api',
      comment:
        'Other web features may consume World Focus only through approved public entrypoints, never through World Focus internals.',
      severity: 'error',
      from: {
        path: '^apps/web/src/features/(?!world-focus(?:/|$))',
      },
      to: {
        path: '^apps/web/src/features/world-focus/(?!(?:index|route-contract)\\.(ts|tsx)$)',
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
        path: '^packages/(design-tokens|i18n|time)/',
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
        path: '^(apps/(web|mobile)|packages/(design-tokens|i18n|time))/',
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
        path: '^packages/(design-tokens|i18n|time)/',
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
