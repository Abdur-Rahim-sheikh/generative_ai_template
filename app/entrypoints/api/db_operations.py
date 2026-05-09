from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from ...dependencies.database_services import get_product_service, get_user_service
from ...schemas.product import CreateProductRequest
from ...schemas.user import CreateUserRequest

router = APIRouter()


@router.post("/create-user")
async def create_user(user: CreateUserRequest, user_service=Depends(get_user_service)):
    await user_service.create_user(user)
    return JSONResponse(
        content={"message": "User created successfully"},
        status_code=status.HTTP_201_CREATED,
    )


@router.get("/get-user/{user_id}")
async def get_user(user_id: str, user_service=Depends(get_user_service)):
    user = await user_service.get_user(user_id)
    if user:
        return user
    return JSONResponse(
        content={"message": "User not found"},
        status_code=status.HTTP_404_NOT_FOUND,
    )


@router.delete("/delete-user/{user_id}")
async def delete_user(user_id: str, user_service=Depends(get_user_service)):
    await user_service.delete_user(user_id)
    return JSONResponse(
        content={"message": "User deleted successfully"},
        status_code=status.HTTP_200_OK,
    )


@router.post("/create-product")
async def create_product(
    product: CreateProductRequest, product_service=Depends(get_product_service)
):
    await product_service.create_product(product)
    return JSONResponse(
        content={"message": "Product created successfully"},
        status_code=status.HTTP_201_CREATED,
    )
