from typing import Optional

from fastapi import APIRouter

from pojo.dto import AnswerListDTO
from pojo.entity import Course, Assignment, Student_Assignment, Assignment_Question, Question, Student_Answer
from pojo.vo import AssignmentVO
from pojo.result import Result
import os
from zhipuai import ZhipuAI

from util.dateParse import parse

os.environ["ZHIPUAI_API_KEY"] = "your api key"
client = ZhipuAI()

student_assignment = APIRouter()

#%%

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
                                    deadline=parse(assignment.deadline),
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
    for answer in answerListDTO.answers:
        # TODO 打分
        question = await Question.get(id=answer.questionId)
        response = client.chat.completions.create(
            model="glm-4",
            messages=[
                {
                    "role": "user",
                    "content": "请你作为一名大学计算机教授，给我的作业打分（100分制），下面是我的作业题目和答案：\n"
                               "题目：{}\n答案：{}\n\n请打分，直接给出数字，不需要其他内容！".format(question.content, answer.studentAnswer)
                }
            ],
            top_p=0.7,
            temperature=0.9,
            stream=False,
            max_tokens=2000,
        )
        score = 100
        if response:
            score = float(response)
        studentAnswer = await Student_Answer.filter(userId=answerListDTO.userId, questionId=answer.questionId).first()

        if studentAnswer:
            await Student_Answer.filter(userId=answerListDTO.userId, questionId=answer.questionId).update(
                studentAnswer=answer.studentAnswer, score=score)
        else:
            await Student_Answer.create(userId=answerListDTO.userId, questionId=answer.questionId,
                                        studentAnswer=answer.studentAnswer, score=score)
    # TODO 加权评分
    score = 100
    await Student_Assignment.filter(userId=answerListDTO.userId, assignmentId=answerListDTO.assignmentId).update(
        completed=True, score=score)

    return Result.success()
