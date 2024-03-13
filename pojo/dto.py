from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class UserDTO(BaseModel):
    id: Optional[int] = None
    userNumber: Optional[str] = None
    password: Optional[str] = None
    name: Optional[str] = None
    email: Optional[str] = None
    role: Optional[int] = None
    personalization: Optional[str] = None
    createTime: Optional[datetime] = None
    updateTime: Optional[datetime] = None


class QuestionDTO(BaseModel):
    id: Optional[int] = None
    number: int = None
    courseId: Optional[int] = None
    chapter: Optional[str] = None
    difficulty: Optional[int] = None
    topic: Optional[List[str]] = None
    content: Optional[str] = None
    answer: Optional[str] = None
    createTime: Optional[datetime] = None
    updateTime: Optional[datetime] = None


class AssignmentDTO(BaseModel):
    id: Optional[int] = None
    courseId: Optional[int] = None
    userId: Optional[int] = None
    title: Optional[str] = None
    description: Optional[str] = None
    questionIds: Optional[List[int]] = None
    deadline: Optional[datetime] = None
    overdue: Optional[bool] = None
    createTime: Optional[datetime] = None
    updateTime: Optional[datetime] = None


class CourseDTO(BaseModel):
    id: Optional[int] = None
    courseName: Optional[str] = None
    userId: Optional[int] = None
    createTime: Optional[datetime] = None
    updateTime: Optional[datetime] = None
