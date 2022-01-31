from pydantic import BaseModel
import datetime
from src.user.schemas import UserOut


class UploadProduct(BaseModel):
    name: str
    start_price: float
    deadline_time: datetime.datetime


class ListProduct(BaseModel):
    id: int
    name: str
    image: str
    create_at: datetime.datetime
    user: UserOut
    start_price: float
    deadline_time: datetime.datetime


