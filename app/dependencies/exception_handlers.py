from fastapi import Request
from ..domain.exceptions import DomainException
from fastapi.responses import JSONResponse


async def global_domain_exception_handler(request: Request, exc: DomainException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "status": "error",
            "message": exc.message,
            "error_type": exc.__class__.__name__,
        },
    )
