"""Pure Google Gemini eval-candidate configuration helpers."""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Final

_DANTE_KEY_ENV: Final = "DANTE_EVAL_GEMINI_API_KEY"
_DANTE_MODEL_ENV: Final = "DANTE_EVAL_GEMINI_MODEL"
_DANTE_REASONING_ENV: Final = "DANTE_EVAL_GEMINI_REASONING_EFFORT"

_DEFAULT_MODEL: Final = "gemini-3.8-flash"
_DEFAULT_REASONING_EFFORT: Final = "low"
_ALLOWED_REASONING_EFFORTS: Final = frozenset({"low", "medium", "high"})


@dataclass(frozen=True, slots=True)
class GeminiCandidateConfig:
    api_key: str
    model: str
    reasoning_effort: str

    @classmethod
    def from_environment(cls) -> "GeminiCandidateConfig":
        api_key = os.environ.get(_DANTE_KEY_ENV)
        if api_key is None or not api_key.strip():
            raise ValueError(
                "missing Gemini candidate configuration; set "
                "DANTE_EVAL_GEMINI_API_KEY"
            )

        model = os.environ.get(_DANTE_MODEL_ENV, _DEFAULT_MODEL).strip()
        if not model:
            raise ValueError("DANTE_EVAL_GEMINI_MODEL cannot be empty")

        reasoning_effort = os.environ.get(
            _DANTE_REASONING_ENV,
            _DEFAULT_REASONING_EFFORT,
        ).strip().lower()
        if reasoning_effort not in _ALLOWED_REASONING_EFFORTS:
            allowed = ", ".join(sorted(_ALLOWED_REASONING_EFFORTS))
            raise ValueError(
                "DANTE_EVAL_GEMINI_REASONING_EFFORT must be one of: " + allowed
            )

        return cls(
            api_key=api_key.strip(),
            model=model,
            reasoning_effort=reasoning_effort,
        )
