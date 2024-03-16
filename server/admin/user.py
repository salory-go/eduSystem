from fastapi import APIRouter
from pojo.dto import UserDTO
from pojo.entity import User
from util.result import Result

admin_user = APIRouter()


@admin_user.get("/user")
async def get_users(role: int):
    users = await User.filter(role=role).values("id", "userNumber", "name", "email")
    return Result.success(users)


@admin_user.post("/user")
async def add_user(userDTO: UserDTO):
    user_data = userDTO.model_dump()
    await User.create(**user_data)
    return Result.success()


@admin_user.delete("/user")
async def del_user(userId: int):
    user = await User.get(id=userId)
    if user.role == 3:
        await User.filter(id=userId).delete()
    elif user.role == 2:
    # TODO 删除关联的所有..
    return Result.success()
