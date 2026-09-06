"""Authenticated DANTE application-context boundary."""

from .contracts import DanteContext
from .service import DanteContextService

__all__ = ["DanteContext", "DanteContextService"]
