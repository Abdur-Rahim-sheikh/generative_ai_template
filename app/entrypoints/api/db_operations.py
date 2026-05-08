from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from ...dependencies.database_services import get_user_service
from ...schemas.user import CreateUserRequest

router = APIRouter()


@router.post("/create-user")
async def create_user(user: CreateUserRequest, user_service=Depends(get_user_service)):
    await user_service.create_user(user)
    return JSONResponse(
        content={"message": "User created successfully"},
        status_code=status.HTTP_201_CREATED,
    )
