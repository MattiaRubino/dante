"""Typed, immutable bootstrap configuration for the DANTE backend."""

from enum import StrEnum
from typing import Annotated, Self

from pydantic import StringConstraints, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

IdentityValue = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]


class Environment(StrEnum):
    """Closed set of DANTE runtime/promotion environments."""

    LOCAL = "local"
    DEV = "dev"
    UAT = "uat"
    PROD = "prod"


class Settings(BaseSettings):
    """Validated process configuration constructed once during application bootstrap."""

    model_config = SettingsConfigDict(
        env_prefix="DANTE_",
        extra="forbid",
        frozen=True,
    )

    env: Environment
    release_sha: IdentityValue
    build_id: IdentityValue
    debug: bool = False

    @model_validator(mode="after")
    def validate_environment_safety(self) -> Self:
        """Reject environment combinations that can silently weaken deployment safety."""
        if self.env is Environment.PROD and self.debug:
            raise ValueError("DANTE_DEBUG must be false when DANTE_ENV=prod")

        if self.env is not Environment.LOCAL:
            if self.release_sha.casefold() == "local":
                raise ValueError("DANTE_RELEASE_SHA=local is allowed only when DANTE_ENV=local")
            if self.build_id.casefold() == "local":
                raise ValueError("DANTE_BUILD_ID=local is allowed only when DANTE_ENV=local")

        return self
