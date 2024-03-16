from fastapi import APIRouter
from pojo.entity import Course, Student_Course, User
from pojo.vo import CourseVO
from util.result import Result
from tortoise.exceptions import DoesNotExist

student_course = APIRouter()


@student_course.get("/course")
async def get_courses():
    courseList = await Course.all().values("id", "image", "courseName", "teacherName", "createTime")
    return Result.success(courseList)


@student_course.get("/course")
async def get_my_courses(user_id: int):
    courses = await Student_Course.filter(userId=user_id).values('courseId', 'joinTime')
    courseList = []
    for c in courses:
        course = await Course.get(id=c['courseId']).values('id', 'image', 'courseName', 'userId')
        user = await User.get(id=c['userId']).values('name')
        courseVO = CourseVO(id=course['courseId'], image=course['image'], courseName=course['courseName'],
                            teacherName=user['name'], joinTime=c['joinTime'])
        courseList.append(courseVO)

    return Result.success(courseList)


@student_course.post("/Course")
async def add_course(userId: int, courseId: int):
    # 检验是否有该课程
    try:
        await Student_Course.get(userId=userId, courseId=courseId)
        # TODO 返回400状态码
        return Result.error('已在该课程中！')
    except DoesNotExist:
        await Student_Course.create(userId=userId, courseId=courseId)
        return Result.success()
