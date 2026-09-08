import { createContext, useContext, type ReactNode } from 'react';

import type {
  TemporalCreateContextInput,
  TemporalCreateContextOption,
} from './temporal-create-ui-types';

export type TemporalCreateContextCreator = (
  input: TemporalCreateContextInput,
) => TemporalCreateContextOption;

const TemporalCreateContextCatalog =
  createContext<TemporalCreateContextCreator | null>(null);

export function temporalCreateLocalContextAuthoringEnabled(
  mode: string,
): boolean {
  return mode === 'test';
}

export function TemporalCreateContextCatalogProvider({
  onCreateContext,
  children,
  mode = import.meta.env.MODE,
}: Readonly<{
  onCreateContext: TemporalCreateContextCreator;
  children: ReactNode;
  mode?: string;
}>) {
  const creator = temporalCreateLocalContextAuthoringEnabled(mode)
    ? onCreateContext
    : null;

  return (
    <TemporalCreateContextCatalog.Provider value={creator}>
      {children}
    </TemporalCreateContextCatalog.Provider>
  );
}

export function useTemporalCreateContextCreator(): TemporalCreateContextCreator | null {
  return useContext(TemporalCreateContextCatalog);
}
