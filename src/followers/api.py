from fastapi import APIRouter, Depends
from typing import List

from . import schemas, models
from src.user.models import User
from src.user.auth import current_active_user

follower_router = APIRouter(prefix='/followers', tags=["followers"])


@follower_router.post('/', response_model=schemas.FollowerList)
async def add_follower(
        schema: schemas.FollowerCreate, user: User = Depends(current_active_user)
):
    """ Router for adding subscribers
    """
    host = await User.objects.get(username=schema.username)
    return await models.Follower.objects.create(subscriber=user.dict(), user=host)


@follower_router.get('/', response_model=schemas.FollowerListTest)
async def my_list_following(user: User = Depends(current_active_user)):
    """ Tist of who the user is subscribed to
    """
    followers = await models.Follower.objects.select_related(
        ['user', 'subscriber']
    ).filter(subscriber=user.id).all()
    list_followers = [item.user for item in followers]
    response = schemas.FollowerListTest(user=user, subscriber=list_followers)
    return response


@follower_router.delete('/{username}', status_code=204)
async def delete_follower(username: str, user: User = Depends(current_active_user)):
    """ Unsubscribe from the user
    """
    follower = await models.Follower.objects.get_or_none(
        user__username=username, subscriber=user.id)
    if follower:
        await follower.delete()
    return {}


@follower_router.get('/me', response_model=List[schemas.FollowerList])
async def my_list_follower(user: User = Depends(current_active_user)):
    """ List of user's subscribers
    """
    return await models.Follower.objects.select_related(
        ['user', 'subscriber']
    ).filter(user=user.id).all()
