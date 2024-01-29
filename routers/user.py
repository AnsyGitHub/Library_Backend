from fastapi import APIRouter, Depends
from typing import Annotated
from dependency import get_current_active_user, get_db
import schemas
user_router = APIRouter(prefix= "/users/me",tags=["users"])


@user_router.get("/")
async def read_users_me(current_user: Annotated[schemas.User, Depends(get_current_active_user)]):
    return current_user

@user_router.get("/items")
async def read_own_items(current_user: Annotated[schemas.User, Depends(get_current_active_user)]):
    return [{"owner": current_user.username}]




