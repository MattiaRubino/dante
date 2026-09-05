"""Compatibility imports for shared Email Platform worker orchestration."""

from dante.platform.email.worker import EmailDeliveryWorkerPool, EmailRendererPort

__all__ = ["EmailDeliveryWorkerPool", "EmailRendererPort"]
