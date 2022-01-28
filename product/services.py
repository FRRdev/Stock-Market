from typing import IO, Generator
from uuid import uuid4

from fastapi import UploadFile, BackgroundTasks, HTTPException, Request
import datetime
import aiofiles

from user.models import User
from .models import Product
from .schemas import UploadProduct


async def save_product(user: User,
                       name: str,
                       img: UploadFile,
                       start_price: float,
                       deadline_time: datetime.datetime
                       ):
    file_name = f'media/img/{user.id}_{uuid4()}.jpg'
    if img.content_type == "image/jpeg":
        # background_tasks.add_task(write_video, file_name, file)
        await write_img(file_name, img)
    else:
        raise HTTPException(status_code=418, detail='It is not jpg')
    info = UploadProduct(name=name, start_price=start_price, deadline_time=deadline_time)
    return await Product.objects.create(image=file_name, user=user.dict(), **info.dict())


async def write_img(file_name: str, file: UploadFile):
    async with aiofiles.open(file_name, "wb") as buffer:
        data = await file.read()
        await buffer.write(data)
