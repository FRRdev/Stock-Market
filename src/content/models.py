import datetime
import ormar
from typing import Optional, Union, Dict, List

from db import MainMeta
from src.user.models import User
from src.product.models import Product


class UserLike(ormar.Model):
    """ Model user's like
    """
    class Meta(MainMeta):
        pass

    id: int = ormar.Integer(primary_key=True)


class Video(ormar.Model):
    """ Video model
    """
    class Meta(MainMeta):
        pass

    id: int = ormar.Integer(primary_key=True)
    title: str = ormar.String(max_length=50)
    description: str = ormar.String(max_length=500)
    file: str = ormar.String(max_length=1000)
    create_at: datetime.datetime = ormar.DateTime(default=datetime.datetime.now)
    user: Optional[Union[User, Dict]] = ormar.ForeignKey(User, related_name='user_video')
    product: Optional[Union[Product, Dict]] = ormar.ForeignKey(Product, related_name='product_video')
    like_count: int = ormar.Integer(default=0)
    like_user: Optional[Union[List[User], Dict]] = ormar.ManyToMany(
        User, related_name="like_users", through=UserLike
    )
