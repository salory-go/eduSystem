from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class LoginVO(BaseModel):
    id: int
    token: str


class QuestionVO(BaseModel):
    id: int
    courseName: str
    chapterName: str
    difficulty: int
    content: str
    answer: str
    createTime: datetime


class AssignmentVO(BaseModel):
    id: int
    courseName: str
    title: str
    deadline: str
    overdue: bool
    completed: Optional[bool] = None
    score: Optional[int] = None
    createTime: datetime


class CourseVO(BaseModel):
    id: int
    image: str
    courseName: str
    teacherName: str
    joinTime: datetime

class ReferenceVO(BaseModel):
    idea: str
    topic: str
    answer: str