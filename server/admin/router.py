from typing import Optional

from fastapi import APIRouter
from datetime import datetime
from pojo.dto import UserDTO
from pojo.entity import User
from util.result import Result

admin = APIRouter()


@admin.get("/user")
async def getUsers():
    users = await User.all().values()
    return Result.success(users)


@admin.post("/user")
async def addUser(userDTO: Optional[UserDTO]):
    if userDTO:
        time = datetime.utcnow()  # 将createTime和updateTime属性设置为当前的UTC时间
        user_data = userDTO.dict()
        user_data.update({
            "personalization": "",
            "createTime": time,
            "updateTime": time
        })
        result = await User(**user_data).save()
        print(result)
        return Result.success()
    else:
        return Result.error("用户信息为空")


