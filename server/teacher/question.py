from datetime import datetime

from fastapi import APIRouter
from typing import Optional, List
from tortoise.queryset import Q

from pojo.entity import Question
from pojo.dto import QuestionDTO
from util.result import Result

question = APIRouter()


@question.get("/teacher/question/{userId}")
async def get_question(userId: int,
                       courseId: Optional[int] = None,
                       chapter: Optional[int] = None,
                       difficulty: Optional[int] = None,
                       topicIds: Optional[List[int]] = None):
    filters = {
        'userId': userId,
        'courseId': courseId,
        'chapter': chapter,
        'difficulty': difficulty,
    }
    # 移除值为 None 的键
    filters = {k: v for k, v in filters.items() if v is not None}
    # TODO
    query = Q(**filters)
    if topicIds is not None:
        # query &= Q(id__in=Question_Topic.filter(topicId__in=topicIds).values("questionId"))

    questions = await Question.filter(query).values()
    return Result.success(questions)


@question.post("/teacher/question/new")
async def create_question(tags: QuestionDTO):
    tags = tags.model_dump(exclude_unset=True)

    # 模拟使用模型生成新题目
    new_question = ""

    return Result.success(new_question)


@question.post("/teacher/question")
async def add_question(questions: List[QuestionDTO]):
    for q in questions:
        q.createTime = datetime.now()
        q.updateTime = datetime.now()
        q = q.model_dump(exclude_unset=True)
        await Question.create(**q)

    return Result.success()


@question.delete("/teacher/question")
async def del_question(questionIds: List[int]):
    await Question.filter(id__in=questionIds).delete()
    return Result.success()
