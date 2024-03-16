from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class UserDTO(BaseModel):
    userNumber: str
    password: str
    role: int
    name: Optional[str] = None
    email: Optional[str] = None


class QuestionDTO(BaseModel):
    number: Optional[int] = None
    courseName: Optional[str] = None
    chapterName: Optional[str] = None
    difficulty: Optional[int] = None
    topic: Optional[List[str]] = None
    content: Optional[str] = None
    answer: Optional[str] = None


class AssignmentDTO(BaseModel):
    courseId: int
    userId: int
    title: str
    isPersonalized: bool
    questionIds: Optional[List[int]] = None
    deadline: datetime


class CourseDTO(BaseModel):
    courseName: str
    userId: int


class QuestionListDTO(BaseModel):
    userId: int
    questions: List[QuestionDTO]


class AnswerDTO(BaseModel):
    userId: Optional[int] = None
    questionId: int
    studentAnswer: str


class AnswerListDTO(BaseModel):
    assignmentId: int
    userId: int
    answers: List[AnswerDTO]


class StarDTO(BaseModel):
    userId: int
    questionId: int
