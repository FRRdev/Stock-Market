from fastapi import APIRouter, Form, UploadFile, File, Depends, Query
import datetime
from typing import List
from fastapi_pagination import Page, paginate, Params

from src.user.models import User
from src.user.auth import current_active_user
from .services import save_product, update_product
from .schemas import UploadProduct, ListProduct
from .models import Product

product_router = APIRouter(prefix='/product', tags=['product'])


@product_router.post('', response_model=UploadProduct)
async def create_product(
        name: str = Form(...),
        image: UploadFile = File(...),
        start_price: float = Form(...),
        deadline_time: datetime.datetime = Form(...),
        user: User = Depends(current_active_user)
):
    """Create product router
    """
    return await save_product(user, name, image, start_price, deadline_time)


@product_router.put('/{product_pk}', status_code=201)
async def update_product_by_pk(
        product_pk: int = Query(...),
        name: str = Form(...),
        image: UploadFile = File(...),
        start_price: float = Form(...),
        deadline_time: datetime.datetime = Form(...),
        user: User = Depends(current_active_user)
):
    """Update product router
    """
    return await update_product(product_pk, user, name, image, start_price, deadline_time)


@product_router.get('/{user_pk}', response_model=Page[ListProduct])
async def get_list_author_products(
        user_pk: str,
        user: User = Depends(current_active_user)
):
    """Get list products by author's id
    """
    queryset = await Product.objects.select_related("user").filter(user=user_pk).all()
    return paginate(queryset)


@product_router.get('', response_model=Page[ListProduct])
async def get_list_all_videos(
        user: User = Depends(current_active_user)
):
    """Get list of all products
    """
    queryset = await Product.objects.select_related("user").all()
    return paginate(queryset)
