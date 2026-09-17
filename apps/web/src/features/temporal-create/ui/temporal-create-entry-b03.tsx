import { useState } from 'react';

import { createB03TemporalCreateRuntime } from '../application/temporal-create-b03-runtime';
import {
  TemporalCreateEntry as BaseTemporalCreateEntry,
  type TemporalCreateEntryProps,
  type TemporalCreateInvocation,
} from './temporal-create-entry';

export type { TemporalCreateEntryProps, TemporalCreateInvocation };

export function TemporalCreateEntry(props: TemporalCreateEntryProps) {
  const [runtime] = useState(
    () => props.runtime ?? createB03TemporalCreateRuntime(),
  );
  return <BaseTemporalCreateEntry {...props} runtime={runtime} />;
}
