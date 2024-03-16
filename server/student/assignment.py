from typing import Optional

from fastapi import APIRouter
from datetime import datetime
from pojo.dto import AnswerListDTO
from pojo.entity import Course, Assignment, Student_Assignment, Assignment_Question, Question, Student_Answer
from pojo.vo import AssignmentVO
from util.result import Result

student_assignment = APIRouter()


@student_assignment.get("/student/assignment")
async def get_assignments(userId: int, courseId: Optional[int] = None):
    # completed score submitTime userId assignmentId
    assignments = await Student_Assignment.filter(userId=userId)

    assignmentList = []
    for a in assignments:
        # courseName
        assignment = await Assignment.get(id=a.assignmentId)
        if courseId and assignment.courseId != courseId:
            continue

        course = await Course.get(id=assignment.courseId)
        assignmentVO = AssignmentVO(id=assignment.id,
                                    courseName=course.courseName,
                                    title=assignment.title,
                                    deadline=assignment.deadline,
                                    overdue=assignment.overdue,
                                    completed=a.completed,
                                    score=a.score,
                                    createTime=assignment.createTime)
        assignmentList.append(assignmentVO)

    return Result.success(assignmentList)


@student_assignment.get("/student/assignment/detail")
async def get_assignment_detail(userId: int, assignmentId: int):
    # 通过assignmentId查询assignment_question的questionIds
    q = await Assignment_Question.get(userId=userId, assignmentId=assignmentId)
    questionIds = list(q.questionIds)
    # 用questionIds查询content、difficulty、两个time
    questionList = []
    for qId in questionIds:
        question = await Question.get(id=qId).values("id", "content", "difficulty")
        questionList.append(question)

    return Result.success(questionList)


@student_assignment.post("/student/assignment")
async def submit_assignment(answerListDTO: AnswerListDTO):
    # 通过两个id来查询答案和学生表
    for answer in answerListDTO.answers:
        # TODO 打分
        score = 100
        await Student_Answer.create(userId=answerListDTO.userId, questionId=answer.questionId,
                                    studentAnswer=answer.studentAnswer, score=score)
    # TODO 加权评分
    score = 100
    await Student_Assignment.filter(userId=answerListDTO.userId, assignmentId=answerListDTO.assignmentId).update(
        completed=True, score=score)

    return Result.success()
