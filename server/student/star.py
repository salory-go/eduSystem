from fastapi import APIRouter
from pojo.entity import Course, Assignment, Student_Course, Star, Question
from pojo.vo import AssignmentsOfCourseVO, StarOfStudentVO
from util.result import Result

student_star = APIRouter()

@student_star.get("/student/star")
async def get_stars():
    starList = await Star.all().values()
    # 用questionId来差question，然后封装成stars
    for item in starList:
        student = await Question.get(id=item.questionId).values()
    star = StarOfStudentVO()
    return Result.success()