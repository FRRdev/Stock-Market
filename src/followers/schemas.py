from typing import List
from pydantic import BaseModel

from src.user.schemas import UserOut


class FollowerCreate(BaseModel):
    username: str


class FollowerList(BaseModel):
    user: UserOut
    subscriber: UserOut


class FollowerListTest(BaseModel):
    user: UserOut
    subscriber: List[UserOut]
