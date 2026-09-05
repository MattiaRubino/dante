"""Azure OpenAI Responses candidate adapter for DANTE direct evals.

Evaluation-only. This module is not a DANTE production ProviderBinding and must
not be imported by production runtime code.
"""

from __future__ import annotations

import time
from typing import Any, Final
from urllib.parse import urlparse

import openai

from azure_candidate_config import AzureCandidateConfig
from dante_eval_core import CandidateResult, EvalFixture
from openai import AsyncOpenAI
from openai.types.responses.response import Response

_MAX_RETRIES: Final = 0


def _structured_text_config(fixture: EvalFixture) -> dict[str, Any]:
    if fixture.response_schema is None:
        raise ValueError("structured eval fixture requires response_schema")
    return {
        "format": {
            "type": "json_schema",
            "name": f"dante_eval_{fixture.fixture_id.replace('-', '_')}",
            "schema": fixture.response_schema,
            "strict": True,
        }
    }


def _response_ids(response: Response) -> tuple[str | None, str | None]:
    return response._request_id, response.id


class AzureOpenAIResponsesCandidate:
    candidate_id = "azure-openai-responses"

    def __init__(self, config: AzureCandidateConfig) -> None:
        self._config = config
        self._client = AsyncOpenAI(
            api_key=config.api_key,
            base_url=config.endpoint,
            max_retries=_MAX_RETRIES,
        )

    @property
    def identity(self) -> dict[str, str]:
        parsed = urlparse(self._config.endpoint)
        return {
            "candidate_id": self.candidate_id,
            "serving_platform": "azure-openai",
            "protocol_family": "responses",
            "deployment": self._config.deployment,
            "endpoint_host": parsed.netloc,
        }

    async def invoke(self, fixture: EvalFixture, *, timeout_seconds: float) -> CandidateResult:
        if not fixture.requires_model:
            raise ValueError("candidate must not be invoked for model-avoidance fixture")

        started = time.perf_counter()
        try:
            response = await self._client.responses.create(
                model=self._config.deployment,
                input=fixture.input_text,
                instructions=fixture.instructions,
                max_output_tokens=fixture.max_output_tokens,
                store=False,
                stream=False,
                background=False,
                tools=[],
                text=_structured_text_config(fixture),
                timeout=timeout_seconds,
            )
        except openai.APIError as exc:
            latency_ms = int((time.perf_counter() - started) * 1000)
            request_id = getattr(exc, "request_id", None)
            error_code = None
            status_code = getattr(exc, "status_code", None)
            if status_code is not None:
                error_code = f"http_{status_code}"
            return CandidateResult(
                output_text=None,
                input_tokens=None,
                output_tokens=None,
                total_tokens=None,
                provider_request_id=request_id,
                provider_response_id=None,
                latency_ms=latency_ms,
                provider_status=None,
                error_class=type(exc).__name__,
                error_code=error_code,
            )

        latency_ms = int((time.perf_counter() - started) * 1000)
        usage = response.usage
        request_id, response_id = _response_ids(response)
        return CandidateResult(
            output_text=response.output_text or None,
            input_tokens=usage.input_tokens if usage is not None else None,
            output_tokens=usage.output_tokens if usage is not None else None,
            total_tokens=usage.total_tokens if usage is not None else None,
            provider_request_id=request_id,
            provider_response_id=response_id,
            latency_ms=latency_ms,
            provider_status=response.status,
        )

    async def close(self) -> None:
        await self._client.close()
