from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class LoginDTO(BaseModel):
    userNumber: str
    password: str
    role: int


class UserDTO(BaseModel):
    id: Optional[int] = None
    userNumber: Optional[str] = None
    password: Optional[str] = None
    name: Optional[str] = None
    email: Optional[str] = None
    role: Optional[int] = None


class QuestionDTO(BaseModel):
    id: Optional[int] = None
    number: Optional[int] = None
    courseId: Optional[int] = None
    courseName: Optional[str] = None
    chapterId: Optional[int] = None
    chapterName: Optional[str] = None
    difficulty: Optional[int] = None
    topic: Optional[List[str]] = None
    content: Optional[str] = None
    answer: Optional[str] = None


class AssignmentDTO(BaseModel):
    id: Optional[int] = None
    courseId: Optional[int] = None
    userId: Optional[int] = None
    title: Optional[str] = None
    isPersonalized: Optional[bool] = None
    questionIds: Optional[List[int]] = None
    deadline: Optional[datetime] = None
    overdue: Optional[bool] = None


class CourseDTO(BaseModel):
    id: Optional[int] = None
    courseName: Optional[str] = None
    userId: Optional[int] = None


class QuestionListDTO(BaseModel):
    userId: int
    questions: List[QuestionDTO]


class AnswerDTO(BaseModel):
    questionId: int
    answer: str


class AnswerListDTO(BaseModel):
    assignmentId: int
    userId: int
    answers: List[AnswerDTO]
