import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { RouterProvider, createRouter } from '@tanstack/react-router';

import '@dante/design-tokens/web.css';
import './bootstrap/i18n';
import {
  initializeWebObservability,
  ObservabilityErrorBoundary,
} from './platform/observability';
import { routeTree } from './routeTree.gen';
import './styles.css';

void initializeWebObservability();

const queryClient = new QueryClient({
  defaultOptions: {
    mutations: {
      retry: false,
    },
  },
});

const router = createRouter({
  routeTree,
  context: {
    queryClient,
  },
  defaultPreloadStaleTime: 0,
});

declare module '@tanstack/react-router' {
  interface Register {
    router: typeof router;
  }
}

const rootElement = document.getElementById('root');

if (!rootElement) {
  throw new Error('DANTE Web root element was not found.');
}

createRoot(rootElement).render(
  <StrictMode>
    <ObservabilityErrorBoundary>
      <QueryClientProvider client={queryClient}>
        <RouterProvider router={router} />
      </QueryClientProvider>
    </ObservabilityErrorBoundary>
  </StrictMode>,
);
