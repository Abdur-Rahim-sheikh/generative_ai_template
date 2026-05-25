from fastapi import APIRouter, Cookie, Depends, HTTPException, Response, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm

from ...adapters import JwtManager
from ...dependencies.database_services import (
    get_jwt_manager,
    get_user_service,
    get_user_session_service,
)
from ...services import UserService, UserSessionService

router = APIRouter()


@router.post("/login")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    user_service: UserService = Depends(get_user_service),
    user_session_service: UserSessionService = Depends(get_user_session_service),
    jwt_manager: JwtManager = Depends(get_jwt_manager),
):
    user = await user_service.get_user_by_email(form_data.username)
    if (
        not user
        or not user.is_active
        or not user_service.hasher.verify(form_data.password, user.hashed_password)
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password or inactive user",
            headers={"WWW-Authenticate": "Bearer"},
        )

    refresh_token = await user_session_service.create_user_session(user.id)

    # app_logger.info(f"User {user.email=} {user.wallet.id=} logged in successfully")
    access_token = jwt_manager.encode(
        {"sub": str(user.id), "wallet_id": str(user.wallet.id)}
    )
    response = JSONResponse(
        content={"access_token": access_token, "token_type": "bearer"}
    )
    response.set_cookie(
        key="refresh_token",
        value=str(refresh_token.id),
        httponly=True,
        # secure=True, # not yet https
        samesite="strict",
    )
    return response


@router.post("/logout")
async def logout(
    refresh_token: str | None = Cookie(default=None),
    user_session_service: UserSessionService = Depends(get_user_session_service),
):
    if refresh_token:
        await user_session_service.delete_user_session(refresh_token)
    response = Response(status_code=status.HTTP_204_NO_CONTENT)
    response.delete_cookie(key="refresh_token")
    return response


@router.post("/refresh")
async def refresh_jwt_token(
    refresh_token: str | None = Cookie(default=None),
    user_session_service: UserSessionService = Depends(get_user_session_service),
    user_service: UserService = Depends(get_user_service),
    jwt_manager: JwtManager = Depends(get_jwt_manager),
):
    session = await user_session_service.get_user_session(refresh_token)
    if not session:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = await user_service.get_user(session.user_id)

    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found or inactive"
        )

    access_token = jwt_manager.encode(
        {"sub": str(user.id), "wallet_id": str(user.wallet.id)}
    )
    response = JSONResponse(
        content={"access_token": access_token, "token_type": "bearer"}
    )
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        # secure=True, # not yet https
        samesite="strict",
    )
    return response
