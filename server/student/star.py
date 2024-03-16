from fastapi import APIRouter
from pojo.entity import Course, Assignment, Student_Course, Star, Question, Chapter
from pojo.vo import AssignmentVO, StarVO
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
