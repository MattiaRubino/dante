"""Temporal Timeline application boundary."""

from __future__ import annotations

from dante.context.contracts import DanteContext
from dante.modules.temporal.contracts import EmptyTimelineWindow, TimelineWindowQuery


class TemporalTimelineApplication:
    """Govern Timeline reads without inventing persistence before a family is activated."""

    def read_window(
        self,
        *,
        query: TimelineWindowQuery,
        context: DanteContext,
    ) -> EmptyTimelineWindow:
        """Return the truthful B00 empty projection for one authenticated DANTE context.

        B00 deliberately establishes the governed query boundary before Activity/Event/Schedule
        product projection persistence exists. Returning an explicit empty result is truthful;
        manufacturing prototype cards or querying unrelated owner shells would not be.
        """
        return EmptyTimelineWindow(
            start_date=query.start_date,
            end_date_exclusive=query.end_date_exclusive,
            effective_zone_id=context.effective_zone_id,
            self_person_ref=context.self_person_ref,
        )
