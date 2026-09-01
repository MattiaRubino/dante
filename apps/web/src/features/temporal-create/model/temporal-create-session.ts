import {
  createTemporalDraft,
  updateTemporalDraft,
  type TemporalDraft,
} from '../../temporal';

export type TemporalCreateFields = Readonly<{
  title: string;
}>;

export type TemporalCreateCloseDecision = 'none' | 'confirm-discard';

export type TemporalCreateSession = Readonly<{
  draft: TemporalDraft<TemporalCreateFields>;
  closeDecision: TemporalCreateCloseDecision;
}>;

export type TemporalCreateCloseRequest = Readonly<{
  session: TemporalCreateSession;
  shouldClose: boolean;
}>;

const EMPTY_TEMPORAL_CREATE_FIELDS: TemporalCreateFields = Object.freeze({
  title: '',
});

function temporalCreateFieldsEqual(
  left: TemporalCreateFields,
  right: TemporalCreateFields,
): boolean {
  return left.title === right.title;
}

function freezeSession(
  draft: TemporalDraft<TemporalCreateFields>,
  closeDecision: TemporalCreateCloseDecision,
): TemporalCreateSession {
  return Object.freeze({ draft, closeDecision });
}

export function createTemporalCreateSession(): TemporalCreateSession {
  return freezeSession(createTemporalDraft(EMPTY_TEMPORAL_CREATE_FIELDS), 'none');
}

export function updateTemporalCreateTitle(
  session: TemporalCreateSession,
  title: string,
): TemporalCreateSession {
  const nextFields = Object.freeze({
    ...session.draft.current,
    title,
  });

  return freezeSession(
    updateTemporalDraft(
      session.draft,
      nextFields,
      temporalCreateFieldsEqual,
    ),
    'none',
  );
}

export function requestTemporalCreateClose(
  session: TemporalCreateSession,
): TemporalCreateCloseRequest {
  if (!session.draft.dirty) {
    return Object.freeze({ session, shouldClose: true });
  }

  return Object.freeze({
    session: freezeSession(session.draft, 'confirm-discard'),
    shouldClose: false,
  });
}

export function continueTemporalCreateEditing(
  session: TemporalCreateSession,
): TemporalCreateSession {
  return freezeSession(session.draft, 'none');
}

export function discardTemporalCreateSession(): TemporalCreateSession {
  return createTemporalCreateSession();
}
