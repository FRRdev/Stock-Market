from pydantic import BaseModel
import datetime
from src.user.schemas import UserOut


class IdProduct(BaseModel):
    id: int


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


class ListProductForBoard(BaseModel):
    id: int
    name: str
    image: str
    create_at: datetime.datetime
    start_price: float
    deadline_time: datetime.datetime


class UploadComment(BaseModel):
    text: str


class ListComment(BaseModel):
    text: str
    user: UserOut
