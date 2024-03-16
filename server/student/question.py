from typing import Optional

from fastapi import APIRouter

from pojo.dto import AnswerDTO
from pojo.entity import Course, Question, Chapter, Student_Answer
from pojo.vo import QuestionVO, ReferenceVO
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


@student_practice.post("/student/question")
async def submit_answer(answerDTO: AnswerDTO):
    # TODO 打分
    score = 100
    studentAnswer = await Student_Answer.filter(userId=answerDTO.userId, questionId=answerDTO.questionId).first()

    if studentAnswer:
        await Student_Answer.filter(userId=answerDTO.userId, questionId=answerDTO.questionId).update(
            studentAnswer=answerDTO.studentAnswer, score=score)
    else:
        await Student_Answer.create(userId=answerDTO.userId, questionId=answerDTO.questionId,
                                    studentAnswer=answerDTO.studentAnswer, score=score)

    return Result.success()


@student_practice.get("/student/question/reference")
async def get_reference(questionId: int):
    question = await Question.get(id=questionId).values("courseId", "chapterId", "content", "answer")
    course = await Course.get(id=question['courseId'])
    chapter = await Chapter.get(id=question['chapterId'])
    courseName = course.courseName
    chapterName = chapter.chapterName
    # TODO 用大模型生成解析
    idea = ""
    topic = ""
    reference = ReferenceVO(idea=idea, tpoic=topic, answer=question['answer'])
    return Result.success(reference)


@student_practice.get("/student/question/history")
async def get_reference(userId: int, questionId: int):
    studentAnswer = await Student_Answer.filter(userId=userId, questionId=questionId).first().values('studentAnswer',
                                                                                                     'score',
                                                                                                     'submitTime')
    if studentAnswer:
        return Result.success(studentAnswer)
    else:
        return Result.error('未曾作答')
