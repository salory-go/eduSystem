from fastapi import APIRouter
from pojo.dto import CourseDTO
from pojo.entity import User, Course, Question, Student_Course, Chapter, Assignment, Student_Assignment
from pojo.vo import CourseVO
from server.teacher.question import del_question
from pojo.result import Result
from util.dateParse import parse

admin_course = APIRouter()


@admin_course.get("/course")
async def get_courses():
    courses = await Course.all().values("id",
                                        "image",
                                        "courseName",
                                        "userId",
                                        "createTime")
    courseList = []
    for course in courses:
        user = await User.get(id=course['userId'])
        courseList.append(CourseVO(id=course['id'],
                                   courseName=course['courseName'],
                                   image=course['image'],
                                   teacherName=user.name,
                                   createTime=parse(course['createTime']))
                          .model_dump(exclude_unset=True))
    return Result.success(courseList)


@admin_course.post("/course")
async def add_course(courseDTO: CourseDTO):
    course = Course(image=courseDTO.image,
                    courseName=courseDTO.courseName,
                    userId=courseDTO.userId)

    await course.save()
    courseId = course.id

    chapterList = []
    for c in courseDTO.chapters:
        chapterList.append(Chapter(chapterName=c,
                                   courseId=courseId))

    await Chapter.bulk_create(chapterList)
    return Result.success()


@admin_course.delete("/course")
async def del_course(courseId: int):
    # course
    await Course.filter(id=courseId).delete()
    await Student_Course.filter(courseId=courseId).delete()

    # chapter
    await Chapter.filter(courseId=courseId).delete()

    # assignment
    assignmentIds = await Assignment.filter(courseId=courseId).values_list('id', flat=True)
    for aId in assignmentIds:
        await Student_Assignment.filter(assignmentId=aId).delete()
    await Assignment.filter(courseId=courseId).delete()

    # question
    questionIds = await Question.filter(courseId=courseId).values_list('id', flat=True)
    await del_question(questionIds)
    await Question.filter(courseId=courseId).delete()

    return Result.success()
