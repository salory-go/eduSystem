
from typing import Optional

from fastapi import APIRouter
from datetime import datetime
from pojo.dto import UserDTO, CourseDTO
from pojo.entity import User, Course
from util.result import Result
from typing import List

user = APIRouter()


@user.get("/admin/user")
async def getUsers(role: int):
    try:
        # 使用 fetch 方法而不是 values
        users = await User.filter(role=role).values()
        return Result.success(users)
    except Exception as e:
        print(f"Error getting users: {e}")
        return Result.error("获取用户列表时发生错误")


@user.post("/admin/user")
async def addUser(userDTO: UserDTO):
    if userDTO:
        time = datetime.utcnow()  # 将createTime和updateTime属性设置为当前的UTC时间
        user_data = userDTO.dict()
        user_data.update({
            "personalization": "",
            "createTime": time,
            "updateTime": time
        })
        await User(**user_data).save()
        return Result.success()
    else:
        return Result.error("用户信息为空")

@user.delete("/admin/user")
async def deleteUserByIds(userIds: List[int]):
    print(userIds)
    try:
        for user_id in userIds:
            # 使用 await 删除用户
            delete = await User.filter(id=user_id).delete()
            if delete:
                print(f"User with ID {user_id} deleted successfully.")
            else:
                print(f"User with ID {user_id} not found.")
    except Exception as e:
        print(f"Error deleting users: {e}")
        return Result.error("删除用户时发生错误")

    return Result.success("用户删除成功")

