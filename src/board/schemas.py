import datetime

from pydantic import BaseModel
from typing import List

from src.user.schemas import UserOut
from src.product.schemas import IdProduct, ListProductForBoard


class BoardCreate(BaseModel):
    id: int
    user: UserOut
    product: IdProduct


class BoardList(BaseModel):
    id: int
    user: UserOut
    product: ListProductForBoard


class CreateBet(BaseModel):
    id: int
    rate: float


class BetDetail(CreateBet):
    user: UserOut
    create_at: datetime.datetime


class BoardDetail(BaseModel):
    id: int
    user: UserOut
    product: ListProductForBoard
    deadline_time: datetime.datetime
    board_bets: List[BetDetail]
    active: bool
