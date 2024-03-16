from fastapi import APIRouter

from pojo.dto import UserDTO
from pojo.entity import User
from pojo.vo import LoginVO
from util.result import Result
from tortoise.exceptions import DoesNotExist

login = APIRouter()


@login.get("/login")
async def login(userDTO: UserDTO):
    try:
        user = await User.get(userNumber=userDTO.userNumber)
        # TODO JWT Token生成
        token = ''
        return Result.success(LoginVO(id=user.id, token=token))
    except DoesNotExist as e:
        # TODO 返回400状态码
        return Result.error("账号或密码错误！")
