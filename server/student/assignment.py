from typing import Optional

from fastapi import APIRouter

from pojo.dto import AnswerListDTO
from pojo.entity import Course, Assignment, Student_Assignment, Assignment_Question, Question, Student_Answer
from pojo.vo import AssignmentVO
from pojo.result import Result
from util.chatglmApi import generate_eval
from util.dateParse import parse

student_assignment = APIRouter()


@student_assignment.get("/assignment")
async def get_assignments(userId: int, courseId: Optional[int] = None):
    # completed score submitTime userId assignmentId
    assignments = await Student_Assignment.filter(userId=userId)

    assignmentList = []
    for a in assignments:
        # courseName
        assignment = await Assignment.get(id=a.assignmentId)
        if courseId and assignment.courseId != courseId:
            continue

        course = await Course.get(id=assignment.courseId).values('courseName')
        assignmentVO = AssignmentVO(id=assignment.id,
                                    courseName=course['courseName'],
                                    title=assignment.title,
                                    deadline=assignment.deadline,
                                    overdue=assignment.overdue,
                                    completed=a.completed,
                                    score=a.score,
                                    createTime=parse(assignment.createTime))
        assignmentList.append(assignmentVO)

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
            question = await Question.get(id=qId).values("id", "content", "difficulty")
            questionList.append(question)
        finally:
            continue

    return Result.success(questionList)


@student_assignment.post("/assignment")
async def submit_assignment(answerListDTO: AnswerListDTO):
    # 通过两个id来查询答案和学生表
    num = len(answerListDTO.answers)
    weighted_score = 0.0

    for sAnswer in answerListDTO.answers:
        # 打分
        q = await Question.get(id=sAnswer.questionId).values('content', 'answer')
        score = generate_eval(q['content'], sAnswer.studentAnswer, q['answer'])
        weighted_score += score / num
        studentAnswer = await Student_Answer.filter(userId=answerListDTO.userId, questionId=sAnswer.questionId).first()

        if studentAnswer:
            await Student_Answer.filter(userId=answerListDTO.userId, questionId=sAnswer.questionId).update(
                studentAnswer=sAnswer.studentAnswer, score=score)
        else:
            await Student_Answer.create(userId=answerListDTO.userId, questionId=sAnswer.questionId,
                                        studentAnswer=sAnswer.studentAnswer, score=score)

    # 加权评分
    await Student_Assignment.filter(userId=answerListDTO.userId, assignmentId=answerListDTO.assignmentId).update(
        completed=True, score=weighted_score)

    return Result.success()
