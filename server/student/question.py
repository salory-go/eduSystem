from typing import Optional

from fastapi import APIRouter
from datetime import datetime
from pojo.dto import UserDTO, CourseDTO
from pojo.entity import User, Course, Assignment, Student_Course, Question, Chapter
from pojo.vo import AssignmentVO, QuestionVO
from util.result import Result

student_practice = APIRouter()


@student_practice.get("/student/question")
async def get_questions(courseId: Optional[int] = None, difficulty: Optional[int] = None,
                        chapterId: Optional[int] = None):
    query = {
        'courseId': courseId,
        'chapterId': chapterId,
        'difficulty': difficulty
    }
    query = {k: v for k, v in query.items() if v is not None}

    questions = await Question.filter(**query).values("id", "courseId", "chapterId", "content", "difficulty")
    questionList = []
    for q in questions:
        course = await Course.get(id=q["courseId"]).values('courseName')
        chapter = await Chapter.get(id=q["chapterId"]).values('chapterName')

        questionVO = QuestionVO(id=q["id"], courseName=course["courseName"], chapterName=chapter["chapterName"],
                                content=q["content"],
                                difficulty=q["difficulty"])
        questionList.append(questionVO)

    return Result.success(questionList)


