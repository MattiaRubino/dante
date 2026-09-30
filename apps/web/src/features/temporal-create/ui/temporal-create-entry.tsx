import type { PlainDate } from '@dante/time';
import {
  useCallback,
  useEffect,
  useRef,
  useState,
} from 'react';
import { createPortal } from 'react-dom';
import { useTranslation } from 'react-i18next';

import type { TemporalValidationIssue } from '../../temporal';
import {
  createLocalTemporalCreateRuntime,
  type TemporalCreateAppliedEffect,
  type TemporalCreatePreparedOperation,
  type TemporalCreateRuntime,
} from '../application/temporal-create-runtime';
import {
  applyTemporalCreateFieldSeed,
  type TemporalCreateFieldSeed,
} from '../application/temporal-create-seed';
import {
  temporalCreateTimelinePreviewFromFields,
  type TemporalCreateTimelineProjection,
} from '../application/temporal-create-projection';
import {
  continueTemporalCreateEditing,
  createTemporalCreateFields,
  createTemporalCreateSession,
  discardTemporalCreateSession,
  requestTemporalCreateClose,
  setTemporalCreateSurface,
  updateTemporalCreateFields,
  type TemporalCreateSession,
  type TemporalCreateSurface,
} from '../model/temporal-create-session';
import {
  TemporalCreateComposer,
  type TemporalCreateContextOption,
} from './temporal-create-composer';

import './temporal-create.css';
import './temporal-create-u1.css';
import './temporal-create-u1-polish.css';

// remainder unchanged
