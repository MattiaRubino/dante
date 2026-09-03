"""Minimized runtime-evidence emission port for DANTE Intelligence."""

from typing import Protocol

from dante.modules.intelligence.contracts.evidence import RuntimeEvidenceEvent


class RuntimeEvidencePort(Protocol):
    """Emit minimized runtime evidence; this port is not an audit or canonical-data owner."""

    async def emit(self, event: RuntimeEvidenceEvent) -> None: ...
