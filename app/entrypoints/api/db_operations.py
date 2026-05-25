from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse

from ...dependencies.database_services import get_product_service, get_user_service
from ...schemas.product import CreateProductRequest, ReadProduct
from ...schemas.user import CreateUserRequest, ReadUser
from ...services import ProductService, UserService
from ...dependencies.auth import get_user_id

router = APIRouter()

UserServiceDep = Annotated[UserService, Depends(get_user_service)]
ProductServiceDep = Annotated[ProductService, Depends(get_product_service)]


@router.post(
    "/create-user", response_model=ReadUser, status_code=status.HTTP_201_CREATED
)
async def create_user(user: CreateUserRequest, user_service: UserServiceDep):
    return await user_service.create_user(user)


@router.get("/get-user/{user_id}", response_model=ReadUser)
async def get_user(user_id: str, user_service: UserServiceDep):
    user = await user_service.get_user(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return user


@router.delete("/delete-user/me")
async def delete_user(
    user_service: UserServiceDep,
    user_id: Annotated[str, Depends(get_user_id)],
):

    await user_service.delete_user(user_id)
    return JSONResponse(
        content={"message": "User deleted successfully"},
        status_code=status.HTTP_200_OK,
    )


@router.post("/create-product", response_model=ReadProduct)
async def create_product(
    product: CreateProductRequest, product_service: ProductServiceDep
):
    await product_service.create_product(product)
    return JSONResponse(
        content={"message": "Product created successfully"},
        status_code=status.HTTP_201_CREATED,
    )
