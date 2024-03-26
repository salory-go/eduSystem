from typing import Optional

from pydantic import BaseModel


class LoginVO(BaseModel):
    id: int
    token: str


class QuestionVO(BaseModel):
    id: Optional[int] = None
    courseName: Optional[str] = None
    chapterName: Optional[str] = None
    difficulty: Optional[int] = None
    content: Optional[str] = None
    answer: Optional[str] = None
    score: Optional[float] = None
    createTime: Optional[int] = None


class AssignmentVO(BaseModel):
    id: int
    courseName: str
    chapterName: str
    title: str
    deadline: int
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


class AssignmentCircumstanceVO(BaseModel):
    userId: int
    userNumber: str
    name: str
    completed: bool
    score: float
