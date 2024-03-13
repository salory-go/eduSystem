
from typing import Optional

from fastapi import APIRouter
from datetime import datetime
from pojo.dto import UserDTO, CourseDTO
from pojo.entity import User, Course
from util.result import Result
from typing import List

course = APIRouter()

@course.get("/admin/course")
async def getCourses():
    courses = await Course.all().values()
    return Result.success(courses)



@course.post("/admin/Course")
async def addCourse(courseDTO: CourseDTO):
    if courseDTO:
        time = datetime.utcnow()  # 将createTime和updateTime属性设置为当前的UTC时间
        data = courseDTO.dict()
        data.update({
            "createTime": time,
            "updateTime": time
        })
        await Course(**data).save()
        return Result.success()
    else:
        return Result.error("课程信息为空")

@course.delete("/admin/course")
async def deleteCourseByIds(courseIds: List[int]):
    try:
        for courseId in courseIds:
            # 使用 await 删除用户
            delete1 = await Course.filter(id=courseId).delete()
            if delete1:
                print(f"User with ID {courseId} deleted successfully.")
            else:
                print(f"User with ID {courseId} not found.")
    except Exception as e:
        print(f"Error deleting users: {e}")
        return Result.error("删除课程时发生错误")

    return Result.success("课程删除成功")