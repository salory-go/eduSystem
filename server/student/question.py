import json
from typing import Optional

from fastapi import APIRouter, Response

from pojo.dto import AnswerDTO, QuestionDTO
from pojo.entity import Course, Question, Chapter, Student_Answer
from pojo.vo import QuestionVO, ReferenceVO, AnswerVO
from pojo.result import Result
from util.chatglmApi import generate_eval, generate_refer, generate_question
from util.dateParse import parse

student_question = APIRouter()


@student_question.get("/question")
async def get_questions(courseId: Optional[int] = None,
                        difficulty: Optional[int] = None,
                        chapterId: Optional[int] = None):
    query = {
        'courseId': courseId,
        'chapterId': chapterId,
        'difficulty': difficulty
    }
    query = {k: v for k, v in query.items() if v is not None}

    questions = await Question.filter(**query).values("id", "courseId", "chapterId", "content", "difficulty")
    questionList = []
    for q in questions:
        course = await Course.get(id=q["courseId"]).values('courseName')
        chapter = await Chapter.get(id=q["chapterId"]).values('chapterName')

        questionList.append(QuestionVO(id=q["id"],
                                       courseName=course["courseName"],
                                       chapterName=chapter["chapterName"],
                                       content=q["content"],
                                       difficulty=q["difficulty"])
                            .model_dump(exclude_unset=True))

    return Result.success(questionList)


@student_question.post("/question")
async def submit_answer(answerDTO: AnswerDTO):
    # 打分
    q = await Question.get(id=answerDTO.questionId).values('content', 'answer')
    score = generate_eval(q['content'], answerDTO.studentAnswer, q['answer'])

    studentAnswer = await Student_Answer.filter(userId=answerDTO.userId, questionId=answerDTO.questionId).first()

    if studentAnswer:
        await Student_Answer.filter(userId=answerDTO.userId, questionId=answerDTO.questionId).update(
            studentAnswer=answerDTO.studentAnswer, score=score)
    else:
        await Student_Answer.create(userId=answerDTO.userId, questionId=answerDTO.questionId,
                                    studentAnswer=answerDTO.studentAnswer, score=score)

    return Result.success()


@student_question.get("/question/reference")
async def get_reference(questionId: int):
    question = await Question.get(id=questionId).values("courseId", "chapterId", "content", "answer")
    course = await Course.get(id=question['courseId']).values('courseName')
    chapter = await Chapter.get(id=question['chapterId']).values('chapterName')

    # 用大模型生成解析
    res = generate_refer(question['content'], course['courseName'], chapter['chapterName'])
    print(res)
    reference = ReferenceVO(**res, answer=question['answer'])
    return Result.success(reference)


@student_question.get("/question/history")
async def get_history_answer(userId: int, questionId: int):
    studentAnswer = await Student_Answer.filter(userId=userId, questionId=questionId).first()
    answerVO = AnswerVO(studentAnswer=studentAnswer.studentAnswer,
                        score=studentAnswer.score,
                        submitTime=parse(studentAnswer.submitTime)).model_dump(exclude_unset=True)
    if studentAnswer:
        return Result.success(answerVO)
    else:
        result = json.dumps(Result.error('未曾作答').model_dump())
        return Response(status_code=400, media_type="application/json", content=result)


@student_question.post("/question/similar")
async def get_similar(questionDTO: QuestionDTO):
    res = generate_question(questionDTO.number,
                            questionDTO.courseName,
                            questionDTO.chapterName,
                            questionDTO.difficulty,
                            questionDTO.content)
    questionList = []
    for q in res:
        questionList.append(QuestionVO(courseName=questionDTO.courseName,
                                       chapterName=questionDTO.chapterName,
                                       difficulty=questionDTO.difficulty,
                                       **q)
                            .model_dump(exclude_unset=True))

    return Result.success(questionList)
