from fastapi import APIRouter
from datetime import datetime
from pojo.dto import addUserDTO
from pojo.entity import User
from util.result import Result

admin = APIRouter()


@admin.get("/user")
async def getUsers():
    users = await User.all().values()
    return Result.success(users)


@admin.post("/user")
async def addUser(userDTO: addUserDTO):
    userDTO.personalization = ""  # 根据需要设置personalization属性
    userDTO.createTime = datetime.utcnow()  # 将createTime属性设置为当前的UTC时间
    userDTO.updateTime = datetime.utcnow()  # 将createTime属性设置为当前的UTC时间
    print(userDTO)
    # result = await User.save(**userDTO)
    return Result.success()
