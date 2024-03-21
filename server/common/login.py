import json

from fastapi import APIRouter, Response

from pojo.dto import UserDTO
from pojo.entity import User
from pojo.vo import LoginVO
from pojo.result import Result
from tortoise.exceptions import DoesNotExist

login = APIRouter()


@login.post("/login")
async def user_login(userDTO: UserDTO):
    try:
        user = await User.get(userNumber=userDTO.userNumber, password=userDTO.password, role=userDTO.role)
        # TODO JWT Token生成
        token = '这是token'
        return Result.success(LoginVO(id=user.id, token=token))
    except DoesNotExist:
        result = json.dumps(Result.error("账号或密码错误！").model_dump())
        return Response(status_code=400, media_type="application/json", content=result)
