from pydantic import BaseModel

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
