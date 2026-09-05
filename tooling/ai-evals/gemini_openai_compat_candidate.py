"""Google Gemini OpenAI-compat eval candidate for DANTE direct evals.

Evaluation-only. This module is not a DANTE production ProviderBinding and must
not be imported by production runtime code. The OpenAI-compatible transport is
used only to obtain comparable model-candidate evidence without adding a second
SDK dependency to the backend project.
"""

from __future__ import annotations

import time
from typing import Any, Final
from urllib.parse import urlparse

import openai
from openai import AsyncOpenAI

from dante_eval_core import CandidateResult, EvalFixture
from gemini_candidate_config import GeminiCandidateConfig

_BASE_URL: Final = "https://generativelanguage.googleapis.com/v1beta/openai/"
_MAX_RETRIES: Final = 0


def _structured_response_format(fixture: EvalFixture) -> dict[str, Any]:
    assert fixture.response_schema is not None
    return {
        "type": "json_schema",
        "json_schema": {
            "name": f"dante_eval_{fixture.fixture_id.replace('-', '_')}",
            "schema": fixture.response_schema,
            "strict": True,
        },
    }


class GeminiOpenAICompatCandidate:
    candidate_id = "google-gemini-openai-compat"

    def __init__(self, config: GeminiCandidateConfig) -> None:
        self._config = config
        self._client = AsyncOpenAI(
            api_key=config.api_key,
            base_url=_BASE_URL,
            max_retries=_MAX_RETRIES,
        )

    @property
    def identity(self) -> dict[str, str]:
        parsed = urlparse(_BASE_URL)
        return {
            "candidate_id": self.candidate_id,
            "serving_platform": "google-gemini-api",
            "protocol_family": "openai-compatible-chat-completions",
            "model": self._config.model,
            "reasoning_effort": self._config.reasoning_effort,
            "endpoint_host": parsed.netloc,
        }

    async def invoke(self, fixture: EvalFixture, *, timeout_seconds: float) -> CandidateResult:
        if not fixture.requires_model:
            raise ValueError("candidate must not be invoked for model-avoidance fixture")

        started = time.perf_counter()
        try:
            response = await self._client.chat.completions.create(
                model=self._config.model,
                reasoning_effort=self._config.reasoning_effort,
                messages=[
                    {"role": "system", "content": fixture.instructions},
                    {"role": "user", "content": fixture.input_text},
                ],
                response_format=_structured_response_format(fixture),
                max_tokens=fixture.max_output_tokens,
                timeout=timeout_seconds,
            )
        except openai.APIError as exc:
            latency_ms = int((time.perf_counter() - started) * 1000)
            status_code = getattr(exc, "status_code", None)
            error_code = f"http_{status_code}" if status_code is not None else None
            return CandidateResult(
                output_text=None,
                input_tokens=None,
                output_tokens=None,
                total_tokens=None,
                provider_request_id=getattr(exc, "request_id", None),
                provider_response_id=None,
                latency_ms=latency_ms,
                provider_status=None,
                error_class=type(exc).__name__,
                error_code=error_code,
            )

        latency_ms = int((time.perf_counter() - started) * 1000)
        choice = response.choices[0]
        usage = response.usage
        finish_reason = choice.finish_reason
        provider_status = "completed" if finish_reason == "stop" else "incomplete"

        return CandidateResult(
            output_text=choice.message.content or None,
            input_tokens=usage.prompt_tokens if usage is not None else None,
            output_tokens=usage.completion_tokens if usage is not None else None,
            total_tokens=usage.total_tokens if usage is not None else None,
            provider_request_id=getattr(response, "_request_id", None),
            provider_response_id=response.id,
            latency_ms=latency_ms,
            provider_status=provider_status,
        )

    async def close(self) -> None:
        await self._client.close()
