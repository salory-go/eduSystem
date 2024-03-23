import json
from typing import Optional, List
from fastapi import APIRouter, Response, Query
from tortoise.exceptions import DoesNotExist
from tortoise import Tortoise
from pojo.dto import StarDTO
from pojo.entity import Course, Star, Chapter
from pojo.vo import QuestionVO
from pojo.result import Result
from util.dateParse import parse

student_star = APIRouter()


@student_star.get("/star")
async def get_stars(userId: int, courseId: Optional[int] = None):
    sql = '''
    SELECT s.id, s.createTime, q.courseId, q.chapterId, content, difficulty
    FROM star s LEFT JOIN question q
    ON s.questionId = q.id
    WHERE s.userId = %s AND q.courseId = IFNULL(%s, q.courseId)
    '''

    result = await Tortoise.get_connection('default').execute_query(sql, [userId, courseId])
    await Tortoise.close_connections()
    stars = result[1]

    starList = []
    for s in stars:
        course = await Course.get(id=s["courseId"]).values('courseName')
        chapter = await Chapter.get(id=s["chapterId"]).values('chapterName')

        starList.append(QuestionVO(id=s["id"],
                                   courseName=course["courseName"],
                                   chapterName=chapter["chapterName"],
                                   content=s["content"],
                                   difficulty=s["difficulty"],
                                   createTime=parse(s['createTime']))
                        .model_dump(exclude_unset=True))

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
async def del_star(starIds: List[int] = Query(...)):
    await Star.filter(id__in=starIds).delete()
    return Result.success()
