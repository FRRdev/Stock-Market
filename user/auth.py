from fastapi_users.authentication import JWTStrategy, AuthenticationBackend, BearerTransport
from fastapi_users import BaseUserManager
from user.schemas import UserDB, User, UserCreate, UserUpdate
from fastapi import Request, Depends
from typing import Optional
from fastapi_users import FastAPIUsers

from user.schemas import UserDB, User, UserCreate, UserUpdate

from user.models import User
from fastapi_users.db import OrmarBaseUserModel, OrmarUserDatabase

SECRET = 'Sajdljfldsjlvsdjvnsjlvnldsvnljsdnvjlsfnvljsfnvlnfjvsfjvnsjfkvndsf'


async def get_user_db():
    yield OrmarUserDatabase(UserDB, User)


class UserManager(BaseUserManager[UserCreate, UserDB]):
    user_db_model = UserDB
    reset_password_token_secret = SECRET
    verification_token_secret = SECRET

    async def on_after_register(self, user: UserDB, request: Optional[Request] = None):
        print(f"User {user.id} has registered.")

    async def on_after_forgot_password(
            self, user: UserDB, token: str, request: Optional[Request] = None
    ):
        print(f"User {user.id} has forgot their password. Reset token: {token}")

    async def on_after_request_verify(
            self, user: UserDB, token: str, request: Optional[Request] = None
    ):
        print(f"Verification requested for user {user.id}. Verification token: {token}")


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)


jwt_authentication = JWTStrategy(secret=SECRET, lifetime_seconds=3600)

bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET, lifetime_seconds=3600)


auth_backends = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)

fastapi_users = FastAPIUsers(
    get_user_manager,
    [auth_backends],
    User,
    UserCreate,
    UserUpdate,
    UserDB
)

current_active_user = fastapi_users.current_user(active=True)