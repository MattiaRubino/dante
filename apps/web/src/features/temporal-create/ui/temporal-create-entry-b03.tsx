import { useState } from 'react';

import { createB06TemporalCreateRuntime } from '../application/temporal-create-b06-runtime';
import {
  TemporalCreateEntry as BaseTemporalCreateEntry,
  type TemporalCreateEntryProps,
  type TemporalCreateInvocation,
} from './temporal-create-entry';

export type { TemporalCreateEntryProps, TemporalCreateInvocation };

export function TemporalCreateEntry(props: TemporalCreateEntryProps) {
  const [runtime] = useState(
    () => props.runtime ?? createB06TemporalCreateRuntime(),
  );
  return <BaseTemporalCreateEntry {...props} runtime={runtime} />;
}
