from fastapi import APIRouter

from pojo.dto import UserDTO
from pojo.entity import User
from pojo.vo import UserVO
from util.result import Result

common = APIRouter()


@common.get("/login")
async def login(userDTO: UserDTO):
    user = await User.filter(username=userDTO.username).values()
    if len(user) == 0:
        return Result.error("账户未存在")
    userVo = UserVO(**user)
    return Result.success(userVo)


@common.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
