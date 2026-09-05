import { useEffect, useRef } from 'react';
import { useTranslation } from 'react-i18next';

import type { WorldFocusSurfaceRendererProps } from './world-focus-surface-registry';
import { useWorldFocusDanteProposal } from './world-focus-dante-proposal-context';

export {
  WORLD_FOCUS_DANTE_CONFIRMATION_INSTANCE_ID,
  WORLD_FOCUS_DANTE_CONFIRMATION_KIND,
  WORLD_FOCUS_DANTE_PROPOSAL_INSTANCE_ID,
  WORLD_FOCUS_DANTE_PROPOSAL_KIND,
  WORLD_FOCUS_DANTE_RECEIPT_INSTANCE_ID,
  WORLD_FOCUS_DANTE_RECEIPT_KIND,
} from './world-focus-dante-proposal-context';

function restoreInsightProposalInvoker(): void {
  queueMicrotask(() => {
    queueMicrotask(() => {
      document
        .querySelector<HTMLButtonElement>(
          '[data-world-focus-dante-proposal-invoker="true"]',
        )
        ?.focus({ preventScroll: true });
    });
  });
}

function restoreProposalFocus(): void {
  queueMicrotask(() => {
    queueMicrotask(() => {
      document
        .querySelector<HTMLButtonElement>(
          '[data-world-focus-dante-proposal-close="true"]',
        )
        ?.focus({ preventScroll: true });
    });
  });
}

export function WorldFocusDanteProposal({
  isCurrentGeneration,
  onRequestClose,
}: WorldFocusSurfaceRendererProps) {
  const { t } = useTranslation('common');
  const { proposal, receipt, requestConfirmation } =
    useWorldFocusDanteProposal();
  const closeRef = useRef<HTMLButtonElement | null>(null);
  const reviewRef = useRef<HTMLButtonElement | null>(null);

  useEffect(() => {
    queueMicrotask(() => {
      if (receipt === null) {
        reviewRef.current?.focus({ preventScroll: true });
        return;
      }
      closeRef.current?.focus({ preventScroll: true });
    });
  }, [receipt]);

  const handleClose = () => {
    onRequestClose();
    restoreInsightProposalInvoker();
  };

  if (proposal === null || !isCurrentGeneration) {
    return (
      <section
        className="world-focus-dante-proposal world-focus-dante-governed-unavailable"
        data-world-focus-dante-surface="proposal"
        role="dialog"
        aria-modal="false"
        aria-labelledby="world-focus-dante-proposal-unavailable-title"
      >
        <header className="world-focus-dante-governed-header">
          <h2 id="world-focus-dante-proposal-unavailable-title">
            {t(($) => $.common.worldFocus.dante.proposal.title)}
          </h2>
          <button
            ref={closeRef}
            className="world-focus-dante-governed-close"
            data-world-focus-dante-proposal-close="true"
            type="button"
            aria-label={t(($) => $.common.worldFocus.dante.proposal.close)}
            onClick={handleClose}
          >
            <span aria-hidden="true">×</span>
          </button>
        </header>
        <p className="world-focus-dante-governed-state" role="status">
          {t(($) => $.common.worldFocus.dante.proposal.unavailable)}
        </p>
      </section>
    );
  }

  const referenceCount = 1 + proposal.basisReferences.supporting.length;

  return (
    <section
      className="world-focus-dante-proposal"
      data-world-focus-dante-surface="proposal"
      data-world-focus-dante-decision-required="explicit-confirmation"
      role="dialog"
      aria-modal="false"
      aria-labelledby="world-focus-dante-proposal-title"
    >
      <header className="world-focus-dante-governed-header">
        <div>
          <span className="world-focus-dante-governed-kicker">
            {t(($) => $.common.worldFocus.dante.proposal.kicker)}
          </span>
          <h2 id="world-focus-dante-proposal-title">{proposal.title}</h2>
        </div>
        <button
          ref={closeRef}
          className="world-focus-dante-governed-close"
          data-world-focus-dante-proposal-close="true"
          type="button"
          aria-label={t(($) => $.common.worldFocus.dante.proposal.close)}
          onClick={handleClose}
        >
          <span aria-hidden="true">×</span>
        </button>
      </header>

      <div className="world-focus-dante-governed-body">
        <div className="world-focus-dante-governed-target">
          <span>{t(($) => $.common.worldFocus.dante.proposal.target)}</span>
          <strong>{proposal.targetLabel}</strong>
        </div>
        <p className="world-focus-dante-governed-change">
          {proposal.changeSummary}
        </p>
        <p className="world-focus-dante-governed-meta">
          {t(($) => $.common.worldFocus.dante.proposal.basis, {
            count: referenceCount,
          })}
        </p>
        <p className="world-focus-dante-governed-requirement">
          {t(($) => $.common.worldFocus.dante.proposal.decisionRequired)}
        </p>
        <p className="world-focus-dante-governed-truth-note">
          {t(($) => $.common.worldFocus.dante.proposal.noEffect)}{' '}
          {t(($) => $.common.worldFocus.dante.proposal.truthNote)}
        </p>

        {receipt === null ? (
          <button
            ref={reviewRef}
            className="world-focus-dante-governed-primary"
            type="button"
            onClick={requestConfirmation}
          >
            {t(($) => $.common.worldFocus.dante.proposal.reviewConfirmation)}
          </button>
        ) : (
          <p className="world-focus-dante-governed-state" role="status">
            {receipt.decision === 'confirmed'
              ? t(
                  ($) =>
                    $.common.worldFocus.dante.proposal.decisionRecorded.confirmed,
                )
              : t(
                  ($) =>
                    $.common.worldFocus.dante.proposal.decisionRecorded.declined,
                )}
          </p>
        )}
      </div>
    </section>
  );
}

export function WorldFocusDanteConfirmation({
  isCurrentGeneration,
}: WorldFocusSurfaceRendererProps) {
  const { t } = useTranslation('common');
  const { proposal, recordDecision } = useWorldFocusDanteProposal();
  const declineRef = useRef<HTMLButtonElement | null>(null);

  useEffect(() => {
    queueMicrotask(() => declineRef.current?.focus({ preventScroll: true }));
  }, []);

  if (proposal === null || !isCurrentGeneration) {
    return null;
  }

  return (
    <section
      className="world-focus-dante-confirmation"
      data-world-focus-dante-surface="confirmation"
      data-world-focus-dante-confirmation-required="true"
      role="alertdialog"
      aria-modal="false"
      aria-labelledby="world-focus-dante-confirmation-title"
      aria-describedby="world-focus-dante-confirmation-description"
    >
      <header className="world-focus-dante-governed-header">
        <div>
          <span className="world-focus-dante-governed-kicker">
            {t(($) => $.common.worldFocus.dante.proposal.confirmation.kicker)}
          </span>
          <h2 id="world-focus-dante-confirmation-title">
            {t(($) => $.common.worldFocus.dante.proposal.confirmation.title)}
          </h2>
        </div>
      </header>

      <div className="world-focus-dante-governed-body">
        <div className="world-focus-dante-governed-target">
          <span>{t(($) => $.common.worldFocus.dante.proposal.target)}</span>
          <strong>{proposal.targetLabel}</strong>
        </div>
        <p className="world-focus-dante-governed-change">
          {proposal.changeSummary}
        </p>
        <p
          id="world-focus-dante-confirmation-description"
          className="world-focus-dante-governed-requirement"
        >
          {t(($) => $.common.worldFocus.dante.proposal.confirmation.description)}
        </p>
        <p className="world-focus-dante-governed-truth-note">
          {t(($) => $.common.worldFocus.dante.proposal.noEffect)}
        </p>

        <div className="world-focus-dante-confirmation-actions">
          <button
            ref={declineRef}
            className="world-focus-dante-governed-secondary"
            type="button"
            onClick={() => recordDecision('declined')}
          >
            {t(($) => $.common.worldFocus.dante.proposal.confirmation.decline)}
          </button>
          <button
            className="world-focus-dante-governed-primary"
            type="button"
            onClick={() => recordDecision('confirmed')}
          >
            {t(($) => $.common.worldFocus.dante.proposal.confirmation.confirm)}
          </button>
        </div>
      </div>
    </section>
  );
}

export function WorldFocusDanteReceipt({
  isCurrentGeneration,
  onRequestClose,
}: WorldFocusSurfaceRendererProps) {
  const { t } = useTranslation('common');
  const { proposal, receipt } = useWorldFocusDanteProposal();
  const closeRef = useRef<HTMLButtonElement | null>(null);

  useEffect(() => {
    queueMicrotask(() => closeRef.current?.focus({ preventScroll: true }));
  }, []);

  const handleClose = () => {
    onRequestClose();
    restoreProposalFocus();
  };

  if (proposal === null || receipt === null || !isCurrentGeneration) {
    return (
      <section
        className="world-focus-dante-receipt world-focus-dante-governed-unavailable"
        data-world-focus-dante-surface="receipt"
        role="dialog"
        aria-modal="false"
        aria-labelledby="world-focus-dante-receipt-unavailable-title"
      >
        <header className="world-focus-dante-governed-header">
          <h2 id="world-focus-dante-receipt-unavailable-title">
            {t(($) => $.common.worldFocus.dante.proposal.receipt.title)}
          </h2>
          <button
            ref={closeRef}
            className="world-focus-dante-governed-close"
            type="button"
            aria-label={t(($) => $.common.worldFocus.dante.proposal.receipt.close)}
            onClick={handleClose}
          >
            <span aria-hidden="true">×</span>
          </button>
        </header>
        <p className="world-focus-dante-governed-state" role="status">
          {t(($) => $.common.worldFocus.dante.proposal.receipt.unavailable)}
        </p>
      </section>
    );
  }

  return (
    <section
      className="world-focus-dante-receipt"
      data-world-focus-dante-surface="receipt"
      data-world-focus-dante-decision={receipt.decision}
      data-world-focus-dante-effect-execution="not-executed"
      role="dialog"
      aria-modal="false"
      aria-labelledby="world-focus-dante-receipt-title"
    >
      <header className="world-focus-dante-governed-header">
        <div>
          <span className="world-focus-dante-governed-kicker">
            {t(($) => $.common.worldFocus.dante.proposal.receipt.kicker)}
          </span>
          <h2 id="world-focus-dante-receipt-title">
            {t(($) => $.common.worldFocus.dante.proposal.receipt.title)}
          </h2>
        </div>
        <button
          ref={closeRef}
          className="world-focus-dante-governed-close"
          type="button"
          aria-label={t(($) => $.common.worldFocus.dante.proposal.receipt.close)}
          onClick={handleClose}
        >
          <span aria-hidden="true">×</span>
        </button>
      </header>

      <div className="world-focus-dante-governed-body">
        <p className="world-focus-dante-receipt-decision">
          {receipt.decision === 'confirmed'
            ? t(
                ($) =>
                  $.common.worldFocus.dante.proposal.receipt.decisions.confirmed,
              )
            : t(
                ($) =>
                  $.common.worldFocus.dante.proposal.receipt.decisions.declined,
              )}
        </p>
        <p className="world-focus-dante-governed-change">
          {proposal.changeSummary}
        </p>
        <p className="world-focus-dante-governed-requirement">
          {t(($) => $.common.worldFocus.dante.proposal.noEffect)}
        </p>
        <p className="world-focus-dante-governed-truth-note">
          {t(($) => $.common.worldFocus.dante.proposal.receipt.canonicalNote)}
        </p>
      </div>
    </section>
  );
}
