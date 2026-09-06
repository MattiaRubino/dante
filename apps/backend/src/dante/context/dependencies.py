"""FastAPI dependency for authenticated DANTE application context."""

from typing import cast

from fastapi import Depends, Request

from dante.auth.contracts import AuthServiceUnavailableError
from dante.auth.dependencies import get_auth_service, single_header_value
from dante.auth.service import AuthService
from dante.auth.sessions import AmbiguousSessionCookieError, session_cookie_value
from dante.context.contracts import DanteContext
from dante.context.service import DanteContextService
from dante.platform.database.runtime import DatabaseRuntime
from dante.platform.http.problem import ProblemError
from dante.platform.time import InvalidTimeZoneError, MissingDeviceTimeZoneError

DANTE_TIME_ZONE_HEADER_NAME = "X-Dante-Time-Zone"


def get_dante_context_service(request: Request) -> DanteContextService:
    """Resolve the application-context service from the process-scoped database runtime."""
    database_runtime = cast(DatabaseRuntime, request.app.state.database_runtime)
    return DanteContextService(database_runtime.session_factory)


async def require_dante_context(
    request: Request,
    auth_service: AuthService = Depends(get_auth_service),
    context_service: DanteContextService = Depends(get_dante_context_service),
) -> DanteContext:
    """Require an admitted AuthSession and resolve its DANTE-facing application context."""
    try:
        cookie_value = session_cookie_value(list(request.scope.get("headers", [])))
    except AmbiguousSessionCookieError as exc:
        raise _authentication_required() from exc

    try:
        admitted = await auth_service.admit_session(cookie_value)
    except AuthServiceUnavailableError as exc:
        raise ProblemError(
            status=503,
            code="service.unavailable",
            category="service",
            title="Service unavailable",
            detail="Authentication is temporarily unavailable.",
            retryable=exc.retryable,
        ) from exc

    if admitted is None:
        raise _authentication_required()

    device_zone_id = single_header_value(request.scope, DANTE_TIME_ZONE_HEADER_NAME)
    try:
        return await context_service.resolve(
            principal=admitted.principal,
            device_zone_id=device_zone_id,
        )
    except MissingDeviceTimeZoneError as exc:
        raise ProblemError(
            status=400,
            code="context.device_timezone_required",
            category="validation",
            title="Device timezone required",
            detail="This DANTE context follows the device timezone and requires a named IANA timezone.",
        ) from exc
    except InvalidTimeZoneError as exc:
        raise ProblemError(
            status=400,
            code="context.invalid_timezone",
            category="validation",
            title="Invalid timezone",
            detail="The supplied timezone is not an accepted named IANA timezone.",
        ) from exc


def _authentication_required() -> ProblemError:
    return ProblemError(
        status=401,
        code="auth.authentication_required",
        category="authentication",
        title="Authentication required",
        detail="A valid authenticated session is required.",
    )
