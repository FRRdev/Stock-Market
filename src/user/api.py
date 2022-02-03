from fastapi.routing import APIRouter

from src.user.auth import auth_backends
from src.user.auth import fastapi_users


user_router = APIRouter()


user_router.include_router(
    fastapi_users.get_auth_router(auth_backends), prefix="/auth/jwt", tags=["auth"]
)
user_router.include_router(
    fastapi_users.get_register_router(), prefix="/auth", tags=["auth"]
)
user_router.include_router(fastapi_users.get_users_router(), prefix="/users", tags=["users"])
