from fastapi import APIRouter

from pojo.dto import loginDTO
from pojo.entity import User
from pojo.vo import UserVO
from util.result import Result

common = APIRouter()


@common.get("/login")
async def login(userDTO: loginDTO):
    user = await User.filter(userNumber=userDTO.userNumber).values()
    if len(user) == 0:
        return Result.error("账户未存在")
    userVo = UserVO(**user)
    return Result.success(userVo)


@common.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
