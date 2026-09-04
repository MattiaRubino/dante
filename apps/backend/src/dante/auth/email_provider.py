"""Compatibility imports for shared Email Platform provider adapters."""

from dante.platform.email import provider as _provider
from dante.platform.email.provider import SesEmailProvider, SmtpEmailProvider

# Retain the module object for existing focused tests that monkeypatch boto3.Session through
# this historical import path. Production implementation lives in dante.platform.email.provider.
boto3 = _provider.boto3

__all__ = ["SesEmailProvider", "SmtpEmailProvider"]
