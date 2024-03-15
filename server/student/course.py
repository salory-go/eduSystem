from fastapi import APIRouter
from pojo.entity import Course, Assignment, Student_Course
from pojo.vo import AssignmentsOfCourseVO, CourseVO
from util.result import Result

student_course = APIRouter()


@student_course.get("/student/course")
async def get_courses():
    courses = await Course.all().values("id","image","courseName","teacherName","createTime")
    return Result.success(courses)

@student_course.get("/student/course")
async def get_my_courses(user_id: int):
    courses = await Student_Course.filter(userId=user_id).values("id","image","courseName","teacherName","createTime")
    return Result.success(courses)

# @student_course.get("/student/course/{courseId}")
# async def get_course_info(courseId: int):
#     # 获取课程对象
#     course = await Course.get(id=courseId).values()
#     # 获取课程对应的作业对象
#     lists = await Assignment.filter(courseId=courseId).values()
#     for item in lists:
#         item.pop("courseId")
#     # 封装成VO
#     assignments = AssignmentsOfCourseVO(**lists)
#     courseVO = CourseVO(courseName=course.courseName,assignments=assignments)
#     return Result.success()


@student_course.post("/student/Course")
async def add_course(userId: int,courseId: int):
    #检验是否有该课程
    list = await Student_Course.filter(userId=userId,courseId=courseId).values()
    if list:
        await Student_Course.save(userId=userId,courseId=courseId)
        return Result.success()
    return Result.error()