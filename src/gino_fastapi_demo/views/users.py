import logging
from datetime import date

from fastapi import APIRouter
from pydantic import BaseModel
from ..models.users import User
from ..cache.cache import Cache

router = APIRouter()


@router.get("/users/{uid}")
async def get_user(uid: int):
    user = await User.get_or_404(uid)
    return user.to_dict()


class UserModel(BaseModel):
    name: str
    joind: date


@router.post("/users")
async def add_user(user: UserModel):
    rv = await User.create(nickname=user.name)
    return rv.to_dict()


@router.delete("/users/{uid}")
async def delete_user(uid: int):
    user = await User.get_or_404(uid)
    await user.delete()
    return dict(id=uid)


@router.get("/hello")
async def hello():
    await Cache.incr("path")
    return {}


def init_app(app):
    app.include_router(router)
