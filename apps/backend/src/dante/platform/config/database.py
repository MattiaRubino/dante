"""Typed database configuration shared by runtime and migration boundaries."""

from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field, SecretStr, StringConstraints
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import URL

DatabaseText = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]
DatabasePort = Annotated[int, Field(ge=1, le=65535)]
ConnectTimeoutSeconds = Annotated[int, Field(ge=1, le=60)]
PoolSize = Annotated[int, Field(ge=1, le=100)]
PoolOverflow = Annotated[int, Field(ge=0, le=100)]
PoolTimeoutSeconds = Annotated[float, Field(gt=0, le=120)]
ReadinessTimeoutSeconds = Annotated[float, Field(gt=0, le=30)]
RuntimeDatabaseUser = Literal["dante_runtime"]


class DatabaseSettings(BaseModel):
    """Runtime-only PostgreSQL configuration embedded in process settings."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    host: DatabaseText
    port: DatabasePort = 5432
    name: DatabaseText
    user: RuntimeDatabaseUser
    password: SecretStr
    connect_timeout_seconds: ConnectTimeoutSeconds = 5
    pool_size: PoolSize = 5
    max_overflow: PoolOverflow = 10
    pool_timeout_seconds: PoolTimeoutSeconds = 30.0
    readiness_timeout_seconds: ReadinessTimeoutSeconds = 2.0

    def sqlalchemy_url(self) -> URL:
        """Build a driver URL without manual credential escaping."""
        return URL.create(
            "postgresql+psycopg",
            username=self.user,
            password=self.password.get_secret_value(),
            host=self.host,
            port=self.port,
            database=self.name,
        )


class MigrationDatabaseSettings(BaseSettings):
    """Credential-isolated settings consumed only by Alembic execution."""

    model_config = SettingsConfigDict(frozen=True, extra="ignore", validate_by_name=True)

    host: DatabaseText = Field(validation_alias="DANTE_DATABASE__HOST")
    port: DatabasePort = Field(default=5432, validation_alias="DANTE_DATABASE__PORT")
    name: DatabaseText = Field(validation_alias="DANTE_DATABASE__NAME")
    password: SecretStr = Field(validation_alias="DANTE_MIGRATOR__PASSWORD")
    connect_timeout_seconds: ConnectTimeoutSeconds = Field(
        default=5,
        validation_alias="DANTE_DATABASE__CONNECT_TIMEOUT_SECONDS",
    )

    def sqlalchemy_url(self) -> URL:
        """Build the dedicated migrator URL without requiring runtime credentials."""
        return URL.create(
            "postgresql+psycopg",
            username="dante_migrator",
            password=self.password.get_secret_value(),
            host=self.host,
            port=self.port,
            database=self.name,
        )
