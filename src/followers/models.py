import ormar
from typing import Optional, Union, Dict

from db import MainMeta
from src.user.models import User


class Follower(ormar.Model):
    """ Follower model
    """

    class Meta(MainMeta):
        pass

    id: int = ormar.Integer(primary_key=True)
    user: Optional[Union[User, Dict]] = ormar.ForeignKey(User, related_name="user")
    subscriber: Optional[Union[User, Dict]] = ormar.ForeignKey(User, related_name="subscriber")
