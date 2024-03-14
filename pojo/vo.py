from datetime import datetime
from typing import List, Optional

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
    createTime: Optional[datetime] = None


class AssignmentVO(BaseModel):
    id: Optional[int] = None
    courseName: Optional[str] = None
    title: Optional[str] = None
    deadline: Optional[datetime] = None
    overdue: Optional[bool] = None
    createTime: Optional[datetime] = None
