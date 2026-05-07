from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from ...dependencies.services import get_user_service
from ...schemas.user import CreateUserRequest
from ...domain import User
from ...config import app_logger

router = APIRouter()


@router.post("/create-user")
async def create_user(user: CreateUserRequest, user_service=Depends(get_user_service)):
    app_logger.debug(f"Creating user: {user}")
    user = User(
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        hashed_password=user.hashed_password,
    )

    await user_service.create_user(user)
    return JSONResponse(
        content={"message": "User created successfully"},
        status_code=status.HTTP_201_CREATED,
    )
