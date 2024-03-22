import json
from typing import Optional
from fastapi import APIRouter, Response
from fastapi.openapi.models import Response
from tortoise.exceptions import DoesNotExist

from pojo.entity import Course, Star, Question, Chapter
from pojo.vo import QuestionVO
from pojo.result import Result
from util.dateParse import parse

student_star = APIRouter()


@student_star.get("/star")
async def get_stars(userId: int, courseId: Optional[int] = None):
    query = {
        'userId': userId,
        'courseId': courseId
    }
    query = {k: v for k, v in query.items() if v is not None}

    stars = await Star.filter(**query).values('questionId', 'createTime')

    starList = []
    for s in stars:
        q = await Question.get(id=s['questionId']).values("id", "courseId", "chapterId", "content", "difficulty")
        course = await Course.get(id=q["courseId"]).values('courseName')
        chapter = await Chapter.get(id=q["chapterId"]).values('chapterName')

        starVO = QuestionVO(id=q["id"], courseName=course["courseName"], chapterName=chapter["chapterName"],
                           content=q["content"], difficulty=q["difficulty"], createTime=parse(s['createTime']))
        starList.append(starVO)

    return Result.success(starList)


@student_star.post("/star")
async def add_star(userId: int, questionId: int):
    try:
        await Star.get(userId=userId, questionId=questionId)
        result = json.dumps(Result.error('已在收藏中！').model_dump())
        return Response(status_code=400, media_type='application/json', content=result)
    except DoesNotExist:
        await Star.create(userId=userId, questionId=questionId)
        return Result.success()


@student_star.delete("/star")
async def del_star(starId: int):
    await Star.filter(id=starId).delete()
    return Result.success()
