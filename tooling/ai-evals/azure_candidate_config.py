"""Pure Azure OpenAI eval-candidate configuration helpers."""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Final
from urllib.parse import urlparse, urlunparse

_DANTE_ENDPOINT_ENV: Final = "DANTE_EVAL_AZURE_ENDPOINT"
_DANTE_KEY_ENV: Final = "DANTE_EVAL_AZURE_API_KEY"
_DANTE_DEPLOYMENT_ENV: Final = "DANTE_EVAL_AZURE_DEPLOYMENT"

_LEGACY_ENDPOINT_ENV: Final = "DOC_CLASS_AZURE_ENDPOINT"
_LEGACY_KEY_ENV: Final = "DOC_CLASS_API_KEY"
_LEGACY_DEPLOYMENT_ENV: Final = "DOC_CLASS_DEPLOYMENT"


@dataclass(frozen=True, slots=True)
class AzureCandidateConfig:
    endpoint: str
    api_key: str
    deployment: str

    @classmethod
    def from_environment(cls) -> AzureCandidateConfig:
        endpoint = _first_env(_DANTE_ENDPOINT_ENV, _LEGACY_ENDPOINT_ENV)
        api_key = _first_env(_DANTE_KEY_ENV, _LEGACY_KEY_ENV)
        deployment = _first_env(_DANTE_DEPLOYMENT_ENV, _LEGACY_DEPLOYMENT_ENV)

        if (
            endpoint is None
            or not endpoint.strip()
            or api_key is None
            or not api_key.strip()
            or deployment is None
            or not deployment.strip()
        ):
            raise ValueError(
                "missing Azure candidate configuration; set DANTE_EVAL_AZURE_* "
                "or the existing DOC_CLASS_* variables"
            )

        return cls(
            endpoint=normalize_azure_responses_base_url(endpoint),
            api_key=api_key.strip(),
            deployment=deployment.strip(),
        )


def _first_env(primary: str, fallback: str) -> str | None:
    value = os.environ.get(primary)
    if value is not None and value.strip():
        return value
    return os.environ.get(fallback)


def normalize_azure_responses_base_url(endpoint: str) -> str:
    raw = endpoint.strip()
    parsed = urlparse(raw)
    if parsed.scheme != "https":
        raise ValueError("Azure endpoint must use https")
    if not parsed.netloc:
        raise ValueError("Azure endpoint host is missing")

    host = parsed.hostname or ""
    if not host.endswith(".openai.azure.com"):
        raise ValueError("expected an Azure OpenAI *.openai.azure.com endpoint")

    clean_path = parsed.path.rstrip("/")
    if clean_path in {"", "/openai", "/openai/v1"}:
        path = "/openai/v1/"
    else:
        raise ValueError("Azure endpoint must be the resource root or the /openai/v1 endpoint")

    return urlunparse(("https", parsed.netloc, path, "", "", ""))
