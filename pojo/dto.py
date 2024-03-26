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
    courseName: Optional[str] = None
    chapterName: Optional[str] = None
    difficulty: int = 2
    topic: Optional[List[str]] = None
    content: Optional[str] = None
    answer: Optional[str] = None


class AssignmentDTO(BaseModel):
    courseId: Optional[int] = None
    chapterId: Optional[int] = None
    userId: Optional[int] = None
    title: Optional[str] = None
    isPersonalized: bool = False
    questionIds: Optional[List[int]] = None
    deadline: Optional[int] = None


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


class QuestionGradeDTO(BaseModel):
    questionId: int
    score: float


class AssignmentGradeDTO(BaseModel):
    userId: int
    assignmentId: int
    assignmentScore: float
    grades: List[QuestionGradeDTO]
