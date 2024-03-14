from datetime import datetime
from typing import Optional

from fastapi import APIRouter

from pojo.entity import Assignment, Assignment_Question, User, Question, Course
from pojo.dto import AssignmentDTO
from pojo.vo import AssignmentVO
from util.result import Result

teacher_assignment = APIRouter()


@teacher_assignment.get("/teacher/assignment")
async def get_assignments(userId: int, courseId: Optional[int] = None):
    query: dict = {'userId': userId}
    if courseId:
        query['courseId'] = courseId

    assignments = await Assignment.filter(**query).values('id', 'courseId', 'title', 'deadline', 'overdue',
                                                          'createTime')

    assignmentList = []
    for a in assignments:
        assignmentVO = AssignmentVO(id=a['id'], title=a['title'], deadline=a['title'], overdue=a['overdue'],
                                    creatTime=a['createTime'])

        course = await Course.get(id=a['courseId'])
        assignmentVO.id = course.id
        assignmentList.append(assignmentVO)

    return Result.success(assignmentList)


@teacher_assignment.post("/teacher/assignment")
async def create_assignment(assignmentDTO: AssignmentDTO):
    assignmentDTO.createTime = datetime.now()
    assignmentDTO.updateTime = datetime.now()

    assignmentData = assignmentDTO.model_dump(exclude_unset=True)
    if not assignmentDTO.isPersonalized:
        assignmentData.pop('questionIds')

    assignment = Assignment(**assignmentData)
    await assignment.save()
    assignmentId = assignment.id

    # 是否个性化
    if assignmentDTO.isPersonalized:
        users = await User.filter(role=2).values('id', 'personalization')

        for user in users:
            # TODO 根据学生画像，通过大模型个性化地为学生生成或选择题目，生成的题目存入题库
            p = user['personalization']

            # 模型生成
            select_questions = [1, 2, 3]
            new_questions = [{}, {}, {}]
            questionIds = [*select_questions]

            for question in new_questions:
                question.update({
                    'courseId': assignmentData['courseId'],
                    'userId': assignmentData['userId'],
                    'chapter': assignmentData['chapter'],
                })

                question = Question(**question)
                await question.save()
                questionIds.append(question.id)

            for qId in questionIds:
                await Assignment_Question.create(assignmentId=assignmentId, questionId=qId)

    else:
        questionIds = assignmentDTO.questionIds

        for qId in questionIds:
            await Assignment_Question.create(assignmentId=assignmentId, questionId=qId)

    return Result.success()


@teacher_assignment.delete("/teacher/assignment")
async def del_assignment(assignmentId: int):
    await Assignment.filter(id=assignmentId).delete()
    # TODO 删除关联的所有..
    return Result.success()
