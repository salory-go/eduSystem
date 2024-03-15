
from typing import Optional

from fastapi import APIRouter
from datetime import datetime
from pojo.dto import UserDTO, CourseDTO
from pojo.entity import User, Course
from pojo.vo import CourseVO
from util.result import Result
from typing import List

admin_course = APIRouter()

@admin_course.get("/admin/course")
async def get_courses():
    courses_all = await Course.all().values("id","image","courseName","userId","createTime")
    courses = []
    for course in courses_all:
        user = await User.get(id=course['userId'])
        courses.append(CourseVO(id=course['id'],
                                courseName=course['courseName'],
                                image=course['image'],
                                teacherName=user.name,
                                createTime=course['createTime']
                                ))
    return Result.success(courses)



@admin_course.post("/admin/course")
async def add_course(courseDTO: CourseDTO):
    course_data = courseDTO.model_dump(exclude_unset=True)
    if courseDTO:
        time = datetime.now()
        course_data.update({
            "createTime": time,
            "updateTime": time,
            "image": ""
        })
        await Course(**course_data).save()
        return Result.success()
    else:
        return Result.error("课程信息为空")

@admin_course.delete("/admin/course")
async def del_course(courseId: int):
    # TODO 删除关联的所有..
    await Course.filter(id=courseId).delete()
    return Result.success("课程删除成功")