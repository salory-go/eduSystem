import json

from fastapi import APIRouter, Response

from pojo.dto import UserDTO
from pojo.entity import User
from pojo.vo import LoginVO
from pojo.result import Result
from tortoise.exceptions import DoesNotExist

from util.jwtToken import generate

login = APIRouter()


@login.post("/login")
async def user_login(userDTO: UserDTO):
    try:
        user = await User.get(userNumber=userDTO.userNumber,
                              password=userDTO.password,
                              role=userDTO.role)
        # JWT Token生成
        payload = dict(userNumber=user.id)
        token = generate(payload)
        return Result.success(LoginVO(id=user.id, token=token))
    except DoesNotExist:
        result = json.dumps(Result.error("账号或密码错误！").model_dump())
        return Response(status_code=400, media_type="application/json", content=result)
