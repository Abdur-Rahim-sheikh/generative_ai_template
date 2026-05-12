from fastapi import Request, status
from ..domain.exceptions import (
    DomainException,
    NotFound,
    AlreadyExists,
    InsufficientFunds,
)
from fastapi.responses import JSONResponse

handlers = {
    DomainException: status.HTTP_400_BAD_REQUEST,
    NotFound: status.HTTP_404_NOT_FOUND,
    AlreadyExists: status.HTTP_409_CONFLICT,
    InsufficientFunds: status.HTTP_402_PAYMENT_REQUIRED,
}


async def global_domain_exception_handler(request: Request, exc: DomainException):
    return JSONResponse(
        status_code=handlers.get(exc, DomainException),
        content={
            "status": "error",
            "message": exc.message,
            "error_type": exc.__class__.__name__,
        },
    )
