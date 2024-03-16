from fastapi import APIRouter

from server.student.assignment import student_assignment
from server.student.course import student_course
from server.student.question import student_practice

student = APIRouter()
student.include_router(student_course)
student.include_router(student_practice)
student.include_router(student_assignment)
