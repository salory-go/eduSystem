from fastapi import APIRouter
from tortoise.exceptions import DoesNotExist

from pojo.entity import Course, Star, Question, Chapter
from pojo.vo import StarVO
from util.result import Result

student_star = APIRouter()


@student_star.get("/student/star")
async def get_stars(userId: int):
    stars = await Star.filter(userId=userId).values('questionId', 'createTime')

    starList = []
    for s in stars:
        q = await Question.get(id=s['questionId']).values("id", "courseId", "chapterId", "content", "difficulty")
        course = await Course.get(id=q["courseId"]).values('courseName')
        chapter = await Chapter.get(id=q["chapterId"]).values('chapterName')

        starVO = StarVO(id=q["id"], courseName=course["courseName"], chapterName=chapter["chapterName"],
                        content=q["content"], difficulty=q["difficulty"], createTime=q["createTime"])
        starList.append(starVO)

    return Result.success(starList)


@student_star.post("/student/star")
async def add_star(userId: int, questionId: int):
    try:
        await Star.get(userId=userId, questionId=questionId)
        # TODO 返回400状态码
        return Result.error('已在收藏中！')
    except DoesNotExist:
        await Star.create(userId=userId, questionId=questionId)
        return Result.success()


@student_star.delete("/student/star")
async def del_star(starId: int):
    await Star.filter(id=starId).delete()
    return Result.success()
