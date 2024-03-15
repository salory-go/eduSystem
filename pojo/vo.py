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

class CourseVO(BaseModel):
    id: Optional[int] = None
    image: Optional[str] = None
    courseName: Optional[str] = None
    teacherName: Optional[str] = None
    createTime: Optional[datetime] = None
class AssignmentsOfCourseVO(BaseModel):
    id: Optional[int] = None
    title: Optional[str] = None
    description: Optional[str] = None
    deadline: Optional[str] = None
    overdue: Optional[bool] = None
    createTime: Optional[datetime] = None
    updateTime: Optional[datetime] = None

class AssignmentsOfStudentVO(BaseModel):
    id: Optional[int] = None
    courseName: Optional[str] = None
    deadline: Optional[str] = None
    title: Optional[str] = None
    overdue: Optional[bool] = None
    completed: Optional[bool] = None
    score: Optional[int] = None
    createTime: Optional[datetime] = None

class StarOfStudentVO(BaseModel):
        id: Optional[int] = None
        courseId: Optional[int] = None
        userId: Optional[int] = None
        content: Optional[str] = None
        chapter: Optional[str] = None
        answer: Optional[str] = None
        difficulty: Optional[int] = 1
        createTime: Optional[datetime] = None
        updateTime: Optional[datetime] = None

class QuestionVO(BaseModel):
    id: Optional[int] = None
    courseName: Optional[str] = None
    chapterName: Optional[str] = None
    difficulty: Optional[int] = None
    content: Optional[str] = None
    answer: Optional[str] = None
    createTime: Optional[datetime] = None

