from fastapi import APIRouter
from datetime import datetime
from pojo.dto import CourseDTO
from pojo.entity import User, Course
from pojo.vo import CourseVO
from util.result import Result

admin_course = APIRouter()


@admin_course.get("/admin/course")
async def get_courses():
    courses = await Course.all().values("id", "image", "courseName", "userId", "createTime")
    courseList = []
    for course in courses:
        user = await User.get(id=course['userId'])
        courseList.append(CourseVO(id=course['id'],
                                   courseName=course['courseName'],
                                   image=course['image'],
                                   teacherName=user.name,
                                   createTime=course['createTime']
                                   ))
    return Result.success(courseList)


@admin_course.post("/admin/course")
async def add_course(courseDTO: CourseDTO):
    course_data = courseDTO.model_dump()
    await Course.create(**course_data)
    return Result.success()


@admin_course.delete("/admin/course")
async def del_course(courseId: int):
    await Course.filter(id=courseId).delete()
    # TODO 删除关联的所有..
    return Result.success()
