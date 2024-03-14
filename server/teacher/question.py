from datetime import datetime

from fastapi import APIRouter
from typing import Optional

from pojo.entity import Question, Course, Chapter
from pojo.dto import QuestionDTO, QuestionListDTO
from pojo.vo import QuestionVO
from util.result import Result

teacher_question = APIRouter()


@teacher_question.get("/teacher/question/{userId}")
async def get_questions(userId: int,
                        courseId: Optional[int] = None,
                        chapterId: Optional[int] = None,
                        difficulty: Optional[int] = None):
    filters = {
        'userId': userId,
        'courseId': courseId,
        'chapterId': chapterId,
        'difficulty': difficulty
    }
    # 移除值为 None 的键
    filters = {k: v for k, v in filters.items() if v is not None}

    questions = await Question.filter(**filters).values('id', 'content', 'answer', 'courseId', 'chapterId',
                                                        'difficulty', 'createTime')
    questionList = []
    for q in questions:
        questionVO = QuestionVO(id=q['id'], content=q['content'], answer=q['answer'], difficulty=q['difficulty'],
                                createTime=q['createTime'])

        course = await Course.get(id=q['courseId'])
        questionVO.courseName = course.id

        chapter = await Chapter.get(id=q['chapterId'])
        questionVO.courseName = chapter.id

        questionList.append(questionVO)

    return Result.success(questionList)


@teacher_question.post("/teacher/question/new")
async def new_questions(questionDTO: QuestionDTO):
    query = questionDTO.model_dump(exclude_unset=True)

    # TODO 使用模型生成新题目
    questions = [{}, {}, {}]

    return Result.success(questions)


@teacher_question.post("/teacher/question")
async def add_questions(questionList: QuestionListDTO):
    userId = questionList.userId
    questions = questionList.questions

    for q in questions:
        q = q.model_dump(exclude_unset=True)
        question = Question(userId=userId, content=q['content'], answer=q['answer'], difficulty=q['difficulty'],
                            createTime=datetime.now(), updateTime=datetime.now())

        course = await Course.get(courseName=q['courseName'])
        question.courseId = course.id

        chapter = await Chapter.get(chapterName=q['chapterName'])
        question.chapterId = chapter.id

        await question.save()
    return Result.success()


@teacher_question.delete("/teacher/question")
async def del_question(questionId: int):
    await Question.filter(id=questionId).delete()

    # TODO 删除关联的所有..
    return Result.success()
