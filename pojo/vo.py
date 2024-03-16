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
    deadline: Optional[str] = None
    overdue: Optional[bool] = None
    completed: Optional[bool] = None
    score: Optional[int] = None
    createTime: Optional[datetime] = None


class CourseVO(BaseModel):
    id: Optional[int] = None
    image: Optional[str] = None
    courseName: Optional[str] = None
    teacherName: Optional[str] = None
    joinTime: Optional[datetime] = None


class StarVO(BaseModel):
    id: Optional[int] = None
    courseId: Optional[int] = None
    userId: Optional[int] = None
    content: Optional[str] = None
    chapter: Optional[str] = None
    answer: Optional[str] = None
    difficulty: Optional[int] = None
    createTime: Optional[datetime] = None
    updateTime: Optional[datetime] = None
