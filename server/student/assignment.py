from fastapi import APIRouter
from datetime import datetime
from pojo.dto import UserDTO, CourseDTO, AnswerListDTO
from pojo.entity import User, Course, Assignment, Student_Course, Student_Assignment, Assignment_Question, Question, \
    Student_Answer
from pojo.vo import AssignmentsOfStudentVO
from util.result import Result

student_assignment = APIRouter()

@student_assignment.get("/student/assignment")
async def get_course_assignments(user_id: int,courseId: int=None):
    # completed score submitTime userId assignmentId
    list = await Student_Assignment.filter(userId=user_id).values()
    all_assignments = []
    course_assignments = []
    for item in list:
        # courseName
        assignment = await Assignment.get(item.assignmentId)
        course = await Course.filter(courseId=assignment.courseId)
        title = assignment.title
        courseName = course.courseName
        deadline = assignment.deadline
        overdue = assignment.overdue
        createTime = assignment.createTime
        data = AssignmentsOfStudentVO(id=assignment.id,
                               courseName=courseName,
                               title=title,
                               deadline=deadline,
                               overdue=overdue,
                               completed=item.completed,
                               score=item.score,
                               createTime=createTime)
        all_assignments.append(data)
        if courseId==course.courseId:
            course_assignments.append(data)
    if courseId:
        return Result.success(course_assignments)
    return Result.success(all_assignments)

@student_assignment.get("/student/assignment/{assignmentId}")
async def get_assignment_detail(assignment_id: int):
    # 通过assignmentId查询assignment_question的questionIds
    questionIds = await Assignment_Question.filter(assignment_id=assignment_id).values()
    # 用questionIds查询content、difficulty、两个time
    questions = []
    for questionId in questionIds:
        question = await Question.get(id=questionId).values("id","content","difficulty")
        questions.append(question)

    return Result.success(questions)

#TODO 接口打分
@student_assignment.post("/student/assignment")
async def submit_assignment(answerListDTO: AnswerListDTO):
    #通过两个id来查询答案和学生表
    for answer in answerListDTO.answers:
        questionId = answer.questionId
        studentAnswer = answer.studentAnswer
        await Student_Answer.save(userId=answerListDTO.userId,questionId=questionId,studentAnswer=studentAnswer,
                                  score=100,submitTime=datetime.now())

    await Student_Assignment.save(userId=answerListDTO.userId, assignmentId=answerListDTO.assignmentId,
                                  completed=True,score=100,submitTime=datetime.now())

    return Result.success()