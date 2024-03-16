from fastapi import APIRouter

from pojo.entity import Course, Chapter, Student_Course, User
from util.result import Result

teacher_course = APIRouter()


@teacher_course.get("/course")
async def get_courses(userId: int):
    courseList = await Course.filter(userId=userId).values('id', 'image', 'courseName')
    return Result.success(courseList)


@teacher_course.get('/course/chapter')
async def get_chapters(courseId: int):
    chapterList = await Chapter.filter(courseId=courseId).values('id', 'chapterName')
    return Result.success(chapterList)


@teacher_course.get('/course/student')
async def get_students(courseId: int):
    userIds = await Student_Course.filter(courseId=courseId).values_list('userId', flat=True)
    userList = await User.filter(id__in=userIds).values('id', 'userNumber', 'name', 'email')
    return Result.success(userList)
