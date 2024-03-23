from typing import Optional, List
from fastapi import APIRouter, Query
from pojo.entity import Assignment, Assignment_Question, User, Question, Course, Chapter, Student_Assignment, \
    Student_Course
from pojo.dto import AssignmentDTO
from pojo.vo import AssignmentVO
from pojo.result import Result
from util.dateParse import parse

teacher_assignment = APIRouter()


@teacher_assignment.get("/assignment")
async def get_assignments(userId: int, courseId: Optional[int] = None):
    query = {
        'userId': userId,
        'courseId': courseId,
    }
    query = {k: v for k, v in query.items() if v is not None}

    assignments = await Assignment.filter(**query).values('id',
                                                          'courseId',
                                                          'title',
                                                          'deadline',
                                                          'overdue',
                                                          'createTime')

    assignmentList = []
    for a in assignments:
        course = await Course.get(id=a['courseId']).values('courseName')

        assignmentList.append(AssignmentVO(id=a['id'],
                                           courseName=course['courseName'],
                                           title=a['title'],
                                           deadline=parse(a['deadline']),
                                           overdue=a['overdue'],
                                           createTime=parse(a['createTime'])).model_dump(exclude_unset=True))

    return Result.success(assignmentList)


@teacher_assignment.post("/assignment")
async def create_assignment(assignmentDTO: AssignmentDTO):
    assignment_data = assignmentDTO.model_dump(exclude_unset=True)
    if assignmentDTO.questionIds:
        assignment_data.pop('questionIds')

    assignment = Assignment(**assignment_data)
    await assignment.save()
    assignmentId = assignment.id
    userIds = await (Student_Course.filter(courseId=assignmentDTO.courseId)
                     .values_list('userId', flat=True))
    assignmentList = []
    for id in userIds:
        assignmentList.append(Student_Assignment(assignmentId=assignmentId, userId=id))

    await Student_Assignment.bulk_create(assignmentList)
    users = await (User.filter(id__in=userIds).values('id', 'personalization'))

    # 是否个性化
    if assignmentDTO.isPersonalized:
        for user in users:
            # TODO 根据学生画像，通过大模型个性化地为学生生成或选择题目，生成的题目存入题库
            p = user['personalization']

            # 模型生成
            select_questions = [1, 2, 3]
            new_questions = [{}, {}, {}]
            # 格式 courseName chapterName content answer difficulty
            questionIds = [*select_questions]

            for question in new_questions:
                course = await Course.get(courseName=question['courseName']).values('id')
                chapter = await Chapter.get(chapterName=question['chapterName']).values('id')

                question = Question(**question,
                                    courseId=course['id'],
                                    chapterId=chapter['id'],
                                    userId=assignmentDTO.userId)
                await question.save()
                questionIds.append(question.id)

            await Assignment_Question.create(assignmentId=assignmentId,
                                             userId=user['id'],
                                             questionIds=str(questionIds))

    else:
        for user in users:
            await Assignment_Question.create(assignmentId=assignmentId,
                                             userId=user['id'],
                                             questionIds=str(assignmentDTO.questionIds))

    return Result.success()


@teacher_assignment.delete("/assignment")
async def del_assignment(assignmentIds: List[int] = Query(...)):
    await Assignment.filter(id__in=assignmentIds).delete()
    await Student_Assignment.filter(assignmentId__in=assignmentIds).delete()
    return Result.success()
