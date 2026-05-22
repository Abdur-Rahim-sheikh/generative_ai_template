from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from ...services import UserService
from ...dependencies.database_services import get_user_service
from typing import Annotated

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


@router.post("/login")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    user_service: UserService = Depends(get_user_service),
):
    user = await user_service.get_user_by_email(form_data.username)
    if not user or not user_service.security.verify_password(
        form_data.password, user.hashed_password
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = user_service.security.encode_access_token({"sub": str(user.id)})
    return JSONResponse(content={"access_token": access_token, "token_type": "bearer"})
