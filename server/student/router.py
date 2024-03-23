from fastapi import APIRouter

from server.student.assignment import student_assignment
from server.student.course import student_course
from server.student.question import student_question
from server.student.star import student_star

student = APIRouter()
student.include_router(student_course)
student.include_router(student_question)
student.include_router(student_assignment)
student.include_router(student_star)
