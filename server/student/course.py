import json

from fastapi import APIRouter, Response
from pojo.entity import Course, Student_Course, User, Chapter
from pojo.vo import CourseVO
from pojo.result import Result
from tortoise.exceptions import DoesNotExist

from util.dateParse import parse

student_course = APIRouter()


@student_course.get("/course")
async def get_courses():
    courses = await Course.all().values("id",
                                        "image",
                                        "courseName",
                                        "userId",
                                        "createTime")
    courseList = []
    for c in courses:
        user = await User.get(id=c['userId']).values('name')
        courseList.append(CourseVO(id=c['id'],
                                   image=c['image'],
                                   courseName=c['courseName'],
                                   teacherName=user['name'],
                                   createTime=parse(c['createTime'])).model_dump(exclude_unset=True))
    return Result.success(courseList)


@student_course.get("/course/{userId}")
async def get_my_courses(userId: int):
    courses = await Student_Course.filter(userId=userId).values('courseId', 'joinTime')
    courseList = []
    for c in courses:
        course = await Course.get(id=c['courseId']).values('id',
                                                           'image',
                                                           'courseName',
                                                           'userId')
        user = await User.get(id=course['userId']).values('name')

        courseList.append(CourseVO(id=course['id'],
                                   image=course['image'],
                                   courseName=course['courseName'],
                                   teacherName=user['name'],
                                   joinTime=parse(c['joinTime']))
                          .model_dump(exclude_unset=True))

    return Result.success(courseList)


@student_course.get("/course/chapter")
async def get_chapters(courseId: int):
    chapterList = await Chapter.filter(courseId=courseId).values('id', 'chapterName')
    return Result.success(chapterList)


@student_course.post("/course")
async def add_course(userId: int, courseId: int):
    # 检验是否有该课程
    try:
        await Student_Course.get(userId=userId, courseId=courseId)
        result = json.dumps(Result.error('已在该课程中！').model_dump())
        return Response(status_code=400, media_type='application/json', content=result)
    except DoesNotExist:
        await Student_Course.create(userId=userId, courseId=courseId)
        return Result.success()
