import datetime
from typing import Optional, Union, Dict, List

import ormar
from db import MainMeta
from user.models import User


class Product(ormar.Model):
    """Product models
    """

    class Meta(MainMeta):
        pass

    id: int = ormar.Integer(primary_key=True)
    name: str = ormar.String(max_length=50)
    image: str = ormar.String(max_length=1000)
    create_at: datetime.datetime = ormar.DateTime(default=datetime.datetime.now)
    user: Optional[Union[User, Dict]] = ormar.ForeignKey(User, related_name='user_products')
    start_price: float = ormar.Float()
    deadline_time: datetime.datetime = ormar.DateTime(
        default=(datetime.datetime.now() + datetime.timedelta(days=1))
    )


class Comment(ormar.Model):
    """Comment to product
    """

    class Meta(MainMeta):
        pass

    id: int = ormar.Integer(primary_key=True)
    user: Optional[Union[User, Dict]] = ormar.ForeignKey(User, related_name='user_comments')
    product: Optional[Union[Product, Dict]] = ormar.ForeignKey(Product, related_name='product_comments')
    create_at: datetime.datetime = ormar.DateTime(default=datetime.datetime.now)
    text: str = ormar.String(max_length=1000)
