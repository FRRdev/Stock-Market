import datetime

import ormar
from db import MainMeta

from typing import Optional, Union, Dict, List

from src.product.models import Product
from src.user.models import User


class Board(ormar.Model):
    """Board model
    """

    class Meta(MainMeta):
        pass

    id: int = ormar.Integer(primary_key=True)
    user: Optional[Union[User, Dict]] = ormar.ForeignKey(User, related_name='boards')
    product: Optional[Union[Product, Dict]] = ormar.ForeignKey(Product, related_name='product_boards', unique=True)



class Bet(ormar.Model):
    """Bet models
    """

    class Meta(MainMeta):
        pass

    id: int = ormar.Integer(primary_key=True)
    board: Optional[Union[Board, Dict]] = ormar.ForeignKey(Board, related_name='board_bets')
    user: Optional[Union[User, Dict]] = ormar.ForeignKey(User, related_name='user_bets')
    create_at: datetime.datetime = ormar.DateTime(default=datetime.datetime.now)
    rate: float = ormar.Float()
