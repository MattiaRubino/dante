"""Compatibility imports for shared Email Platform provider adapters."""

import boto3  # type: ignore[import-untyped]

from dante.platform.email.provider import SesEmailProvider, SmtpEmailProvider

# Retain the boto3 module for existing focused tests that monkeypatch boto3.Session through
# this historical import path. Python imports share the same module object, so this still
# affects the production implementation in dante.platform.email.provider.

__all__ = ["SesEmailProvider", "SmtpEmailProvider"]
