from typing import Optional

from pydantic import BaseModel


class LoginVO(BaseModel):
    id: int
    token: str


class QuestionVO(BaseModel):
    id: Optional[int]
    courseName: str
    chapterName: str
    difficulty: int
    content: str
    answer: str
    createTime: Optional[int]


class AssignmentVO(BaseModel):
    id: int
    courseName: str
    title: str
    deadline: str
    overdue: bool
    completed: Optional[bool] = None
    score: Optional[int] = None
    createTime: int


class CourseVO(BaseModel):
    id: int
    image: str
    courseName: str
    teacherName: str
    joinTime: Optional[int] = None
    createTime: Optional[int] = None


class ReferenceVO(BaseModel):
    idea: str
    topic: str
    answer: str


class AnswerVO(BaseModel):
    studentAnswer: str
    score: float
    submitTime: int
