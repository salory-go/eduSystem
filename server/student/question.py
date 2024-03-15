from fastapi import APIRouter
from datetime import datetime
from pojo.dto import UserDTO, CourseDTO
from pojo.entity import User, Course, Assignment, Student_Course, Question
from pojo.vo import AssignmentsOfCourseVO, QuestionVO
from util.result import Result

student_practice = APIRouter()

@student_practice.get("/student/question")
async def get_my_question(course_id: int=None,difficulty:int=None,chapter:int=None):
    # values("id", "courseId", "chapterId", "content", "difficulty")
    courses = await Question.all()
    # courses.f
    questions = []
    for course in courses:
        # courseName = await Course.
        questions.append(QuestionVO(id=course.id,))
    return Result.success(courses)

# @student_practice.get("/student/question/{courseId}")
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