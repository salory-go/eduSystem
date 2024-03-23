from typing import List

from fastapi import APIRouter, Query
from pojo.dto import UserDTO
from pojo.entity import User
from pojo.result import Result

admin_user = APIRouter()


@admin_user.get("/user")
async def get_users(role: int):
    users = await User.filter(role=role).values("id",
                                                "userNumber",
                                                "name",
                                                "email")
    return Result.success(users)


@admin_user.post("/user")
async def add_user(userDTO: UserDTO):
    user_data = userDTO.model_dump()
    await User.create(**user_data)
    return Result.success()


@admin_user.delete("/user")
async def del_user(userIds: List[int] = Query(...)):
    await User.filter(id__in=userIds).delete()
    # TODO 删除关联的所有..
    return Result.success()
