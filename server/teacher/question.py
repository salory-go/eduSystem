from fastapi import APIRouter
from typing import Optional, List

from pojo.entity import Question, Course, Chapter, Star, Student_Answer
from pojo.dto import QuestionDTO, QuestionListDTO
from pojo.vo import QuestionVO
from pojo.result import Result
from util.chatglmApi import generate_question

teacher_question = APIRouter()


@teacher_question.get("/question/{userId}")
async def get_questions(userId: int,
                        courseId: Optional[int] = None,
                        chapterId: Optional[int] = None,
                        difficulty: Optional[int] = None):
    query = {
        'userId': userId,
        'courseId': courseId,
        'chapterId': chapterId,
        'difficulty': difficulty
    }
    query = {k: v for k, v in query.items() if v is not None}

    questions = await Question.filter(**query).values('id', 'content', 'answer', 'courseId', 'chapterId',
                                                      'difficulty', 'createTime')
    questionList = []
    for q in questions:
        questionVO = QuestionVO(id=q['id'], content=q['content'], answer=q['answer'], difficulty=q['difficulty'],
                                createTime=q['createTime'])

        course = await Course.get(id=q['courseId']).values('courseName')
        questionVO.courseName = course['courseName']

        chapter = await Chapter.get(id=q['chapterId']).values('chapterName')
        questionVO.chapterName = chapter['chapterName']

        questionList.append(questionVO)

    return Result.success(questionList)


@teacher_question.post("/question/new")
async def new_questions(questionDTO: QuestionDTO):
    # 使用模型生成新题目
    res = generate_question(questionDTO.number, questionDTO.courseName, questionDTO.chapterName, questionDTO.difficulty)

    questionList = []
    for q in res:
        questionList.append(QuestionVO(courseName=questionDTO.courseName,
                                       chapterName=questionDTO.chapterName,
                                       difficulty=questionDTO.difficulty,
                                       **q))
    return Result.success(questionList)


@teacher_question.post("/question")
async def add_questions(questionList: QuestionListDTO):
    userId = questionList.userId
    questions = questionList.questions

    for q in questions:
        q = q.model_dump(exclude_unset=True)
        question = Question(userId=userId, content=q['content'], answer=q['answer'], difficulty=q['difficulty'])

        course = await Course.get(courseName=q['courseName']).values('id')
        question.courseId = course['id']

        chapter = await Chapter.get(chapterName=q['chapterName']).values('id')
        question.chapterId = chapter['id']

        await question.save()
    return Result.success()


@teacher_question.delete("/question")
async def del_question(questionIds: List[int]):
    await Question.filter(id__in=questionIds).delete()
    await Star.filter(questionId_in=questionIds).delete()
    await Student_Answer.filter(questionId__in=questionIds).delete()
    return Result.success()
