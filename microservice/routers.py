from fastapi import APIRouter, Depends
from models import Statistics
from user import (
    create_user,
    get_user,
    get_users,
    delete_user,
    update_user

)
from authentication import get_current_user
routes_user = APIRouter()


@routes_user.post("/create", response_model=Statistics)
def create(user: Statistics):
    return create_user(user.dict())


@routes_user.get("/get/{id}")
def get_by_id(id: str = Depends(get_current_user)):
    return get_user(id)


@routes_user.get("/all")
def get_all_users():
    return get_users()


@routes_user.get("/delete")
def delete(user: Statistics):
    return delete_user(user.dict())


@routes_user.post("/update")
def update(user: Statistics):
    return update_user(user.dict())