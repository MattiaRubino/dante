import { useState } from 'react';

import { createB14TemporalCreateRuntime } from '../application/temporal-create-b14-runtime';
import {
  TemporalCreateEntry as BaseTemporalCreateEntry,
  type TemporalCreateEntryProps,
  type TemporalCreateInvocation,
} from './temporal-create-entry';

export type { TemporalCreateEntryProps, TemporalCreateInvocation };

export function TemporalCreateEntry(props: TemporalCreateEntryProps) {
  const [runtime] = useState(
    () => props.runtime ?? createB14TemporalCreateRuntime(),
  );
  return <BaseTemporalCreateEntry {...props} runtime={runtime} />;
}
