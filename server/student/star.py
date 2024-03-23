import json
from typing import Optional
from fastapi import APIRouter, Response
from fastapi.openapi.models import Response
from tortoise.exceptions import DoesNotExist

from pojo.dto import StarDTO
from pojo.entity import Course, Star, Question, Chapter
from pojo.vo import QuestionVO
from pojo.result import Result
from util.dateParse import parse

student_star = APIRouter()


@student_star.get("/star")
async def get_stars(userId: int, courseId: Optional[int] = None):
    stars = await Star.filter(userId=userId).values('questionId', 'createTime')

    starList = []
    for s in stars:
        q = await Question.get(id=s['questionId']).values("id",
                                                          "courseId",
                                                          "chapterId",
                                                          "content",
                                                          "difficulty")
        if courseId and q['id'] != courseId:
            continue

        course = await Course.get(id=q["courseId"]).values('courseName')
        chapter = await Chapter.get(id=q["chapterId"]).values('chapterName')

        starList.append(QuestionVO(id=q["id"],
                                   courseName=course["courseName"],
                                   chapterName=chapter["chapterName"],
                                   content=q["content"],
                                   difficulty=q["difficulty"],
                                   createTime=parse(s['createTime'])))

    return Result.success(starList)


@student_star.post("/star")
async def add_star(starDTO: StarDTO):
    try:
        await Star.get(userId=starDTO.userId, questionId=starDTO.questionId)
        result = json.dumps(Result.error('已在收藏中！').model_dump())
        return Response(status_code=400, media_type='application/json', content=result)
    except DoesNotExist:
        await Star.create(userId=starDTO.userId, questionId=starDTO.questionId)
        return Result.success()


@student_star.delete("/star")
async def del_star(starId: int):
    await Star.filter(id=starId).delete()
    return Result.success()
