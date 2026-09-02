import {
  createContext,
  useContext,
  type ReactNode,
} from 'react';

import type {
  TemporalCreateContextInput,
  TemporalCreateContextOption,
} from './temporal-create-ui-types';

export type TemporalCreateContextCreator = (
  input: TemporalCreateContextInput,
) => TemporalCreateContextOption;

const TemporalCreateContextCatalog = createContext<TemporalCreateContextCreator | null>(
  null,
);

export function TemporalCreateContextCatalogProvider({
  onCreateContext,
  children,
}: Readonly<{
  onCreateContext: TemporalCreateContextCreator;
  children: ReactNode;
}>) {
  return (
    <TemporalCreateContextCatalog.Provider value={onCreateContext}>
      {children}
    </TemporalCreateContextCatalog.Provider>
  );
}

export function useTemporalCreateContextCreator(): TemporalCreateContextCreator | null {
  return useContext(TemporalCreateContextCatalog);
}
