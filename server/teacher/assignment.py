from typing import Optional, List
from fastapi import APIRouter, Query
from pojo.entity import Assignment, Assignment_Question, User, Question, Course, Chapter, Student_Assignment, \
    Student_Course, Student_Answer
from pojo.dto import AssignmentDTO, AssignmentGradeDTO
from pojo.vo import AssignmentVO, AssignmentCircumstanceVO, QuestionVO
from pojo.result import Result
from util.chatglmApi import generate_eval
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
                                                          'chapterId',
                                                          'title',
                                                          'deadline',
                                                          'overdue',
                                                          'createTime')

    assignmentList = []
    for a in assignments:
        course = await Course.get(id=a['courseId']).values('courseName')
        chapter = await Chapter.get(id=a['chapterId']).values('chapterName')

        assignmentList.append(AssignmentVO(id=a['id'],
                                           courseName=course['courseName'],
                                           chapterName=chapter['chapterName'],
                                           title=a['title'],
                                           deadline=parse(a['deadline']),
                                           overdue=a['overdue'],
                                           createTime=parse(a['createTime']))
                              .model_dump(exclude_unset=True))

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
            new_questions = [{}, {}, {}]
            # 格式 courseName chapterName content answer difficulty
            questionIds = []

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
        assignment_questions = []
        for user in users:
            for q in assignmentDTO.questionIds:
                assignment_questions.append(Assignment_Question(assignmentId=assignmentId,
                                                                userId=user['id'],
                                                                questionId=q))

        await Assignment_Question.bulk_create(assignment_questions)
    return Result.success()


@teacher_assignment.delete("/assignment")
async def del_assignment(assignmentIds: List[int] = Query(...)):
    await Assignment.filter(id__in=assignmentIds).delete()
    await Student_Assignment.filter(assignmentId__in=assignmentIds).delete()
    return Result.success()


@teacher_assignment.get("/assignment/{assignmentId}")
async def get_specific_assignments(assignmentId: int):
    assignments = await Student_Assignment.filter(assignmentId=assignmentId)
    assignmentList = []
    for a in assignments:
        user = await User.get(id=a.userId)
        assignmentList.append(AssignmentCircumstanceVO(
            userId=a.userId,
            userNumber=user.userNumber,
            name=user.name,
            completed=a.completed,
            score=a.score,
        ))
    return Result.success(assignmentList)


@teacher_assignment.get("/detail")
async def get_student_assignment_detail(userId: int, assignmentId: int, ):
    student_assignments = await (Assignment_Question.filter(userId=userId, assignmentId=assignmentId)
                                 .values('questionId', 'studentAnswer', 'score'))
    data = []
    for a in student_assignments:
        question = await Question.get(id=a['questionId']).values('content', 'difficulty')
        data.append(QuestionVO(
            id=a['questionId'],
            content=question['content'],
            difficulty=question['difficulty'],
            answer=a['studentAnswer'],
            score=a['score'])
        .model_dump(exclude_unset=True))
    return Result.success(data)


@teacher_assignment.post("/grade")
async def grade(assignmentGradeDTO: AssignmentGradeDTO):
    await Student_Assignment.filter(userId=assignmentGradeDTO.userId,
                                    assignmentId=assignmentGradeDTO.assignmentId).update(
        score=assignmentGradeDTO.assignmentScore)
    for q in assignmentGradeDTO.gradings:
        if await Assignment_Question.filter(userId=assignmentGradeDTO.userId,
                                            assignmentId=assignmentGradeDTO.assignmentId,
                                            questionId=q.questionId).first():

            await Assignment_Question.filter(userId=assignmentGradeDTO.userId,
                                             assignmentId=assignmentGradeDTO.assignmentId,
                                             questionId=q.questionId).update(score=q.score)
        else:
            await Assignment_Question.create(userId=assignmentGradeDTO.userId,
                                             assignmentId=assignmentGradeDTO.assignmentId,
                                             questionId=q.questionId,
                                             score=q.score)
    return Result.success()


@teacher_assignment.post("/assignment/autograde")
async def autograde_assignments(assignmentId: int):
    # 对所有的学生作业进行批改
    # 对某个学生的所有题目打分之后再对作业打分
    assignmentQuestions = await Assignment_Question.filter(assignmentId=assignmentId)
    for a in assignmentQuestions:
        questionId = a.questionId
        studentId = a.userId
        # 获取所有题目、学生答案
        question = await Question.filter(id=questionId).first().values("content", "answer")
        student_answer = await Student_Answer.filter(questionId=questionId, userId=studentId).first().values(
            "studentAnswer")
        score = generate_eval(question['content'], student_answer['studentAnswer'], question['answer'])
        # 题目打分
        await Assignment_Question.filter(assignmentId=assignmentId,questionId=questionId, userId=studentId).update(score=score)
    # 作业打分
    assignmentGrade = await Student_Assignment.filter(assignmentId=assignmentId).values("userId")
    for a in assignmentGrade:
        questionScores = await Assignment_Question.filter(assignmentId=assignmentId, userId=a['userId']).values("score")
        score = 0
        num = len(assignmentQuestions)
        for s in questionScores:
            score += s['score']
        score = score / num
        await Student_Assignment.filter(assignmentId=assignmentId, userId=a['userId']).update(score=score)

    return Result.success()
