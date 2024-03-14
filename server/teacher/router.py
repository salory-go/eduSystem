from fastapi import APIRouter

from server.teacher.assignment import teacher_assignment
from server.teacher.course import teacher_course
from server.teacher.question import teacher_question

teacher = APIRouter()

teacher.include_router(teacher_assignment)
teacher.include_router(teacher_question)
teacher.include_router(teacher_course)
