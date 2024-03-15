from typing import Optional

from fastapi import APIRouter, Query
from datetime import datetime
from pojo.dto import UserDTO, CourseDTO
from pojo.entity import User, Course
from util.result import Result
from typing import List

admin_user = APIRouter()


@admin_user.get("/admin/user")
async def get_users(role: int):
    try:
        # 使用 fetch 方法而不是 values
        users = await User.filter(role=role).values("id","userNumber","name","email")
        return Result.success(users)
    except Exception as e:
        print(f"Error getting users: {e}")
        return Result.error("获取用户列表时发生错误")


@admin_user.post("/admin/user")
async def add_user(userDTO: UserDTO):
    if userDTO:
        print(userDTO)
        time = datetime.utcnow()  # 将createTime和updateTime属性设置为当前的UTC时间
        user_data = userDTO.model_dump(exclude_unset=True)
        print(user_data)
        user_data.update({
            "personalization": "",
            "createTime": time,
            "updateTime": time
        })
        await User(**user_data).save()
        return Result.success()
    else:
        return Result.error("用户信息为空")


@admin_user.delete("/admin/user")
async def deleteUserByIds(userId: int):
    # TODO 删除关联的所有..
    delete = await User.filter(id=userId).delete()
    return Result.success("用户删除成功")
