from pydantic import BaseModel

from src.user.schemas import UserOut
from src.product.schemas import IdProduct


class BoardCreate(BaseModel):
    id: int
    user: UserOut
    product: IdProduct
