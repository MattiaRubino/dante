"""FastAPI dependencies for authenticated DANTE application context."""

from typing import Annotated, cast

from fastapi import Depends, Request

from dante.auth.contracts import AdmittedSession, AuthServiceUnavailableError
from dante.auth.dependencies import get_auth_service, single_header_value
from dante.auth.service import AuthService
from dante.auth.sessions import (
    CSRF_HEADER_NAME,
    AmbiguousSessionCookieError,
    csrf_token_matches,
    session_cookie_value,
)
from dante.context.contracts import DanteContext, DanteContextIntegrityError
from dante.context.service import DanteContextService
from dante.platform.database.runtime import DatabaseRuntime
from dante.platform.http.problem import ProblemError
from dante.platform.time import InvalidTimeZoneError, MissingDeviceTimeZoneError

DANTE_TIME_ZONE_HEADER_NAME = "X-Dante-Time-Zone"

AuthServiceDependency = Annotated[AuthService, Depends(get_auth_service)]


def get_dante_context_service(request: Request) -> DanteContextService:
    """Resolve the application-context service from the process-scoped database runtime."""
    database_runtime = cast(DatabaseRuntime, request.app.state.database_runtime)
    return DanteContextService(database_runtime.session_factory)


DanteContextServiceDependency = Annotated[
    DanteContextService,
    Depends(get_dante_context_service),
]


async def _require_admitted_session(
    request: Request,
    auth_service: AuthService,
) -> AdmittedSession:
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
    return admitted


async def _resolve_dante_context(
    *,
    request: Request,
    admitted: AdmittedSession,
    context_service: DanteContextService,
) -> DanteContext:
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
            detail=(
                "This DANTE context follows the device timezone and requires a named IANA timezone."
            ),
        ) from exc
    except InvalidTimeZoneError as exc:
        raise ProblemError(
            status=400,
            code="context.invalid_timezone",
            category="validation",
            title="Invalid timezone",
            detail="The supplied timezone is not an accepted named IANA timezone.",
        ) from exc
    except DanteContextIntegrityError as exc:
        raise ProblemError(
            status=500,
            code="context.integrity_error",
            category="internal",
            title="DANTE context unavailable",
            detail="The authenticated DANTE context could not be resolved safely.",
            retryable=False,
        ) from exc


async def require_dante_context(
    request: Request,
    auth_service: AuthServiceDependency,
    context_service: DanteContextServiceDependency,
) -> DanteContext:
    """Require an admitted AuthSession and resolve its DANTE-facing application context."""
    admitted = await _require_admitted_session(request, auth_service)
    return await _resolve_dante_context(
        request=request,
        admitted=admitted,
        context_service=context_service,
    )


async def require_mutating_dante_context(
    request: Request,
    auth_service: AuthServiceDependency,
    context_service: DanteContextServiceDependency,
) -> DanteContext:
    """Require AuthSession + CSRF evidence before resolving a mutating DANTE context."""
    admitted = await _require_admitted_session(request, auth_service)
    if not csrf_token_matches(
        admitted.csrf_token,
        single_header_value(request.scope, CSRF_HEADER_NAME),
    ):
        raise ProblemError(
            status=403,
            code="security.csrf_failed",
            category="security",
            title="Request rejected",
            detail="The request could not satisfy the browser security policy.",
            retryable=False,
        )

    return await _resolve_dante_context(
        request=request,
        admitted=admitted,
        context_service=context_service,
    )


def _authentication_required() -> ProblemError:
    return ProblemError(
        status=401,
        code="auth.authentication_required",
        category="authentication",
        title="Authentication required",
        detail="A valid authenticated session is required.",
    )
