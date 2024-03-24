from typing import List, Optional

from pydantic import BaseModel


class UserDTO(BaseModel):
    userNumber: str
    password: str
    role: int
    name: Optional[str] = None
    email: Optional[str] = None


class QuestionDTO(BaseModel):
    number: int = 1
    isSimilar: bool = False
    courseName: str = "计算机网络"
    chapterName: str = "综合练习"
    difficulty: int = 2
    topic: Optional[List[str]] = None
    content: Optional[str] = None
    answer: Optional[str] = None


class AssignmentDTO(BaseModel):
    courseId: int
    chapterId: int
    userId: int
    title: str
    isPersonalized: bool
    questionIds: Optional[List[int]] = None
    deadline: int


class CourseDTO(BaseModel):
    image: str
    courseName: str
    userId: int
    chapters: List[str]


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
