from typing import Optional

from fastapi import APIRouter
from tortoise import Tortoise

from pojo.dto import AnswerListDTO
from pojo.entity import Course, Assignment, Student_Assignment, Assignment_Question, Question, Student_Answer
from pojo.vo import AssignmentVO
from pojo.result import Result
from util.chatglmApi import generate_eval
from util.dateParse import parse

student_assignment = APIRouter()


@student_assignment.get("/assignment")
async def get_assignments(userId: int, courseId: Optional[int] = None):
    sql = '''
    SELECT sa.id, sa.completed, sa.score, a.courseId, a.title, a.deadline, a.overdue, a.createTime
    FROM student_assignment sa LEFT JOIN assignment a
    ON sa.assignmentId = a.id
    WHERE sa.userId = %s AND a.courseId = IFNULL(%s, a.courseId)
    '''

    result = await Tortoise.get_connection('default').execute_query(sql, [userId, courseId])
    await Tortoise.close_connections()
    assignments = result[1]

    assignmentList = []
    for a in assignments:
        course = await Course.get(id=a['courseId']).values('courseName')
        assignmentList.append(AssignmentVO(id=a['id'],
                                           courseName=course['courseName'],
                                           title=a['title'],
                                           deadline=parse(a['deadline']),
                                           overdue=a['overdue'],
                                           completed=a['completed'],
                                           score=a['score'],
                                           createTime=parse(a['createTime'])))

    return Result.success(assignmentList)


@student_assignment.get("/assignment/detail")
async def get_assignment_detail(userId: int, assignmentId: int):
    # 通过assignmentId查询assignment_question的questionIds
    q = await Assignment_Question.get(userId=userId, assignmentId=assignmentId)
    questionIds = list(q.questionIds)
    # 用questionIds查询content、difficulty、两个time
    questionList = []
    for qId in questionIds:
        try:
            question = await Question.get(id=qId).values("id",
                                                         "content",
                                                         "difficulty")
            questionList.append(question)
        finally:
            continue

    return Result.success(questionList)


@student_assignment.post("/assignment")
async def submit_assignment(answerListDTO: AnswerListDTO):
    # 通过两个id来查询答案和学生表
    for sAnswer in answerListDTO.answers:
        await (Assignment_Question
               .filter(userId=answerListDTO.userId, questionId=sAnswer.questionId)
               .update(studentAnswer=sAnswer.studentAnswer))

    await (Student_Assignment
           .filter(assignmentId=answerListDTO.assignmentId, userId=answerListDTO.userId)
           .update(completed=True))

    return Result.success()
