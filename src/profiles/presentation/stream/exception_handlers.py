from faststream import ExceptionMiddleware

from profiles.application.common.application_error import ApplicationError


def application_error_handler(exc: ApplicationError) -> str:
    return f"Exc: {exc.error_type} with message: {exc.message} occured"


def fastream_exception_middleware() -> ExceptionMiddleware:
    return ExceptionMiddleware(
        publish_handlers={ApplicationError: application_error_handler}
    )
