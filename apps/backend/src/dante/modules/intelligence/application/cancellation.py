"""Provider-neutral request cancellation primitive for ModelAccess callers."""

from __future__ import annotations

import asyncio


class ModelCancellationSignal:
    """One request-local cancellation signal shared across application-owned async work."""

    __slots__ = ("_event",)

    def __init__(self) -> None:
        self._event = asyncio.Event()

    @property
    def cancelled(self) -> bool:
        return self._event.is_set()

    def cancel(self) -> bool:
        """Request cancellation once; return False when it had already been requested."""
        if self._event.is_set():
            return False
        self._event.set()
        return True

    async def wait(self) -> None:
        """Wait until cancellation is requested."""
        await self._event.wait()
