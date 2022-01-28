from fastapi import APIRouter, Form, UploadFile, File, Depends
import datetime

from .models import Product
from user.models import User
from user.auth import current_active_user
from .services import save_product
from .schemas import UploadProduct

product_router = APIRouter(prefix='/product', tags=['product'])


@product_router.post('', response_model=UploadProduct)
async def create_product(
        name: str = Form(...),
        image: UploadFile = File(...),
        start_price: float = Form(...),
        deadline_time: datetime.datetime = Form(...),
        user: User = Depends(current_active_user)
):
    return await save_product(user, name, image, start_price, deadline_time)
